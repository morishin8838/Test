# coding: utf-8

import sys,os,math
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
from sklearn.tree import DecisionTreeClassifier

def get_ret_index(close):
    # リターンインデックス データーが昇順（日付が過去が上になって最新が一番下）になっている前提
    returns = pd.Series(close).pct_change() # 騰落率を求める
    ret_index = (1 + returns).cumprod() # 累積積を求める
    ret_index.iloc[0] = 1 # 最初の値を 1.0 にする
    return ret_index

def learn_data(arr,step):
    #train_X (教師データの配列) と train_y (それに対する 1 か 0 かのラベル) が戻る
    learn_X = []; 
    learn_y = [];
    flg=0;
    for i in np.arange(0, len(arr)-step):
        end = i + step# step日間の変化を素性にする
        data = arr.iloc[i:end]
        close= data['AdjClose']
        close.head()
        feature = get_ret_index(close)
        # その翌日、株価は上がったか？
        if close.iloc[-3] < arr['AdjClose'].iloc[end]:
            flg=1
        else:
            flg=0
        #print(close.iloc[-1],"<",arr['AdjClose'].iloc[end],flg)
        learn_X.append(feature.values)
        learn_y.append(flg) # YES なら 1  NO なら 0 
    # 上げ下げの結果と教師データのセットを返す
    return np.array(learn_X), np.array(learn_y)

def TestAcuraccy():
    "精度を確認する。学習時と同じデータをサンプルとして実施する。100点がとれるはず"
    test_y = []
    for i in np.arange(0,len(LrnX)-step):
        end = i + step
        # リターンインデックスと同じ期間をテストとして分類させてみる
        test_x = LrnX[i:end]
        #print(type(test_x))
        # 結果を格納して返す
        result = clf.predict(test_x)
        test_y.append(result[0])
        
def Judgement(tm, num, zz, st, a, b):
    CorrectFlg =True;
    if a > 0:
        if b == 1:
            Predict = "Rise"
        else:
            Predict = "Down"
            CorrectFlg =False;
    else:
        if b == 1:
            Predict = "Rise"
            CorrectFlg =False;
        else:
            Predict = "Down"
    print("{} {} {} step({}) {}-{}-{} [Predict : {}] Result: ¥{}".format(tm, num, CorrectFlg, st, zz.year,zz.month,zz.day,Predict, a))    
    return CorrectFlg


def calc_decision_tree_prdct(code, start, xday):
    "条件を変えながら、決定木で株価を予想する。"
    
    csvfile = "stock_{}.csv".format(str(code));    
    print("From {} to {} by {}".format(start,xday, step))
    dic_score={}
    # 'M' is month-end, instead I need same-day-of-month
    #t_piriod= pd.date_range(start, xday, freq='M')
    t_piriod= pd.date_range(start, xday, freq='W')
    t_piriod=t_piriod[int(len(t_piriod)/5):-2]

    if os.path.isfile(csvfile):
        df = pd.read_csv(csvfile, index_col=0, parse_dates=True)
        #for st in np.arange(step-ofst,step+ofst,int(30)):
        s_st = 20;  # Calc Condition Start(day)
        e_st = 30; # Calc Condition End(day)
        width= 1;  # 1 Month
        mmm= np.arange(s_st,e_st,width)
        calc_cnt_all=len(mmm)*len(t_piriod); calc_cnt=0;
        data=[];
        for st in mmm:
            strike=[]
            for tt in t_piriod:
                calc_cnt=calc_cnt+1;
                CalcPrgsDisp="({}/{})".format(calc_cnt, calc_cnt_all)
                #1) 教師データ作成
                #start = datetime.datetime.strptime(start, '%Y-%m-%d')
                dx=df.loc[start:tt]
                dx = dx.dropna()
                LrnX,LrnY =learn_data(dx,st)

                #2) 学習させる
                # 決定木のインスタンスを生成
                clf = DecisionTreeClassifier()
                # 学習させる
                clf.fit(LrnX, LrnY)

                #3) 予測させる
                i=len(dx)-st
                #print(dx['AdjClose'][i:i+step].values.reshape(1,-1))
                result = clf.predict(dx['AdjClose'][i:i+st].values.reshape(1, -1))
                #print(result)
                #翌日取得（１日オフセット）
                for ofset_day in [1,2,3,4,5]:
                    zz =dx.index[-1]+ timedelta(days=ofset_day)
                    #予測日（翌日）の上下結果取得
                    if (len(df[df.index== zz]))!=0:
                        break
                    else:
                        pass
                        #print("...Retry maybe weekend day")
                xx = (df[df.index== zz].AdjClose[0]) - (df[df.index== dx.index[-1]].AdjClose[0])
                if not math.isnan(xx):
                    #print("{} {}".format(df[df.index== zz].AdjClose[0],(df[df.index== dx.index[-1]].AdjClose[0])))
                    tm=datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                    data.append([tm,tt,zz,st,int(result[0]),xx,CalcPrgsDisp])
                    strike.append(Judgement(tm, CalcPrgsDisp, zz, st, int(xx),int(result[0])));
                else:
                    pass
                    #print("... Skip calc because of NAN")
            score=np.count_nonzero(strike)/float(len(strike))
            #print("Step {} : Winning percentage {}[%]".format(st, score*100))
            dic_score[st]=score;
        print("----- End calc_decision_tree_prdct -----")
        for k, v in dic_score.items():
            print("Step {} : Winning percentage {}[%]".format(k, v))
        #xx=pd.Series(dic_score)
        xx=pd.DataFrame(data,columns=["LogTime","VirtualDate","PredictDate","CalcCond","LrnResult","ActualValue","CalcCount"])
        out_csvfile = "stock_{}_decision_tree.csv".format(str(code));    
        xx.to_csv(out_csvfile)
    else:
        print("Nothing csv file")    
        
def calc_decision_tree(code, start, xday, step):
    "決定木で株価を予想する。stepの値はcalc_decision_tree_prdctで決定する"
    
    csvfile = "stock_{}.csv".format(str(code));    
    print("From {} to {} by {}".format(start,xday, step))
    if os.path.isfile(csvfile):
        #1) 教師データ作成
        df = pd.read_csv(csvfile, index_col=0, parse_dates=True)
        #start = datetime.datetime.strptime(start, '%Y-%m-%d')
        dx=df.loc[start:xday]
        dx = dx.dropna()
        
        step = int(step)
        LrnX,LrnY =learn_data(dx,step)

        #2) 学習させる
        # 決定木のインスタンスを生成
        clf = DecisionTreeClassifier()
        # 学習させる
        clf.fit(LrnX, LrnY)

        #3) 予測させる
        i=len(dx)-step
        #print(dx['AdjClose'][i:i+step].values.reshape(1,-1))
        result = clf.predict(dx['AdjClose'][i:i+step].values.reshape(1, -1))
        #print(result)

        #翌日取得（１日オフセット）
        zz =dx.index[-1]+ timedelta(days=1)
        #予測日（翌日）の上下結果取得
        xx = (df[df.index== zz].AdjClose[0]) - (df[df.index== dx.index[-1]].AdjClose[0])
        Judgement(zz, step, int(xx),int(result[0]));
    else:
        print("Nothing csv file")    
if __name__ == '__main__':
    code = sys.argv[1] # 
    start = sys.argv[2] # 学習開始日時
    xday  = sys.argv[3] # 予測日
    mode  = sys.argv[4] # mode
    step  = sys.argv[5] # step
    
    if mode=='Lrn':
        calc_decision_tree_prdct(code, start, xday);
    elif mode =='Predict':
        calc_decision_tree(code, start, xday, step);
    else:
        print(" No Mode")
                      
    

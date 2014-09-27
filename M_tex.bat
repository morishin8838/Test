@echo off
REM TeXworksでtex文章を作る方法
REM http://blog.mochiring.net/archives/805
REM 1) 起動後、編集から設定を開きます
REM 2) タイプセットタブを開きコンパイルのための設定をします．
REM 3) タイプセットの方法の追加する
REM 4) 以下の命令列を書き,batという拡張子で保存
REM 5) 新しいタイプセットを登録
REM 6) 引数は，バッチファイル引数で拡張子を除くファイル名を表す$basenameを指定
REM
REM

platex -guess-input-enc -interaction=nonstopmode "%1".tex
dvipdfmx -f ptex-ipaex.map "%1".dvi

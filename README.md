# Private notebook files

I'm impressed notebook of ipython, called jupyter now. I would try to introduce my work flow to improve my jobs. so I created some samples using notebook. then I would present the files as sample using nbviewer. :smile:  
[top-level of samples](http://nbviewer.ipython.org/github/morishin8838/nbviewer/blob/master/index.ipynb)  
next, I introduced nbviewer server in local, so  I would present my procedure in this repo.  
Finally, I would challenge "handler.py" of nbviewer provider to custom to put tree directory such as github, but I can't.:cry:   
if you success to create custom "handler.py" for local provider , which has tree directory displayed, please inform me.

## Procedure to publish your notebook file via github
1. push the ipynb files to github
    e.g  (https://github.com/morishin8838/nbviewer/index.ipynb)
2. access the ipynb file via nbviewer
    e.g  (http://nbviewer.ipython.org/github/morishin8838/nbviewer/blob/master/index.ipynb)
3. you can download files above button.

## Set up nbviewer server to opparation in local PC.
As you know, we can introduce nbviewer server besed on the repo [nbviewer/jupyter](https://github.com/jupyter/nbviewer).  
it is easy to introduce it using "docker". but I'm not familiar with "docker".:cry:  and then I also introduced nbserver in using of private network. here is my procedure.

1. Download the nbviwer from repo [nbviewer/jupyter](https://github.com/jupyter/nbviewer).
2. cd repo
3. python setup.py install
4. Download the static files [morishin8838/nbviewer_static_files](https://github.com/morishin8838/nbviewer_static_files)
5. copy the static files to the static directory of site-package "nbviewer", which has installed by the repo of nbviewer.

## How to create CSS of nbviewer package.
In case you want to creat notebook.css, styles.css and slides.css yourself, you could take that below flow,

1. Download [less.js-windows-v2.5.1a](https://github.com/duncansmart/less.js-windows/releases)  
2. prepare less files of static in the repo [nbviewer/jupyter](https://github.com/jupyter/nbviewer).  
3. cd <lessc.cmd located directory>  
4. .\lessc.cmd　--include-path='.\less' --source-map='.\static\less'  .\less\styles.less styles.css  
5. .\lessc.cmd　--include-path='.\less' --source-map='.\static\less'  .\less\notebook.less notebook.css  
6. .\lessc.cmd　--include-path='.\less' --source-map='.\static\less'  .\less\slides.less slides.css  


Thanks!
:yum:



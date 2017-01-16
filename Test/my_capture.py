#!/usr/bin/env python
#coding:utf-8
'''
Created on Sep 11, 2015

@author: yang.hongsheng
'''

# <== include('examples/showgrabbox.py')==>
from entrypoint2 import entrypoint
from pyscreenshot import grab


@entrypoint
def show(backend='auto'):
    if backend == 'auto':
        backend = None
    im = grab(bbox=(100, 200, 300, 400), backend=backend)
    im.show()
# <==end==>
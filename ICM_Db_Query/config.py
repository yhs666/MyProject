#!/usr/bin/env python
#coding:utf-8
'''
Created on Jan 3, 2017

@author: yang.hongsheng
'''
import json

def config():
    f= open('config.dat', 'r')
    c = json.load(f)
    f.close()
    return c


#!/usr/bin/env python
#coding:utf-8
'''
Created on Jan 3, 2016

@author: yang.hongsheng
'''
import time
from autopy import key,alert
pin ="ddddddd"
if alert.alert("is ok","message", default_button="OK", cancel_button="Cancel"):
    time.sleep(5)
    key.type_string(pin,120)
    #key.tap(key, )
    
    
    
    
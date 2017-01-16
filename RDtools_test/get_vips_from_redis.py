#!/usr/bin/env python
#coding:utf-8
'''
Created on Dec 19, 2015

@author: yang.hongsheng
'''

import pickle as p 
import cPickle 
import redis
import time
import win32con
import win32clipboard as w

ip ="waps-20"
time_out = 60
myredis = redis.Redis(host=ip,password="www.wasu.com")
cluster = [
    "BJBPrdApp01",
    "BJBPrdApp02",
    "BJBPrdApp03",
    "BJBPrdApp04",
    "BJBPrdApp05",
    "SH2PrdApp01",
    "SH2PrdApp02",
    "SHAPrdApp01",
    "SHAPrdApp02",
    "SH3PrdApp01",
    "SH3PrdApp02",
    "BJBPrdDDC01",
    "BJBPrdDDC02",
    "BJBPrdPFCC01",
    "BJBPrdStr01",
    "BJBPrdStr02",
    "SH2PrdPFCC01",
    "SH2PrdStr01",
    "SHAPrdDDC01",
    "SHAPrdPFCC01",
    "SHAPrdStr01",
    "SH3PrdDDC01",
    "SH3PrdPFCC01",
    "SH3PrdStp01",

    ]

def get_vips(myredis,key):
    print "Get %s vips" % key
    key = key +":vips"
    return  cPickle.loads(myredis.get(key))


print len(cluster)
for i in cluster:
    print "-------------------"
    print get_vips(myredis,i)
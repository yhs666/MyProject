#!/usr/bin/env python
#coding:utf-8
'''
Created on Dec 19, 2015

@author: yang.hongsheng
'''
import cPickle 
import redis
import time
import sys
ip ="waps-20"
password = "www.wasu.com"
time_out = 60
try:
    myredis = redis.Redis(host=ip,password=password,port = 6379)
except:
    print "Redis connect issue!"
    sys.exit()

office365 =[
            ["42.159.32.1","42.159.63.254"],
            ["42.159.160.1","42.159.191.254"],
            ["139.219.16.1","139.219.30"],
            ["139.219.17.1","139.219.17.254"],
            ["139.219.145.1","139.219.145.30"],
            ["139.219.146.1","139.219.146.254"]

            ]

webapp = [
          ["42.159.5.43","BJ-6c2a711961ac48c3b24d33b0da5241f2"],
          ["42.159.4.236","c771c2fd00aa493eb5ad275e21d92b75"],
          ["42.159.132.179","SH-d77bac0cac04496085e26ba598acd0c9"]
          
          ]


def set_to_redis(rs,myredis,key):
    try:
        keyvip = key +":vips" 
        if myredis.set(keyvip,cPickle.dumps(rs)):
            keytime = key + ":time"
            myredis.set(keytime,time.asctime())
            return True
        else:
            print "issue"
            return False
    except:
        return False

if set_to_redis(office365, myredis, "office365"): print "write office365 ips"
if set_to_redis(webapp, myredis, "webapp"): print "write webapp ips"
myredis.bgsave()

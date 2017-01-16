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
ip ="hs-linux.chinacloudapp.cn"
time_out = 60
try:
    myredis = redis.Redis(host=ip)
except:
    print "Redis connect issue!"
    sys.exit()

key ="test"
rs = '''
def f(x):
    x = x + 1
    return x

print 'This is my output.'
c= 4
def main():
    print f(c)

main()

'''
if myredis.set(key,cPickle.dumps(rs)):
    print "set ok"


time.sleep(5)
d = cPickle.loads(myredis.get(key))
#print d

exec d
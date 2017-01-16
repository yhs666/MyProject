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
import sys
ip ="waps-20"
password = "www.wasu.com"
time_out = 60
try:
    myredis = redis.Redis(host=ip,password=password,port = 6379)
except:
    print "Redis connect issue!"
    sys.exit()





def getText():
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_TEXT)
    w.CloseClipboard()

    return d

def setText(aString):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_TEXT, aString)
    w.CloseClipboard()

def check_show(rs):
    ips = []
    for i in rs:
        if i.strip() and i[:4] =="    " and "Success" not in i:
            if "-" in i:
                a = i.strip().split('-')
                ips.append(a)
    return ips
def showvipranges(rs):
    ips =""
    rs = rs.split('\n')
    if len(rs) > 2:
        ips = check_show(rs)
    else:
        rs = rs.split('\r\n')
        if len(rs) > 2:
            ips = check_show(rs)
    return ips

def set_to_redis(rs,myredis,key):
    try:
        keyvip = key +":vips" 
        if myredis.set(keyvip,cPickle.dumps(showvipranges(rs))):
            keytime = key + ":time"
            myredis.set(keytime,time.asctime())
            return True
        else:
            return False
    except:
        return False

def cmd_str(i):
    cmd = "fcclient.exe c:" + i +"  ShowVipRanges"   
    setText(cmd)
    return cmd
    
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

#cluster = ["BJBPrdApp01"]
cluster_none = [
    
    #"BJBUFCProd",

    #"SH2UFCProd",

    #"SHAUFCProd",

    #"SH3UFCProd",
    ]

for i in cluster:
    cmd = cmd_str(i)
    begin_time = time.time()
    end_time = time.time()
    print "start get %s vip ranges" % i
    while (time.time() - begin_time) < 500:
        time.sleep(1)
        try:
            rs = getText()
        except:
            print "run $s have issue" % i
            rs =""
            break
        if rs != cmd and len(rs.strip()) >100:
            break
        
            
            
    if len(rs) > 2:
        set_to_redis(rs,myredis,i)
        print " %s showvipranges had done!" % i
    time.sleep(1)
myredis.bgrewriteaof()

print "RUn over!"        
        
        
# time.sleep(10)
# 
# def get_vips(myredis,key):
#     print "Get vips"
#     key = key +":vips"
#     return  cPickle.loads(myredis.get(key))
# 
# 
# print get_vips(myredis,"BJBPrdApp01")

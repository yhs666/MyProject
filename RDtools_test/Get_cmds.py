#!/usr/bin/env python
#coding:utf-8
'''
Created on Dec 25, 2015

@author: yang.hongsheng
'''

import cPickle 
import redis
import time,sys
import win32con
import win32clipboard as w
import getpass

ip ="waps-20"
password="www.wasu.com"
time_out = 60
try:
    myredis = redis.Redis(host=ip,password=password)
    print "Connect Redis OK!"
except:
    print "Connect Redis issue! quit!"
    sys.exit()
    
import logging
import os
FILE=os.getcwd()

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename = os.path.join(FILE,'log.txt'),
                    filemode='w')
logging.info('msg')
logging.debug('msg2')

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


user_name = getpass.getuser()
print user_name

user_list=["yang.hongsheng","jiang.shixun"]

def user_cmd(username,key):
    r = username + ":" +key
    return r 

def user_get(username):
    a = [user_cmd(username, "cmds"),user_cmd(username, "status")]
    return a

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

cmds =[] 
cmds_name =[]
for i in user_list:
    #if myredis.exists(i):
    res = myredis.mget(user_get(i))
    if res[0] != None and res[1] =="submit":
        cmd = res[0].strip().strip(';')
        cmds.append(cmd)
        cmds_name.append(i)
        msg = "  username: %s  commands: %s" % (i,cmd)
        logging.info(msg)
        
        
print cmds,cmds_name
      
if cmds and cmds_name and getText() == "done":
    cmds_str = ";".join(cmds)
    setText(cmds_str)
    for i in cmds_name:
        myredis.set(user_cmd(i,"status"),"running")
        
    msg = "  Run commands: %s" % cmds_str
    logging.info(msg)
else:
    msg = "  Commands None or Powershell run other command, need wait" 
    logging.info(msg)    


#if  __name__=='__main__':
    

        
        
    
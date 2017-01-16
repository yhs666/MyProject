#!/usr/bin/env python
#coding:utf-8
'''
Created on 2016年1月9日

@author:yang.hongsheng 
'''

import cPickle 
import redis
import time
import win32con
import win32clipboard as w
import logging
import sys,os
import hashlib
import threading

ip ="waps-20"
password = "www.wasu.com"
time_out = 60
local_thread = threading.local()
FILE=os.getcwd()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename = os.path.join(FILE,'log.txt'),
                    filemode='w')
try:
    myredis = redis.Redis(host=ip,password=password,port = 6379)
    print "Connect Redis OK!"
    logging.info('Connect Redis OK!')

except:
    print "Redis connect issue!"
    logging.info('Redis connect issue!')
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

    
    
def open_file(filename):
    if os.path.exists(filename):
        try:
            myfile = open(filename, "r") # or "a+", whatever you need
            
            return myfile
        except:
            print "open file error "
            return False
    else:
        print "File no exists"
        return False

def user_cmd(username,key):
    r = username + ":" +key
    return r 

def user_get(username):
    a = [user_cmd(username, "cmds"),user_cmd(username, "status")]
    return a


def set_to_redis_more(mhash,res):
    
    try:

        key1 = mhash +":cmd" 
        key2 = mhash +":res" 
    
        keytime = mhash + ":time"            
        myredis.mset({key2:cPickle.dumps(res),keytime:time.ctime(), key1:hash_cmd[mhash]})
        
        msg = "  Commands: %s Hash: %s  Status: %s " % (hash_cmd[mhash],mhash,"Done")
        logging.info(msg)
        return True
    except:
        msg = "  Commands: %s Hash: %s  Status: %s " % (hash_cmd[mhash],mhash,"issue!")
        logging.info(msg)
        return False

 

def thread_wait_result(filename,mhash, wait_time =500):

    begin_time=time.time()
    while (time.time() - begin_time) < wait_time:
        time.sleep(1)
        #f = open_file(filename)
        f =open_file(filename)
   
        if f:
            x = f.read().splitlines()

            set_to_redis_more(mhash,x)
            
            break
        else:
            continue
        
    else:
        sys.stdout.write("Time out!")
        sys.stdout.flush()
        msg = "  Run commands: %s  %s   timeout! " % (hash_cmd[mhash],mhash)
        logging.info(msg)
        
file_path = "E:\\robbot\\"
user_list=["yang.hongsheng","jiang.shixun"] 

while True:
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
        time.sleep(1) 
        continue   



    time.sleep(5)
    hash_cmd ={}
    files_name = []
    hashs =[]
    run_cmd_username =[]
    for j in range(len(cmds)):
        for k in cmds[j].split(";"):
            
            hash_j = hashlib.md5(k).hexdigest()
            hash_cmd[hash_j]= k

            data_name = file_path + hash_j
            files_name.append(data_name)
            hashs.append(hash_j)
            run_cmd_username.append(cmds_name[j]) 
            msg = "  Commands: %s Hash: %s  Useranem: %s " % (k,hash_j,cmds_name[j])
            logging.info(msg)
            print msg
     
    threads = []
    n=0   
    print files_name
    for filename in files_name:    
        print filename
        t = threading.Thread(target=thread_wait_result,args=(filename,hashs[n],))
        threads.append(t)
        n=n+1


    for t in threads:
        t.setDaemon(True)
        t.start()
    
    # wait the thread over
    for t in threads:
        t.join()

    print "--------------Done---------------"
            
        
    time.sleep(1)
    
  
    
myredis.bgrewriteaof()

print "RUn over!"        


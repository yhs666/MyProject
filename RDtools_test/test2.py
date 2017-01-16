#!/usr/bin/env python
#coding:utf-8
'''
Created on Dec 29, 2015

@author: yang.hongsheng
'''
import cmd
import os
from win32con import FILE_NAME_NORMALIZED
cmd = "dir"
import hashlib



file_name = "7acd181852b2e06486d7a8b26d502f7f"
file_path = ""

data_name = file_path + file_name
print data_name

def open_file(data_name):
    if os.path.exists(data_name):
        try:
            myfile = open(data_name, "r") # or "a+", whatever you need
            
            return myfile
        except:
            print "Could not open file! "
            return False
    else:
        print "could not open file"
        return False

def showvipranges(f):
    # list_data_name =open(data_name, "r").read().splitlines() 
    #sys.stdout.write("%s\n" % x)
    x = f.read().splitlines()
    s_start =6
    key_end ="  -- Action Succeeded -- "
    key_in = "    "
    res =[]
    #print x[-1]
    if  key_end == x[-1]:       
        for i in range(s_start,len(x)-4):
            #if x[i][0:4]== key_in:
            if len(x[i]) >=21 and len(x[i]) <= 35:
                #    42.159.224.10-42.159.231.250
                y = x[i].strip().split("-")
                res.append(y)
  
    else:  
        res=[]
     
    #print res    
    return res
  
  
# 
# f = open_file(data_name)
# print f
# if f:
#     z= showvipranges(f)
#     print "----------------------------------------------"
#     for i in z:
#         print i
#     


import threading

    
import cPickle 
import redis
import time
import win32con
import win32clipboard as w
import sys,os
import hashlib
from time import sleep,ctime

#from __future__ import print_function
#print = lambda x: sys.stdout.write("%s\n" % x)

ip ="waps-20"
password = "www.wasu.com"
time_out = 60
try:
    myredis = redis.Redis(host=ip,password=password,port = 6379)
except:
    print "Redis connect issue!"
    sys.exit()
def music(func):
    
    f = open_file(func)
    if f:
        z= showvipranges(f)
        #print "thisis:" ,z
        x = "yanghongsheng"
        x=""
        for i in z:
            x = x +','.join(i)
        
        #sys.stdout.write("%s\n" % x)
        name = threading.currentThread().getName()
        print z,threading.currentThread().getName()
        
#         s = ''.join(z)
#         sys.stdout.write(s)  # same as print
#         sys.stdout.flush()

def move(func):
    
    f = open_file(func)

    if f:
        z= showvipranges(f)
        x = "yanghongsheng"
        x=""
        for i in z:
            x = x +','.join(i)
        #sys.stdout.write("%s\n" % x)
#         s = ''.join(w)
#         sys.stdout.write(s)  # same as print
#         sys.stdout.flush()33
    print z,threading.currentThread().getName()
         
        
        
import threading

threads = []

t1 = threading.Thread(target=music,args=("1",))
threads.append(t1)
t2 = threading.Thread(target=move,args=("2",))
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    
    # wait the thread over
    for t in threads:
        t.join()
        
        
        
    print "------------------------------------"
    print "all over %s" %ctime()


    

    
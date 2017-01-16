#!/usr/bin/env python
#coding:utf-8
'''
Created on Dec 19, 2015

@author: yang.hongsheng
'''

#!/usr/bin/env python
#coding:utf-8
'''
Created on Dec 19, 2015

@author: yang.hongsheng
'''


import cPickle 
import redis
import time
import win32con
import win32clipboard as w
import sys,os
import hashlib
import threading

ip ="waps-20"
password = "www.wasu.com"
time_out = 60
local_thread = threading.local()
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

def showvipranges(f):
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


def set_to_redis_more(cmd,res):
    
    try:

        keyvip = cmd +":vips" 
        keytime = cmd + ":time"            
        myredis.mset({keyvip:cPickle.dumps(res),keytime:time.ctime()})
        
        return True
    except:
        return False

def cmd_str(i):
    cmd = "fcclient.exe c:" + i +"  ShowVipRanges"   
    #setText(cmd)
    return cmd

def cmds_str(list_i):
    cmd =""
    for i in list_i:
        cmd = cmd + "fcclient.exe c:" + i +"  ShowVipRanges;" 
      
    #setText(cmd)
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

def cluster_deal(cluster):
    c =[]
    d=[]
    thread_n =10
    chang = len(cluster) 
    zheng = chang / thread_n
    yu = chang % thread_n
    for i in range(0,zheng):
        
        for j in range(0,thread_n):
            k = i*thread_n +j
            d.append(cluster[k])
        
        c.append(d)
        d=[]
    for i in range(0,yu):
        k= zheng * thread_n + i
        d.append(cluster[k])
    
    c.append(d)
    
    return c



def get_fc_cmd(cmd):
    #cmd = "fcclient.exe c:" + i +"  ShowVipRanges"
    fc_cmd=""
    cmd_list = cmd.strip().split()
    if len(cmd_list) >= 3:
        fc_cmd = cmd_list[2].strip().split(":")
    
    return fc_cmd   

def thread_wait_result(filename,cluster_name, wait_time =500):

    begin_time=time.time()
    while (time.time() - begin_time) < wait_time:
        time.sleep(1)
        #f = open_file(filename)
        f =open_file(filename)
   
        if f:
            res= showvipranges(f)
          
            #print  res 
            print "---------------------------------"
            set_to_redis_more(cluster_name,res)
            break
        else:
            continue
        

file_path = "E:\\robbot\\" 
#cluster = ["BJBPrdApp01"]


# 创建全局ThreadLocal对象:

cluster = [
    "BJBPrdApp01",
    "BJBPrdApp02"
    ]
for i in cluster_deal(cluster):
    print "---------------------------------------------------"
    #cmd = ';'.join(i)
    cmd = cmds_str(i)
    setText(cmd)
    begin_time = time.time()
    end_time = time.time()
    hash_res =[]
    files_name =[]
    cmd0 = cmd.strip(";").split(";")
    for j in cmd0:
        print j
        hash_j = hashlib.md5(j).hexdigest()
        hash_res.append(hash_j)
        data_name = file_path + hash_j
        files_name.append(data_name) 
     
    threads = []
    n=0   
    print files_name
    for filename in files_name:    
        print i[n]  
        print filename
        t = threading.Thread(target=thread_wait_result,args=(filename,i[n],))
        threads.append(t)
        n=n+1


    for t in threads:
        t.setDaemon(True)
        t.start()
    
    # wait the thread over
    for t in threads:
        t.join()

    print "--------------Done---------------"
            
        
    time.sleep(2)
    
  
    
myredis.bgrewriteaof()

print "RUn over!"        


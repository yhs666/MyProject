#!/usr/bin/env python
#coding:utf-8
'''
Created on Dec 19, 2015

@author: yang.hongsheng
'''
import pickle as p 
import cPickle 
import redis
import time,sys
import win32con
import win32clipboard as w
from tempfile import _name_sequence

ip ="waps-20"
time_out = 60
password = "www.wasu.com"
try:
    myredis = redis.Redis(host=ip,password=password)
    #print cPickle.loads(myredis.get("webapp:vips"))
except:
    print "Connect Redis issue! quit!"
    #sys.exit()
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
    #print "Get %s vips" % key
    key = key +":vips"
    #print cPickle.loads(myredis.get(key))
    return  cPickle.loads(myredis.get(key))


def check_ip_cluster(ips,ip):
    flag =False
    for i in ips:
        ip_list_start = i[0].split(".")
        ip_list_end =  i[1].split(".")
        ip_list = ip.split(".")
        for j in range(0,4):
            if int(ip_list[j]) == int(ip_list_start[j]):
                continue
            elif (int(ip_list[j]) >= int(ip_list_start[j])) and (int(ip_list[j]) <= int(ip_list_end[j])):
                flag=True
                break
            else:
                break
    
        if flag:
            #print "check_ip_cluster: Find ip." 
            break
        
    return flag  


def find_ip(myredis,ip):
    res = []  
    #webapp
    if res ==[]:
        ips = get_vips(myredis,"webapp")
        for i in ips:
            if i[0]== ip:
                res.append("webapp")
                break
            else:
                res = []   
    #vips
    if res ==[]:
        for i in cluster:
            ips = get_vips(myredis,i)
            #print ips
            if check_ip_cluster(ips, ip):
                #print i
                res.append(i)
                #break
                continue

    #office365
    if res ==[]:
        ips = get_vips(myredis,"office365") 
        if check_ip_cluster(ips, ip):
            res.append("office365")
        else:
            res =[]

    return res

if  __name__=='__main__':
    ip = "42.159.5.43"
    while 1:
        ip = raw_input("Please input your check ip:")
        res = find_ip(myredis,str(ip))
        if res == []:
            print "Can not find this ip in cluster!"
        else:
            print res

    
    
    
    
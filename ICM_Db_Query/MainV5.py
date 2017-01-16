#!/usr/bin/env python
#coding:utf-8
'''
Created on Oct 17, 2016

@author: yang.hongsheng
'''
import _mssql
#import os,pymssql
#import logging
import sys
#import MySQLdb
#import hashlib
#import openpyxl
import autopy


#from datetime import datetime
from insert_logs import print_logs
from SummaryQuery import *
from Insert_mysql import *
from insert_execl import *
from Input_date import input_main


#reload(sys)  
#sys.setdefaultencoding('utf8') 

DATETIME_FMT = '%Y-%m-%d %H:%M:%S'
import json

global config

config = json.load(open('config.dat', 'r'))

if __name__=='__main__':
    
    startdate,enddate_or_tickets_info,name,s,mysqlflag = input_main()
    
    if s=="1":
        print '*'*50
        tickets_info = get_icm_report_data(startdate,enddate_or_tickets_info)
        print '*'*50
        #print tickets_info
        if mysqlflag=="y":
            print "Insert mysql issue: ", insert_tickets_icm_report(tickets_info,name)
        else:
            print "The Query Date Not Insert Mysql Database!"
            
        print "Insert execl issue: ",insert_execl(tickets_info)
        
    elif s=="2":
        print '*'*50
        efforttime = get_icm_efforttime_data(sql_key=enddate_or_tickets_info)
        print '*'*50
        if mysqlflag=="y":
            print "Insert mysql issue: ", insert_tickets_effort(efforttime,name)
        else:
            print "The Query Date Not Insert Mysql Database!"   
             
        print "Insert execl issue: ",insert_execl_effort(efforttime)
        
    elif s=="3":
        print '*'*50
        efforttime = get_icm_efforttime_data(startdate=startdate,enddate=enddate_or_tickets_info)
        print '*'*50
        if mysqlflag=="y":
            print "Insert mysql issue: ", insert_tickets_effort(efforttime,name)
        else:
            print "The Query Date Not Insert Mysql Database!" 
            
        print "Insert execl issue: ",insert_execl_effort(efforttime)
    elif s=="4":
        print '*'*50
        tickets_info = get_icm_report_datav2(enddate_or_tickets_info)
        print '*'*50
        #print tickets_info
        if mysqlflag=="y":
            print "Insert mysql issue: ", insert_tickets_icm_report(tickets_info,name)
        else:
            print "The Query Date Not Insert Mysql Database!"
             
        print "Insert execl issue: ", insert_execl(tickets_info)
    elif s =="5":
        print '*'*50
        tickets_info=get_icm_report_datav5(startdate,enddate_or_tickets_info)
        print tickets_info
        print '*'*50
        
        if mysqlflag=="y":
            print "Insert mysql issue: ", insert_tickets_icm_report(tickets_info,name)
        else:
            print "The Query Date Not Insert Mysql Database!"
            
        print "Insert execl issue: ",insert_execl(tickets_info)
        
    print "-"*50
    print_logs("Run done!")
    #autopy.alert.alert(msg="Had Done the work!",title="ICM Report",)
    autopy.alert.alert(msg="ICM Report",title="Had Done the work")
    sys.exit()




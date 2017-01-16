#!/usr/bin/env python
#coding:utf-8
'''
Created on Oct 20, 2016

@author: yang.hongsheng
'''
import sys
from datetime import datetime
from get_users import get_users
import hashlib

DATETIME_FMT = '%Y-%m-%d %H:%M:%S'

def menu_selec():
    print  '''
    
    Please Select the function  index num:
    
    [1]  Query ICM Data base used startdate and end date.
            SQL Filter: PROD  and  OwningTeamName = 'WASU'
    
    [2]  Get Tickets Effort time. Input tickets nums.
    
    [3]  Get Tickets Effort time. Input tickets start date and end date.
    
    [4]  Please input tickets nums Get ICM data.
    
    [5]  Query ICM Data base used startdate and end date(v5).
            SQL Filter: (PROD or Test) and  Operation  history users have wasu members.
                         and efforttime >0
    
    '''
    while 1:
        s0 = raw_input("Please Select the function  index num: 1 | 2 | 3 | 4 |5 \n num:")
        
        if s0 in ["1","2","3","4","5"]:
            break
        else:
            print "Input function  index num Error. Please retry !"
            continue
    
    return s0

def input_tickets():
    print "Please input tickets below, Enter will end:"
    sql_key =""
    while 1:
        line = raw_input()
        if line == "":
            print "Input end."
            break
        elif line.strip() =="":
            continue
        else:
            try:
                tm = int(line.strip())
                sql_key = "'" + line.strip() + "'," + sql_key 
            except Exception,e:
                print "input error: ",line.strip()
                continue
            
    return sql_key.strip(',')

def input_query_date():
    while 1:
        while 1:
            s0 = raw_input("Please input Query Start Date(CST) Ex:2016-09-24 \n Start Date:")
            try:
                startdate =datetime.strptime(s0, '%Y-%m-%d')
                break
            except:
                print "Input date like: 2016-01-05 !"
                continue
        while 1:
            s1 = raw_input("Please input Query End Date(CST) Ex:2016-10-01 \n End Date:")
            try:
                enddate =datetime.strptime(s1, '%Y-%m-%d')
                break
            except:
                print "Input date like: 2016-01-05 !"
                continue

        if (enddate-startdate).days >=0:
            break
        else:
            print "Please confirm your Input Enddate Gt StartDate! "
            continue

    # return start date and end date
    return s0,s1 

def input_name():
    name = raw_input("Please input Query Name(string.) Defualt: Null \n Name:")
    if name =="":
        m = hashlib.md5()
        s = datetime.strftime(datetime.now(), DATETIME_FMT)
        m.update(s)
        name = m.hexdigest()
    return name

def insert_mysql():
    name=""
    while 1:
        try:
            name = raw_input("Do you want insert query data in mysql?  Y/N  Defualt: Y \n Insert mysql:")
            name=name.lower()
            if name =="y" or name =="n":
                break
        except Exception,e:
            print e
    if name =="":
        name ="y"        
    return name

def input_main():
    
    s = menu_selec()
    name = input_name()
    mysqlflag =insert_mysql()
    
    if s =="1" or s =="3" or s=="5":
        r1,r2 = input_query_date()
        
        return r1,r2,name,s,mysqlflag
        
    elif s =="2" or s =="4":
        sql_key = input_tickets()
        
        return False,sql_key,name,s,mysqlflag

    
    
    
if __name__ == '__main__':
    
    print input_main()
    
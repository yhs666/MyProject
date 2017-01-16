#!/usr/bin/env python
#coding:utf-8
'''
Created on Nov 2, 2016

@author: yang.hongsheng
'''

import sys  
import MySQLdb
from datetime import datetime
from insert_logs import print_logs
import copy

DATETIME_FMT = '%Y-%m-%d %H:%M:%S'
time_out = 60
from config import config
config = config()


mysql_flag=1
try:
    mysqlconn=MySQLdb.connect(host=config['mysqldb']['host'],user=config['mysqldb']['username'],passwd=config['mysqldb']['password'],db=config['mysqldb']['db'],port=3306,charset='utf8')
    mysqlcur=mysqlconn.cursor()
except Exception,e:
    mysql_flag=0
    print "Mysql connect issue,sys exit!!",e
    print_logs(e)
    #sys.exit()
    
insert_issue=[]
def insert_tickets_icm_report(ticketsInfo,name):
    
    ticketsInfo_list=copy.deepcopy(ticketsInfo)
    
    updatetime = datetime.strftime(datetime.now(), DATETIME_FMT)
    if mysql_flag:
        for i in ticketsInfo_list:
            
            # unicde change to string
            for k in range(len(i)):
                if  i[k] is  None:
                    continue
                elif type(i[k]) is datetime:
                    i[k]= datetime.strftime(i[k],DATETIME_FMT)
                elif type(i[k]) is int:
                    i[k] = str(i[k])
                elif type(i[k]) is long:
                    i[k] = str(i[k])
                else:
                    i[k]=  i[k].encode("utf-8") 
            
            i.append(updatetime)
            
            # Insert mysql database
            # name,str(ID),str(IncidentSeverity),Title,str(EffortTime),SubType,EscalationOccured,Trigger,Source,AzureSource,CreatedDate,MitigatedDate,ResolvedDate,TicketState,SubStatus,OwningService,OwningTeam,ImpactedServices,ImpactedTeams,ImpactedComponent,ServiceResponsible,Keywords,CurrentSummary,updatetime

            # insert name
            i.insert(0,name)
            try:
                mysqlcur.execute('''insert into icm_report  values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', i)
                mysqlconn.commit()
                 
            except Exception,e:
                print "------------------------issue---------------------------------"
                msg = "Insert tickets to mysql  %s : %s issue!" %(i[1],e) 
                print_logs(msg)
                print "------------------------issue---------------------------------"
                insert_issue.append(i[1])
    else:
        print_logs("Mysql database connect issue. The Date not insert database.")
        insert_issue.append("Mysql Error!")
    
    return insert_issue

#insert effort time
def insert_tickets_effort(ticketsInfo,name):
    
    ticketsInfo_list=copy.deepcopy(ticketsInfo)
    
    updatetime = datetime.strftime(datetime.now(), DATETIME_FMT)
    if mysql_flag:
        for i in ticketsInfo_list:          
            i.append(updatetime)
            # insert name
            i.insert(0,name)
            # Insert mysql database
            ''''
            CREATE TABLE  `icm`.`icm_effort` (
            `name` VARCHAR( 30 ) NOT NULL ,
             `icm` int( 10 ) NOT NULL ,
             `changedate` DATETIME DEFAULT NULL ,
             `username` VARCHAR( 50 ) NOT NULL ,
             `effort` INT( 7 ) NOT NULL ,
             `updatetime` DATETIME DEFAULT NULL ,
            KEY  `icm` (  `icm` ) ,
            KEY  `username` (  `username` )
            ) ENGINE = INNODB DEFAULT CHARSET = utf8;
            '''
            
            try:
                mysqlcur.execute('''insert into icm_effort  values(%s,%s,%s,%s,%s,%s)''', i)
                mysqlconn.commit()
                 
            except Exception,e:
                print "------------------------issue---------------------------------"
                msg = "insert_tickets_effort-->Insert tickets to mysql  %s : %s issue!" %(i[1],e) 
                print_logs(msg)
                print "------------------------issue---------------------------------"
                insert_issue.append(i[1])
    else:
        print_logs("Mysql database connect issue. The Date not insert database.")
        insert_issue.append("Mysql Error!")
    
    return insert_issue


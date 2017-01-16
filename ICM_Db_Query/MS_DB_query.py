#!/usr/bin/env python
#coding:utf-8
'''
Created on Nov 2, 2016

@author: yang.hongsheng
'''
import _mssql
import os,pymssql
import logging
import sys  

from insert_logs import print_logs
#from get_users import get_users
from config import config

DATETIME_FMT = '%Y-%m-%d %H:%M:%S'
'''
server="suodk6gsjy.database.windows.net"
database="Azure-China-DataWarehouse"
user="nanboli@suodk6gsjy.database.windows.net"
password="oarnAlUzNblwkw13"
'''
config = config()
server= config['DataWarehouse']['host']
database=config['DataWarehouse']['db']
user=config['DataWarehouse']['username']
password=config['DataWarehouse']['password']

time_out = 60

# setting  logs
FILE=os.getcwd()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename = os.path.join(FILE,'MS_DB_query_log.txt'),
                    filemode='a')

# define connect MS SQL
try:
    conn=pymssql.connect(server,user,password,database=database)
    cursor=conn.cursor()
    print "Connect Warwhouse OK!"
    logging.info('Connect Warwhouse OK!')

except  Exception,e:
    print "Warwhouse connect issue!",e
    logging.info('Warwhouse connect issue!')
    sys.exit()

wasu_users="'oe-FanSongchen-china','oe-quanzhiyang-china','oe-yanghongsheng-china','oe-yangwenting-china','oe-yangfacai-china', \
            'oe-zhanglianhui-china','oe-luowei-china','oe-zoulili-china','oe-zhangyuan-china','oe-yuezhao-china', \
            'oe-jiangshixun-china', \
            'oe-lichuangcheng-china','oe-guofei-china','oe-kangkai-china'"

'''
###############Search service tickets changes

select * from  warehouseincidenthistory  where incidentid=24750236  and severity is not NULL order by changedate

'''
#----------------------  Search Tickets ------------------------------------------------- 
def  get_wasu_icm_tickets(startdate,enddate):
    '''
    Filter: PRD ENV
    If history have wasu tearm, Then return.
    '''
    try:
        #startdate,enddate,name = input_query_date()
        msg= "Start Query Db....."
        print msg
        logging.info(msg)
        SQlQuery ="select distinct   \
            a.incidentid,a.severity,a.title,a.keywords,a.status,dateadd(hour,8,a.createdate) as createdate, \
            dateadd(hour,8,a.resolvedate) as resolvedate,dateadd(hour,8,a.mitigatedate ) as mitigatedate , \
            a.IncidentSubType,a.owningtenantname,a.owningteamname,a.responsibletenantname,a.originatingtenantname \
            from  WarehouseIncidents  as a, WarehouseIncidentHistory as b  \
            where  b.incidentid = a.incidentid  and   \
            b.OwningTeamName = 'WINDOWSAZUREOPERATIONSCENTERCHINA\WASU'  and   \
            dateadd(hour,8,a.createdate) >=  '" + startdate  +  \
            "' and  dateadd(hour,8,a.createdate) < '" + enddate +  \
            "' and a.OccurringEnvironment = 'PROD'  \
            and  replace(a.owningteamname,'WINDOWSAZUREOPERATIONSCENTERCHINA','') <>'WALS' \
            and  a.incidenttype ='CustomerReported' \
            order by a.incidentid,a.title "
     
            
        cursor.execute(SQlQuery)
        ticketdata = cursor.fetchall()
    
        sql_key =""
        for i in ticketdata:
            sql_key = "'" + str(i[0])+ "'," + sql_key
            
        sql_key=sql_key.strip(',')
        
        #hash incident id for name       
        
        print_logs(" Query Db get_wasu_icm_tickets Done!")
            
        return ticketdata,sql_key
    except Exception,e:
        print "------------------------issue---------------------------------"
        msg = "get_wasu_icm_tickets  function issue : %s  " %(e) 
        print msg
        print "------------------------issue---------------------------------"
        logging.info(msg)
           
        return False,False


#----------------------  Search Tickets ------------------------------------------------- 
def  get_wasu_icm_ticketsv2(sql_key):
    '''
    Get tickets info From input tickets
    '''
    try:
        #startdate,enddate,name = input_query_date()
        msg= "Start Query Db....."
        print msg
        logging.info(msg)
        SQlQuery ="select distinct   \
            a.incidentid,a.severity,a.title,a.keywords,a.status,dateadd(hour,8,a.createdate) as createdate, \
            dateadd(hour,8,a.resolvedate) as resolvedate,dateadd(hour,8,a.mitigatedate ) as mitigatedate , \
            a.IncidentSubType,a.owningtenantname,a.owningteamname,a.responsibletenantname,a.originatingtenantname \
            from  WarehouseIncidents  as a \
            where  a.incidentid in (" + sql_key + ")  \
            order by a.incidentid "
     
            
        cursor.execute(SQlQuery)
        ticketdata = cursor.fetchall()
    
        sql_key =""
        for i in ticketdata:
            sql_key = "'" + str(i[0])+ "'," + sql_key
            
        sql_key=sql_key.strip(',')
        
        #hash incident id for name       
        
        print_logs(" Query Db get_wasu_icm_ticketsv2 Done!")
            
        return ticketdata
    except Exception,e:
        print "------------------------issue---------------------------------"
        msg = "get_wasu_icm_ticketsv2  function issue : %s  " %(e) 
        print msg
        print "------------------------issue---------------------------------"
        logging.info(msg)
           
        return False

def  get_wasu_icm_tickets_user(startdate,enddate):
    '''
     No have PRD ENV
     If tickets History have wasu users, Than return
    '''
    try:
        #startdate,enddate,name = input_query_date()
        
        msg= "Start Query Db....."
        print msg
        wasu_users = config['wasu-users']
        
        logging.info(msg)
        
        SQlQuery ="select distinct   \
            a.incidentid,a.severity,a.title,a.keywords,a.status,dateadd(hour,8,a.createdate) as createdate, \
            dateadd(hour,8,a.resolvedate) as resolvedate,dateadd(hour,8,a.mitigatedate ) as mitigatedate , \
            a.IncidentSubType,a.owningtenantname,a.owningteamname,a.responsibletenantname,a.originatingtenantname \
            from  WarehouseIncidents  as a, WarehouseIncidentHistory as b ,WarehouseIncidentCustomFieldEntries as c \
            where  b.incidentid = a.incidentid  and   \
            b.changedby in (" + wasu_users + ")  \
            and dateadd(hour,8,a.createdate) >=  '" + startdate  +  \
            "' and  dateadd(hour,8,a.createdate) < '" + enddate +  \
            "' and  replace(a.owningteamname,'WINDOWSAZUREOPERATIONSCENTERCHINA','') <>'WALS' \
            and a.incidentid = c.incidentid  \
            and  c.displayName='Ops Team Effort' \
            and ISNUMERIC(c.value) >0 \
            order by a.incidentid,a.title "
     
        #and  a.incidenttype ='CustomerReported' \  
        
        print  SQlQuery 
        cursor.execute(SQlQuery)
        ticketdata = cursor.fetchall()
        print ticketdata
        sql_key =""
        for i in ticketdata:
            sql_key = "'" + str(i[0])+ "'," + sql_key
            
        sql_key=sql_key.strip(',')
        
        #hash incident id for name       
        
        print_logs(" Query Db get_wasu_icm_tickets_user Done!")
            
        return ticketdata,sql_key
    except Exception,e:
        print "------------------------issue---------------------------------"
        msg = "get_wasu_icm_tickets_user  function issue : %s  " %(e) 
        print msg
        print "------------------------issue---------------------------------"
        logging.info(msg)
           
        return False,False
         
def get_icm_azure_info(sql_key):
    
    #   sql_key  '12345678','12345679' 
    #---------------------------- Azure summary-------------------------------------------
    try:
        SQlQuery=" select  incidentid, displayname, value \
                from dbo.WarehouseIncidentCustomFieldEntries  \
                where incidentid in (" + sql_key + ")  \
                order by incidentid "
        
        #print   SQlQuery      
        cursor.execute(SQlQuery)
        azure_table = cursor.fetchall()
    
        #---------------------------Impacted  Component--------------------------------------------
        
        SQlQuery="select incidentid, tenantName, Componentname \
                from dbo.WarehouseIncidentImpactedComponents \
                where istombstoned =0 and   incidentid in ( " + sql_key + ")  \
                order by incidentid "
        #print   SQlQuery        
        cursor.execute(SQlQuery)
        impacted_component_table = cursor.fetchall()
        
        #---------------------------Impacted Teams--------------------------------------------
        
        SQlQuery="select incidentid, teamName \
                from dbo.WarehouseIncidentImpactedTeams  \
                where   incidentid in ( " + sql_key + ")  \
                order by incidentid "
        #print   SQlQuery
        cursor.execute(SQlQuery)
        impacted_teams_table = cursor.fetchall()
        
        # ---------------- Impacted Services  -----------------------------
        SQlQuery="select incidentid, tenantName \
                from dbo.WarehouseIncidentImpactedTenants  \
                where   incidentid in ( " + sql_key + ")  \
                order by incidentid "
        #print   SQlQuery
        cursor.execute(SQlQuery)
        impacted_services_table = cursor.fetchall()
        print_logs("Db  get_icm_azure_info Done!")
        return azure_table,impacted_component_table,impacted_teams_table,impacted_services_table

    except Exception,e:
              
        print "------------------------issue---------------------------------"
        print_logs( "get_icm_azure_info  function issue : %s  " %(str(e))) 
        print "------------------------issue---------------------------------"
 
        return False,False,False,False


# Close Azure DB connect
def mssql_close():
    if conn:
        
        conn.close()
        

#select  a.incidentid,a.changedate,a.changedby, b.value  from  warehouseincidenthistory  as a, warehouseincidentcustomfieldhistory as b  where  b.incidenthistoryid = a.Historyid  and b.name='opsteameffort' and a.incidentid=25298502
def get_icm_efforttime(sql_key):
    try:
        SQlQuery="select a.incidentid,dateadd(hour,8,a.changedate) as changedate,a.changedby, b.value \
                from warehouseincidenthistory  as a, warehouseincidentcustomfieldhistory as b   \
                where   b.incidenthistoryid = a.Historyid  \
                and b.name='opsteameffort' \
                and a.incidentid in ( " + sql_key + ")  \
                order by a.incidentid,a.changedate"
        #print   SQlQuery
        cursor.execute(SQlQuery)
        efforttime_table = cursor.fetchall()
        
        return efforttime_table
    except Exception,e:
              
        print "------------------------issue---------------------------------"
        print_logs( "get_icm_efforttime  function issue : %s  " %(str(e))) 
        print "------------------------issue---------------------------------"
 
        return False

def get_icm_transfer_history(sql_key):
    # select  from  where incidentid=25298502   and  


    try:
        SQlQuery="select incidentid,changedate,changedby,changedescription,owningtenantname,owningTeamname  \
                from warehouseincidenthistory    \
                where     \
                owningteamname  IS NOT NULL \
                and incidentid in ( " + sql_key + ")  \
                order by incidentid,changedate "
        #print   SQlQuery
        cursor.execute(SQlQuery)
        transfer_history = cursor.fetchall()
        
        return transfer_history
    except Exception,e:
              
        print "------------------------issue---------------------------------"
        print_logs( "get_icm_transfer_history  function issue : %s  " %(str(e))) 
        print "------------------------issue---------------------------------"
 
        return False


if __name__ == '__main__':
    '''
    querydata,history_table,sql_key,name = get_wasu_icm_tickets()
    print sql_key
    azure_table,impacted_component_table,impacted_teams_table,impacted_services_table=get_icm_azure_info(sql_key)
    print history_table
    '''
    tickets,key = get_wasu_icm_tickets_user('2016-11-11','2016-11-30')
    
    print tickets
    print key
    mssql_close
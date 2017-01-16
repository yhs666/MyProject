#!/usr/bin/env python
#coding:utf-8
'''
Created on Oct 17, 2016

@author: yang.hongsheng
'''
import os,pymssql
import logging
import sys  
import MySQLdb
import hashlib
from datetime import datetime
reload(sys)  
sys.setdefaultencoding('utf8') 

DATETIME_FMT = '%Y-%m-%d %H:%M:%S'
server="suodk6gsjy.database.windows.net"
database="Azure-China-DataWarehouse"
user="nanboli@suodk6gsjy.database.windows.net"
password="oarnAlUzNblwkw13"
time_out = 60

# setting  logs
FILE=os.getcwd()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename = os.path.join(FILE,'ICM_Query.txt'),

                    filemode='w')

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

# define connect MYSQLicm
'''
try:
    mysqlconn=MySQLdb.connect(host='waps-20',user='icm',passwd='wasu@1234',db='icm',port=3306,charset='utf8')
    mysqlcur=mysqlconn.cursor()
except Exception,e:
    print "Mysql connect issue",e
    logging.info(e)
 '''   
try:
    mysqlconn=MySQLdb.connect(host='waps-20',user='wasu',passwd='www.wasu.com',db='wasu',port=3306,charset='utf8')
    mysqlcur=mysqlconn.cursor()
except Exception,e:
    print "Mysql connect issue",e
    logging.info(e)
#----------------------  Search Tickets -------------------------------------------------

startdate="2016-09-24"
enddate="2016-10-01"

# define name
name=""

inser_issue=[]

SQlQuery =" select distinct incidentid,severity,title,keywords,status,dateadd(hour,8,createdate) as createdate, \
         dateadd(hour,8,resolvedate) as resolvedate,dateadd(hour,8,mitigatedate ) as mitigatedate , \
         IncidentSubType,owningtenantname,owningteamname,responsibletenantname,originatingtenantname \
         from dbo.WarehouseIncidents  \
         where  dateadd(hour,8,createdate) >= '" + startdate  +  \
         "' and dateadd(hour,8,createdate) < '" + enddate +  \
         "'  and OccurringEnvironment = 'PROD' and \
         replace(owningteamname,'WINDOWSAZUREOPERATIONSCENTERCHINA','') <>'WALS' and \
         incidenttype ='CustomerReported'  \
         order by incidentid,title "
         
cursor.execute(SQlQuery)
querydata = cursor.fetchall()
'''
row=cursor.fetchone()  # 长链接查询
#for i in range(cur.rowcount):
#cur.fetchall() #短链接查询
while row:
    print row
    row=cursor.fetchone()
'''
#--------------------------confirm the tickets belongs wasu.---------------------------------------------
# confirm the tickets belongs wasu.

sql_key =""
for i in querydata:
    sql_key = "'" + str(i[0])+ "'," + sql_key
sql_key=sql_key.strip(',')

#print sql_key

SQlQuery  ="select distinct incidentid from dbo.WarehouseIncidentHistory \
            where incidentid in (" +  sql_key + ") \
            and OwningTeamName = 'WINDOWSAZUREOPERATIONSCENTERCHINA\\WASU'  \
            order by incidentid "

#print SQlQuery
cursor.execute(SQlQuery)
history_table = cursor.fetchall()

#--------------------------incidentid to sql_key---------------------------------------------

sql_key =""
for i in history_table:
    sql_key = "'" + str(i[0])+ "'," + sql_key
sql_key=sql_key.strip(',')

#hash incident id for name

if name =="":
    m = hashlib.md5()
    m.update(sql_key)
    name = m.hexdigest()

#---------------------------- Azure summary-------------------------------------------
#query azure summary, effort time, trigger,azure source, escalation status in  WarehouseIncidentCustomFieldEntries
#print sql_key

SQlQuery=" select  incidentid, displayname, value \
        from dbo.WarehouseIncidentCustomFieldEntries  \
        where incidentid in (" + sql_key + ")  \
        order by incidentid "

print   SQlQuery      
cursor.execute(SQlQuery)
azure_table = cursor.fetchall()

#---------------------------Impacted  Component--------------------------------------------

SQlQuery="select incidentid, tenantName, Componentname \
        from dbo.WarehouseIncidentImpactedComponents \
        where istombstoned =0 and   incidentid in ( " + sql_key + ")  \
        order by incidentid "
print   SQlQuery        
cursor.execute(SQlQuery)
impacted_component_table = cursor.fetchall()

#---------------------------Impacted Teams--------------------------------------------

SQlQuery="select incidentid, teamName \
        from dbo.WarehouseIncidentImpactedTeams  \
        where   incidentid in ( " + sql_key + ")  \
        order by incidentid "
print   SQlQuery
cursor.execute(SQlQuery)
impacted_teams_table = cursor.fetchall()

#---------------------------Summary tickets info--------------------------------------------

#format
# ID    IncidentSeverity    Title    Effort Time     SubType    EscalationOccured    Trigger    Source    
# Created Date    Mitigated Date    Resolved Date    Ticket State    Sub Status    Owning Service     
# Owning Team    Impacted Services    Impacted Teams    Impacted Component    Service Responsible    Keywords    Current Summary

# summary the tickets info
print  "ID    IncidentSeverity    Title    Effort Time    SubType    EscalationOccured    Trigger    Source    Created Date    Mitigated Date    Resolved Date    Ticket State    Sub Status    Owning Service     Owning Team    Impacted Services    Impacted Teams    Impacted Component    Service Responsible    Keywords    Current Summary"

for i in history_table:
    ID = i[0]
    #----------------search from incidents table => datatable
    for incident in querydata:
        if ID == incident[0]:
      
            IncidentSeverity = incident[1]
            Title = incident[2]
            SubType = incident[8]
            CreatedDate = incident[5]
            MitigatedDate = incident[7]
            ResolvedDate = incident[6]
            TicketState = incident[4]
            OwningService =incident[9]
            OwningTeam = incident[10]
            ServiceResponsible =incident[11]
            Keywords = incident[3]

            break
        
    #----------------search from azure table => azure_table
    sum_azure =0
    #$azure_key = New-Object -TypeName System.Collections.ArrayList

    SubStatus=""
    CurrentSummary=""
    EffortTime=""
    TriggerField=""
    EscalationOccured=""
    AzureSource=""

    for azure in azure_table:

        if ID == azure[0]:
            sum_azure = sum_azure + 1      
            displayname = azure[1]
            if displayname  == "Azure SubType":
                SubStatus=azure[2]
            elif displayname  == "Current Summary":
                CurrentSummary=azure[2]
            elif displayname == "Ops Team Effort":
                EffortTime=azure[2]
            elif displayname  == "Trigger Field":
                Trigger=azure[2]
            elif displayname  == "Escalation Status":
                EscalationOccured=azure[2]
            elif displayname  == "Azure Source":
                AzureSource=azure[2]
            
        if sum_azure > 25:
            break

    #----------------search from Impacted Component  table => $impacted_component_table-----------------------------
    ImpactedComponent=""
    for impacted in impacted_component_table:
        if ID == impacted[0]:
            ImpactedComponent=impacted[2]

    #----------------search from Impacted Teams  table => $impacted_teams_table-----------------------------
    ImpactedTeams=""
    for  azure in  impacted_teams_table:
        if ID == azure[0]:              
            ImpactedTeams=azure[1]

    # ----------------Not have Impacted Services  -----------------------------
    ImpactedServices =""
    
    # ----------------Define Source-----------------------------

    if AzureSource in ["CSS-ASMS"] :
        Source = "WASMS"
   
    elif  AzureSource  in ["CSS-IAAS Platform","CSS-Networking","CSS-IAAS Availability"] :
        Source = "WATS"
    elif AzureSource in ["CSS-SQL","CSS-Developer","CSS-WebApp"]:
        Source = "CIE"
    elif  AzureSource in ["CSS-Shanghai"]:
        Source = "CSS"
    elif AzureSource in ["Component Team","First Party"]:
        Source = "Component"
    else:
        Source = "other"

    # print the data

    print ID,IncidentSeverity,Title,EffortTime,SubType,EscalationOccured,Trigger,Source,CreatedDate,MitigatedDate,ResolvedDate,TicketState,SubStatus,OwningService,OwningTeam,ImpactedServices,ImpactedTeams,ImpactedComponent,ServiceResponsible,Keywords,CurrentSummary
    # date time
    
    #list_test =['ID','IncidentSeverity','Title','EffortTime','SubType','EscalationOccured','Trigger','Source','CreatedDate','MitigatedDate','ResolvedDate','TicketState','SubStatus','OwningService','OwningTeam','ImpactedServices','ImpactedTeams','ImpactedComponent','ServiceResponsible','Keywords','CurrentSummary']
    #for i in list_test:
    #    print i,type(eval(i))
    '''
    ID <type 'long'>
    IncidentSeverity <type 'int'>
    Title <type 'unicode'>
    EffortTime <type 'unicode'>
    SubType <type 'NoneType'>
    EscalationOccured <type 'str'>
    Trigger <type 'unicode'>
    Source <type 'str'>
    CreatedDate <type 'datetime.datetime'>
    MitigatedDate <type 'datetime.datetime'>
    ResolvedDate <type 'datetime.datetime'>
    TicketState <type 'unicode'>
    SubStatus <type 'unicode'>
    OwningService <type 'unicode'>
    OwningTeam <type 'unicode'>
    ImpactedServices <type 'str'>
    ImpactedTeams <type 'str'>
    ImpactedComponent <type 'str'>
    ServiceResponsible <type 'unicode'>
    Keywords <type 'unicode'>
    CurrentSummary <type 'unicode'>
    
    '''
    # unicde change to string
    list_unicde =['Title','EffortTime','SubType','EscalationOccured','Trigger','Source','TicketState','SubStatus','OwningService','OwningTeam','ImpactedServices','ImpactedTeams','ImpactedComponent','ServiceResponsible','Keywords','CurrentSummary']
    for i in list_unicde:
        #print i,type(eval(i))
        if  eval(i) is None:
            vars()[i]= ""
        else:
            vars()[i]=  eval(i).encode("utf-8")  
    
    updatetime = datetime.strftime(datetime.now(), DATETIME_FMT)
    
    print OwningTeam,ImpactedTeams
    
    # Insert mysql database
    id =None
    try:
        mysqlcur.execute('''insert into Report  values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (id,name,str(ID),str(IncidentSeverity),Title,str(EffortTime),SubType,EscalationOccured,Trigger,Source,AzureSource,datetime.strftime(CreatedDate, DATETIME_FMT),datetime.strftime(MitigatedDate,DATETIME_FMT),datetime.strftime(ResolvedDate,DATETIME_FMT),TicketState,SubStatus,OwningService,OwningTeam,ImpactedServices,ImpactedTeams,ImpactedComponent,ServiceResponsible,Keywords,CurrentSummary,updatetime))
        mysqlconn.commit()
         
    except Exception,e:
        msg = "Insert tickets  %s : %s issue!" %(str(ID),e) 
        print msg
        logging.info(msg)
        inser_issue.append(ID)

print inser_issue
mysqlcur.close()
conn.close()



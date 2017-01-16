#!/usr/bin/env python
#coding:utf-8
'''
Created on Nov 2, 2016

@author: yang.hongsheng
'''

from MS_DB_query import *
from insert_logs import print_logs
from datetime import datetime
from Insert_mysql import *
DATETIME_FMT = '%Y-%m-%d %H:%M:%S'

def get_icm_report_data(startdate,enddate):
    tickets_info =[]
    querydata,sql_key = get_wasu_icm_tickets(startdate,enddate)
    azure_table,impacted_component_table,impacted_teams_table,impacted_services_table=get_icm_azure_info(sql_key)
    mssql_close()
    #---------------------------Summary tickets info--------------------------------------------
    print  "ID    IncidentSeverity    Title    Effort Time    SubType    EscalationOccured    Trigger    Source  AzureSource  Created Date    Mitigated Date    Resolved Date    Ticket State    Sub Status    Owning Service     Owning Team    Impacted Services    Impacted Teams    Impacted Component    Service Responsible    Keywords    Current Summary"
    
    if querydata and azure_table:
        for incident in querydata:
            tickets=[]
            ID = incident[0]
            IncidentSeverity = incident[1]
            Title = incident[2]
            #SubStatus = incident[8]
            CreatedDate = incident[5]
            MitigatedDate = incident[7]
            ResolvedDate = incident[6]
            TicketState = incident[4]
            OwningService =incident[9]
            OwningTeam = incident[10]
            ServiceResponsible =incident[11]
            Keywords = incident[3]
            #----------------search from azure table => azure_table
            sum_azure =0
            #$azure_key = New-Object -TypeName System.Collections.ArrayList
            SubStatus=""
            SubType=""
            CurrentSummary=""
            EffortTime=""
            Trigger=""
            EscalationOccured=""
            AzureSource=""
        
            for azure in azure_table:
        
                if ID == azure[0]:
                    sum_azure = sum_azure + 1      
                    displayname = azure[1]
                    if displayname  == "Azure SubType":
                        SubType=azure[2]
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
                    elif displayname  == "Sub Status":
                        SubStatus=azure[2]
                if sum_azure > 25:
                    break
            #######deal owning team-------drop  "WINDOWSAZUREOPERATIONSCENTERCHINA\" -------------------    
            if "WINDOWSAZUREOPERATIONSCENTERCHINA\\" in OwningTeam :
                OwningTeam=OwningTeam.split("WINDOWSAZUREOPERATIONSCENTERCHINA\\")[1]
            #----------------search from Impacted Component  table => $impacted_component_table-----------------------------
            ImpactedComponent=""
            for impacted in impacted_component_table:
                if ID == impacted[0]:
                    ImpactedComponent=impacted[2]
                    break   
            #----------------search from Impacted Teams  table => $impacted_teams_table-----------------------------
            ImpactedTeams=""
            for  azure in  impacted_teams_table:
                if ID == azure[0]:              
                    ImpactedTeams=azure[1]
                    break
            # ----------------Not have Impacted Services  -----------------------------
            ImpactedServices =""
            for  azure in  impacted_services_table:
                if ID == azure[0]:              
                    ImpactedServices=azure[1]
                    break
                
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
            msg= ID,IncidentSeverity,Title,EffortTime,SubType,EscalationOccured,Trigger,Source,AzureSource,CreatedDate,MitigatedDate,ResolvedDate,TicketState,SubStatus,OwningService,OwningTeam,ImpactedServices,ImpactedTeams,ImpactedComponent,ServiceResponsible,Keywords,CurrentSummary
            print_logs(msg)
            tickets=[ID,IncidentSeverity,Title,EffortTime,SubType,EscalationOccured,Trigger,Source,AzureSource,CreatedDate,MitigatedDate,ResolvedDate,TicketState,SubStatus,OwningService,OwningTeam,ImpactedServices,ImpactedTeams,ImpactedComponent,ServiceResponsible,Keywords,CurrentSummary]
            tickets_info.append(tickets)
            
    return tickets_info

def get_icm_report_datav2(sql_key):
    tickets_info =[]
    querydata = get_wasu_icm_ticketsv2(sql_key)
    azure_table,impacted_component_table,impacted_teams_table,impacted_services_table=get_icm_azure_info(sql_key)
    mssql_close()
    #---------------------------Summary tickets info--------------------------------------------
    print  "ID    IncidentSeverity    Title    Effort Time    SubType    EscalationOccured    Trigger    Source  AzureSource  Created Date    Mitigated Date    Resolved Date    Ticket State    Sub Status    Owning Service     Owning Team    Impacted Services    Impacted Teams    Impacted Component    Service Responsible    Keywords    Current Summary"
    
    if querydata and azure_table:
        for incident in querydata:
            tickets=[]
            ID = incident[0]
            IncidentSeverity = incident[1]
            Title = incident[2]
            #SubStatus = incident[8]
            CreatedDate = incident[5]
            MitigatedDate = incident[7]
            ResolvedDate = incident[6]
            TicketState = incident[4]
            OwningService =incident[9]
            OwningTeam = incident[10]
            ServiceResponsible =incident[11]
            Keywords = incident[3]
            #----------------search from azure table => azure_table
            sum_azure =0
            #$azure_key = New-Object -TypeName System.Collections.ArrayList
            SubStatus=""
            SubType=""
            CurrentSummary=""
            EffortTime=""
            Trigger=""
            EscalationOccured=""
            AzureSource=""
        
            for azure in azure_table:
        
                if ID == azure[0]:
                    sum_azure = sum_azure + 1      
                    displayname = azure[1]
                    if displayname  == "Azure SubType":
                        SubType=azure[2]
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
                    elif displayname  == "Sub Status":
                        SubStatus=azure[2]
                if sum_azure > 25:
                    break
            #######deal owning team-------drop  "WINDOWSAZUREOPERATIONSCENTERCHINA\" -------------------    
            if "WINDOWSAZUREOPERATIONSCENTERCHINA\\" in OwningTeam :
                OwningTeam=OwningTeam.split("WINDOWSAZUREOPERATIONSCENTERCHINA\\")[1]
            #----------------search from Impacted Component  table => $impacted_component_table-----------------------------
            ImpactedComponent=""
            for impacted in impacted_component_table:
                if ID == impacted[0]:
                    ImpactedComponent=impacted[2]
                    break   
            #----------------search from Impacted Teams  table => $impacted_teams_table-----------------------------
            ImpactedTeams=""
            for  azure in  impacted_teams_table:
                if ID == azure[0]:              
                    ImpactedTeams=azure[1]
                    break
            # ----------------Not have Impacted Services  -----------------------------
            ImpactedServices =""
            for  azure in  impacted_services_table:
                if ID == azure[0]:              
                    ImpactedServices=azure[1]
                    break
                
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
            msg= ID,IncidentSeverity,Title,EffortTime,SubType,EscalationOccured,Trigger,Source,AzureSource,CreatedDate,MitigatedDate,ResolvedDate,TicketState,SubStatus,OwningService,OwningTeam,ImpactedServices,ImpactedTeams,ImpactedComponent,ServiceResponsible,Keywords,CurrentSummary
            print_logs(msg)
            tickets=[ID,IncidentSeverity,Title,EffortTime,SubType,EscalationOccured,Trigger,Source,AzureSource,CreatedDate,MitigatedDate,ResolvedDate,TicketState,SubStatus,OwningService,OwningTeam,ImpactedServices,ImpactedTeams,ImpactedComponent,ServiceResponsible,Keywords,CurrentSummary]
            tickets_info.append(tickets)
            
    return tickets_info

def get_icm_report_datav5(startdate,enddate):
    tickets_info =[]
    querydata,sql_key = get_wasu_icm_tickets_user(startdate,enddate)
    
    print "datetime:",startdate,enddate
    print querydata
    azure_table,impacted_component_table,impacted_teams_table,impacted_services_table=get_icm_azure_info(sql_key)
    mssql_close()
    #---------------------------Summary tickets info--------------------------------------------
    print  "ID    IncidentSeverity    Title    Effort Time    SubType    EscalationOccured    Trigger    Source  AzureSource  Created Date    Mitigated Date    Resolved Date    Ticket State    Sub Status    Owning Service     Owning Team    Impacted Services    Impacted Teams    Impacted Component    Service Responsible    Keywords    Current Summary"
    
    if querydata and azure_table:
        for incident in querydata:
            tickets=[]
            ID = incident[0]
            IncidentSeverity = incident[1]
            Title = incident[2]
            #SubStatus = incident[8]
            CreatedDate = incident[5]
            MitigatedDate = incident[7]
            ResolvedDate = incident[6]
            TicketState = incident[4]
            OwningService =incident[9]
            OwningTeam = incident[10]
            ServiceResponsible =incident[11]
            Keywords = incident[3]
            #----------------search from azure table => azure_table
            sum_azure =0
            #$azure_key = New-Object -TypeName System.Collections.ArrayList
            SubStatus=""
            SubType=""
            CurrentSummary=""
            EffortTime=""
            Trigger=""
            EscalationOccured=""
            AzureSource=""
        
            for azure in azure_table:
        
                if ID == azure[0]:
                    sum_azure = sum_azure + 1      
                    displayname = azure[1]
                    if displayname  == "Azure SubType":
                        SubType=azure[2]
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
                    elif displayname  == "Sub Status":
                        SubStatus=azure[2]
                if sum_azure > 25:
                    break
            #######deal owning team-------drop  "WINDOWSAZUREOPERATIONSCENTERCHINA\" -------------------    
            if "WINDOWSAZUREOPERATIONSCENTERCHINA\\" in OwningTeam :
                OwningTeam=OwningTeam.split("WINDOWSAZUREOPERATIONSCENTERCHINA\\")[1]
            #----------------search from Impacted Component  table => $impacted_component_table-----------------------------
            ImpactedComponent=""
            for impacted in impacted_component_table:
                if ID == impacted[0]:
                    ImpactedComponent=impacted[2]
                    break   
            #----------------search from Impacted Teams  table => $impacted_teams_table-----------------------------
            ImpactedTeams=""
            for  azure in  impacted_teams_table:
                if ID == azure[0]:              
                    ImpactedTeams=azure[1]
                    break
            # ----------------Not have Impacted Services  -----------------------------
            ImpactedServices =""
            for  azure in  impacted_services_table:
                if ID == azure[0]:              
                    ImpactedServices=azure[1]
                    break
                
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
            msg= ID,IncidentSeverity,Title,EffortTime,SubType,EscalationOccured,Trigger,Source,AzureSource,CreatedDate,MitigatedDate,ResolvedDate,TicketState,SubStatus,OwningService,OwningTeam,ImpactedServices,ImpactedTeams,ImpactedComponent,ServiceResponsible,Keywords,CurrentSummary
            print_logs(msg)
            tickets=[ID,IncidentSeverity,Title,EffortTime,SubType,EscalationOccured,Trigger,Source,AzureSource,CreatedDate,MitigatedDate,ResolvedDate,TicketState,SubStatus,OwningService,OwningTeam,ImpactedServices,ImpactedTeams,ImpactedComponent,ServiceResponsible,Keywords,CurrentSummary]
            tickets_info.append(tickets)
            
    return tickets_info


def get_icm_efforttime_data(**kargs):
    "ex: (startdate=2016-10-20,enddate=2016-11-03) or (sql_key ='20168725','2012655') "
    
    #####################判断 参数--------------------
    keys = kargs.keys()
    efforttime_info =[]
    if len(keys) >2:
        print_logs("kargs only support startdate enddate or sql_key")
        return efforttime_info
    elif "startdate" in keys and "enddate" in keys:
        flag =2
    elif  "sql_key" in keys:
        flag=1
    else:
        print_logs("kargs only support startdate enddate or sql_key")
        return efforttime_info
    
    ###################get sql_key####################
    if flag ==2:    
        querydata,sql_key = get_wasu_icm_tickets(kargs['startdate'],kargs['enddate'])
        #mssql_close()
    if flag ==1:
        sql_key = kargs['sql_key']
    
    #search MS DB
    efforttime = get_icm_efforttime(sql_key) 
    mssql_close()
    
    if efforttime:
        efforttime_len = len(efforttime)
        for i in range(0,efforttime_len):
            #efforttime[i]=list(efforttime[i])
            tmp_list=[]
            #print efforttime[i]
            if i >0 and  efforttime[i][0]== efforttime[i-1][0]:
                efforttime_tmp=int(efforttime[i][3])- int(efforttime[i-1][3])
            else:
                efforttime_tmp=int(efforttime[i][3])
                
            #转换日期为字符串
            efforttime_date = datetime.strftime(efforttime[i][1], DATETIME_FMT)
            tmp_list=[int(efforttime[i][0]),efforttime_date,efforttime[i][2],efforttime_tmp] 
            #print  efforttime[i]
            efforttime_info.append(tmp_list)
    
    return    efforttime_info   

  
                    
                    
if __name__ == '__main__':
    '''          
    data = get_icm_efforttime_data(sql_key="'24985929','24985929','24985929'")
    print data
    print insert_tickets_effort(data,"summaryQuery modle")   
    for i in data:
        print i
    '''
    x,y = get_wasu_icm_tickets_user('2016-10-01',"2016-10-20")
    print x
    print '#'*50
    print y
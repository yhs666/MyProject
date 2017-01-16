#!/usr/bin/env python
#coding:utf-8
'''
Created on Dec 16, 2015

@author: yang.hongsheng
'''
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import redis
import logging
import sys
import lxml.html
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
from selenium.webdriver.support.select import Select
from datetime import datetime

import crypto
import sys
sys.modules['Crypto'] = crypto

from crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

ip ="172.31.4.119"
redispassword = "wasu.com"
time_out = 60

FILE=os.getcwd()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename = os.path.join(FILE,'Get_ICM_date_log.txt'),
                    filemode='w')
try:
    myredis = redis.Redis(host=ip,password=redispassword,port = 6379)
    print "Connect Redis OK!"
    logging.info('Connect Redis OK!')

except:
    print "Redis connect issue!"
    logging.info('Redis connect issue!')
    sys.exit()

keyword=[
        'IncidentSeverity',
        'Title',
        'Effort Time',
        'SubType',
        'EscalationOccured',
        'Trigger',
        'Azure Source',
        'Created Date',
        'Mitigated Date',
        'Resolved Date',
        'Ticket State',
        'Sub Status',
        'Owning Service',
        'Owning Team',
        'Impacted Services',
        'Impacted Teams',
        'Impacted Component',
        'Service Responsible',
        'Keywords',
        'Current Summary',
        'updatetime',
         ]
redis_key=[
        'Severity:',
        'Title:',
        'Ops Team Effort:',
        'Azure SubType:',
        'Escalation Status:',
        'Trigger Field:',
        'Azure Source:',
        'Created Date',
        'Time Mitigated (CST):',
        'Time Resolved (CST):',
        'Ticket State',
        'Sub Status:',
        'Owning Service:',
        'Owning Team:',
        'Impacted Services:',
        'Impacted Teams:',
        'Impacted Component:',
        'Service Responsible:',
        'Keywords:',
        'Current Summary:',
        'updatetime'
           ]


DATETIME_FMT = '%Y-%m-%d %H:%M:%S'

datetimenow=datetime.strftime(datetime.now(), DATETIME_FMT)

def new_table(url):
    #main_window =driver.current_window_handle
    try:
        script_url= "window.open('%s','_blank');" % url
        driver.execute_script(script_url)
        driver.find_element_by_tag_name('body')
    except Exception,e:
        print e    

def get_icm_details(page_source):
    try:
        page_source=page_source.encode('utf-8','ignore')
        root = lxml.html.fromstring(page_source)
        icmdetail=[]
        icmazure=[]
        for row in root.xpath('.//table[@id="ctl00_MainContent_TabContainer_TabDetails_IncidentDetailsView"]//tr'):     
            icmdetail.append(row.xpath('.//td/text()'))
            icmazure.append(row.xpath('.//td/div//text()'))

        icmdetail_key=[2,3,4,5,6,7,8,9,13,14,15,16]
        icm_keyword={}
        for i in icmdetail_key:
            hang = icmdetail[i]
            if len(hang) % 2 != 0:
                hang.append('')
            j=0
            while j < len(hang)-1:
                hang_key = hang[j].strip()
                if hang_key == "" or ':' != hang_key[-1]:
                    j=j+1
                    continue      
                hang_value= hang[j+1].strip()
                if  hang_value != "" and  ':' == hang_value[-1]:
                    hang_value=''
                    j=j+1
                else:
                    j=j+2
                
                #print i,j,hang_key,hang_value
                icm_keyword[hang_key]=hang_value
        
        icm_keyword[icmdetail[17][0]] =icmdetail[17][2].strip()
        #print icm_keyword[icmdetail[17][0]]
        icmazure_key=[]
        icmazure_value=[]
        end =len(icmdetail)-1
        begin = end -7
        for i in range(begin,end):
            hang = icmdetail[i]
            for j in hang:
                if j.strip() != "":
                    icmazure_key.append(j.strip())
        for i in range(begin,end):
            hang = icmazure[i]
            if i == end -1 :
                icmazure_value.append(hang[0].strip())
            else:
                for j in range(0,len(hang),2):
                    icmazure_value.append(hang[j].strip())
        #print icmazure_key
        #print icmazure_value
        if len(icmazure_key) == len(icmazure_value):
            for i in range(0,len(icmazure_key)):
                
                icm_keyword[icmazure_key[i]]=icmazure_value[i].encode('utf-8','ignore')
            
            # tilte and summary not error code
            icm_keyword["Title:"]= driver.find_element_by_id("ctl00_MainContent_IncidentTitleHeader").text
            icm_keyword["Current Summary:"]= driver.find_elements_by_xpath("//*[@id='bigStringTextDiv']")[-1].text
            
            icm_keyword["Owning Team:"] =driver.find_element_by_xpath("/html/body/form/div[3]/div[2]/div[2]/div[2]/div[2]/div[1]/div/table/tbody/tr/td/table/tbody/tr[3]/td[4]").text
            icm_keyword["Impacted Services:"] =driver.find_element_by_xpath("/html/body/form/div[3]/div[2]/div[2]/div[2]/div[2]/div[1]/div/table/tbody/tr/td/table/tbody/tr[4]/td[2]").text
            icm_keyword["Impacted Teams:"] =driver.find_element_by_xpath("/html/body/form/div[3]/div[2]/div[2]/div[2]/div[2]/div[1]/div/table/tbody/tr/td/table/tbody/tr[4]/td[4]").text
            icm_keyword["Impacted Component:"] =driver.find_element_by_xpath("/html/body/form/div[3]/div[2]/div[2]/div[2]/div[2]/div[1]/div/table/tbody/tr/td/table/tbody/tr[4]/td[6]").text
            icm_keyword["Service Responsible:"] =driver.find_element_by_xpath("/html/body/form/div[3]/div[2]/div[2]/div[2]/div[2]/div[1]/div/table/tbody/tr/td/table/tbody/tr[5]/td[2]").text
            
            
            return icm_keyword
        else:
            print "ICM Azure part have issue or changed!"
            logging.info("ICM Azure part have issue or changed!")
            return False
    except Exception , e:
        msg = "get_icm_details: issue.  " + e
        print msg
        logging.info(msg)
        return False

def get_icm_history(page_source):
    try:
        icmhistory=[] 
        page_source=page_source.encode('utf-8','ignore')   
        root = lxml.html.fromstring(page_source)
        for row in root.xpath('.//table[@id="HistoryDisplayGrid"]//tr'):
            icmhistory.append(row.xpath('.//td/text()'))
            
        icm_history=[]
        
        for i in icmhistory:
            temp=[]
            t={}
            if i ==[]:
                continue
            for j in range(0,len(i)):
                if j <3:
                    temp.append(i[j])
                else:
                    k = i[j].split('[')
                    l = i[j].split(':')
                    if len(l) !=2 and len(k) ==1:
                        t[i[j]] =""
                    elif len(k)==2:
                        h_key =k[0].split("'")[1]
                        h_val = k[1].split("]")[0]
                        t[h_key]=h_val
                    elif len(l) ==2:
                        h_key =l[0].replace("'","")
                        h_val = l[1]
                        t[h_key]=h_val                
                    else:
                        h_key =k[1].split("]")[0]
                        h_val = k[2].split("]")[0]
                        t[h_key]=h_val
            temp.append(t)
            icm_history.append(temp)
        
        return icm_history
    except Exception , e:
        print "get_icm_history",e
        return False 
def login():    
#def login(username,password):
    try:
        elem = driver.find_element_by_id("userNameInput")
        elem.clear()
        elem.send_keys(username)
        elem = driver.find_element_by_id("passwordInput")
        elem.clear()
        elem.send_keys(password)
        time.sleep(1)
        elem = driver.find_element_by_id("submitButton")
        elem.click()
        return True 
    except Exception, e:
        print "login: Not found login!",e
        return False
    
def icm_login(url,n= None):
    try:
        if n == 1:
            #login(username, password)
            login() 
            print "ICM_login:  OK!"
            return driver.current_window_handle
        else:
            return new_table(url)
            print "ICM_login: new table"
    except Exception, e:
        return False
        print "ICM_login:  ISSUE !",e

def set_redis(key,vaule):
    try:
        myredis.set(key,json.dumps(vaule))
    except Exception, e:
        print e
        myredis.set(key,json.dumps(vaule,ensure_ascii=False))
        
def deal_icm(hands,detailorhistory='ALL'):
    '''
    detail or histroy ==[detail,history,ALl]
    '''
    #get icm details
    for i in hands:
        
        try:
            driver.switch_to_window(i)
            driver.implicitly_wait(60)
            if detailorhistory =='detail' or detailorhistory=='ALL':
                icmNo = driver.current_url[-8:]
                icmdet = get_icm_details(driver.page_source)
                icmdet['updatetime']= datetime.strftime(datetime.now(), DATETIME_FMT)
                icmdet['Created Date']=driver.find_element_by_id("ctl00_MainContent_CreatedDateLabel").text
                tm=driver.find_element_by_id("ctl00_MainContent_SeverityLabel").text
                icmdet['Ticket State']=tm.split('-')[1].strip()
                print icmNo,icmdet
                key= icmNo + ":detail"
                set_redis(key,icmdet)
                # write status
                key2 =icmNo + ":detail:status"
                myredis.set(key2,"ok")
                #msg = icmNo +" :Details: " + icmdet
                #logging.info(msg)
            #click history

        except Exception, e:
            icmNo = driver.current_url[-8:]
            msg = icmNo + ' Get Details Have issue!!',e
            print  time.ctime(),msg 
            logging.info(msg)
            key2 =icmNo + ":detail:status"
            myredis.set(key2,"issue")
            
    if detailorhistory=='ALL' or detailorhistory=='history':
        for i in hands:
            driver.switch_to_window(i)
            driver.implicitly_wait(5)
            history =driver.find_element_by_id("__tab_ctl00_MainContent_TabContainer_TabHistory")
            history.click()
    #deal history
    if detailorhistory=='ALL'  or detailorhistory=='history':
        for i in hands:
            try: 
                driver.switch_to_window(i)
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "HistoryDisplayGrid")))
                driver.implicitly_wait(60)
                icmNo = driver.current_url[-8:]
                icm_history_list = get_icm_history(driver.page_source)
                icm_history_list.append(datetime.strftime(datetime.now(), DATETIME_FMT))
                #print icmNo,icm_history_list
                key= icmNo + ":history"
                myredis.set(key,json.dumps(icm_history_list,ensure_ascii=False))
                # write status
                key2 =icmNo + ":history:status"
                myredis.set(key2,"ok")
                
                #msg = icmNo +":history:" +icm_history_list
                #logging.info(msg)
                
            except Exception, e:
                icmNo = driver.current_url[-8:]
                msg = icmNo + ' Get History Have issue!!',e
                print  time.ctime(),msg 
                logging.info(msg)
                key2 =icmNo + " :detail :status"
                myredis.set(key2,"issue")
    '''
    for i in hands:
        driver.switch_to_window(i)
        driver.close()           
    ''' 
class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC
     
    #解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')
           
def get_pwd():
    get_encry =myredis.get("cmepwd")
    pc = prpcrypt('wasuwasuwasuwasu') 
    return  pc.decrypt(get_encry)     


# 初始化ICM 
def init_icm():
    try:
        global username
        username = "cme\oe-yanghongsheng"
        global password 
        password = get_pwd()
        
        global driver
        # define ENV
        url="https://icm.ad.msft.net/imp/v3/incidents/search/basic"
        #iedriver = "C:\Users\yang.hongsheng\Desktop\IEDriverServer\IEDriverServer32.exe"
        iedriver = ".\\IEDriverServer\\IEDriverServer32.exe"
        os.environ["webdriver.ie.driver"] = iedriver
        driver = webdriver.Ie(iedriver) 
        #login icm
        driver.get(url)
        #login_icm_handle = icm_login(url, n=1)
        login()
        global login_icm_handle
        login_icm_handle=driver.current_window_handle
        driver.implicitly_wait(30)
        cookie = driver.get_cookies()
        driver.add_cookie(cookie[0]) 
        
           
    except Exception,e:
        print "icm init err: ",str(e)
        logging.info("icm init error! exit.") 
        sys.exit()

def get_icm_data(tickets_list,get_type):
    # default ALL, select detail or history
    #并发数
    bing = 10
    #get icm detail or history
    q= tickets_list
    for i in range(0,len(q),bing):
        end=len(q)-i  
        if end > bing:
            end=bing
        for  j in range(0,end):
            url = "https://icm.ad.msft.net/imp/IncidentDetails.aspx?id=" + q[j+i]
            new_table(url)
            time.sleep(2)
    
        hands = driver.window_handles
        hands.remove(login_icm_handle)
        # default ALL, select details or history
        deal_icm(hands,get_type)
        driver.switch_to_window(login_icm_handle)    
        #get icm date over.
    print "************************Get icm data  Done************************************"
    msg = ' Get ICM Date  Run over!!'
    print  time.ctime(),msg 
    logging.info(msg)


def check_login():
    try:
        driver.implicitly_wait(3)
        WebDriverWait(driver, 3).until(lambda x : x.find_element_by_id("submitButton"))
        #driver.find_element_by_id("submitButton")
        #driver.switch_to_window(login_icm_handle)
        driver.implicitly_wait(30)
        login()
        msg = "Check icm login Need re login!"
        print msg
        logging.info(msg) 
    except Exception,e:
        driver.implicitly_wait(30)
        msg = "Check icm login didn't Need re login!"
        print msg
        logging.info(msg) 
    

def get_icm_datav2(tickets_list):
    #并发数
    bing = 10
    #get icm detail or history
    q= tickets_list
    for i in range(0,len(q),bing):
        end=len(q)-i  
        if end > bing:
            end=bing
        for  j in range(0,end):
            url = "https://icm.ad.msft.net/imp/IncidentDetails.aspx?id=" + q[j+i]
            new_table(url)
            time.sleep(2)
    
        hands = driver.window_handles
        hands.remove(login_icm_handle)
        # default ALL, select details or history
        deal_icm(hands,"detail")
        
        
        for tickets_hand in hands:
            driver.switch_to_window(tickets_hand)
            driver.implicitly_wait(60)
            icmNo= driver.current_url[-8:]
            
            key = icmNo +":detail"
            ticket_info = json.loads(myredis.get(key))
            if  ticket_info["Public Postmortem Needed:"] !="Standard RCA":
                print "Public Postmortem Needed:", icmNo,"Changed."
                
                #Edit incident
                history =driver.find_element_by_id("ctl00_MainContent_TabContainer_TabDetails_IncidentDetailsView_IncidentEditTop")
                history.click()
                time.sleep(5)
                driver.implicitly_wait(60)
                
                #search  id='ValueEnum'
                ids =  driver.find_elements_by_xpath("//*[@id='ValueEnum']")
                
                # Public Postmortem Needed: ids[5]
                '''
                Public Postmortem Needed:
                <select name="ctl00$MainContent$TabContainer$TabDetails$IncidentDetailsView$CustomFieldGroups$ctl00$CustomFieldsBlock$ctl13$ValueEnum" id="ValueEnum" style="width: 75%;">
                    <option value="">(Select)</option>
                    <option selected="selected" value="7">Not Required</option>
                    <option value="5">Post Mortem</option>
                    <option value="4">Standard RCA</option>
                    <option value="6">Unknown</option>
                '''

                select=Select(ids[5])
                #print dir(select)
                select.select_by_value("7")  #change to Not Required
                #select.select_by_index(7)
                
                # find save butten
                driver.find_element_by_id("ctl00_MainContent_TabContainer_TabDetails_IncidentDetailsView_DetailsUpdateBottom").click()
                time.sleep(5)
                driver.implicitly_wait(60)
                driver.close()          
            else:
                driver.switch_to_window(tickets_hand)
                driver.close() 
            
            
        driver.switch_to_window(login_icm_handle)    
        #get icm date over.
    print "************************Get icm data  Done************************************"
    msg = ' Get ICM Date  Run over!!'
    print  time.ctime(),msg 
    logging.info(msg)
    
    
    
    
        
   
if __name__=='__main__':

    # init icm
    init_icm()

    ticket_list = ['25694984']
    #并发数
    bing = 10
    #get icm detail or history

    for i in range(0,len(ticket_list),bing):
        end=len(ticket_list)-i  
        if end > bing:
            end=bing
        for  j in range(0,end):
            url = "https://icm.ad.msft.net/imp/IncidentDetails.aspx?id=" + ticket_list[j+i]
            new_table(url)
            time.sleep(2)
    
        hands = driver.window_handles
        hands.remove(login_icm_handle)
        # default ALL, select details or history
        deal_icm(hands,"detail")
        
        
        for tickets_hand in hands:
            driver.switch_to_window(tickets_hand)
            driver.implicitly_wait(60)
            icmNo= driver.current_url[-8:]
            
            key = icmNo +":detail"
            ticket_info = json.loads(myredis.get(key))
            if  ticket_info["Public Postmortem Needed:"] !="Standard RCA":
                print "Public Postmortem Needed:", icmNo,"Changed."
                
                #Edit incident
                history =driver.find_element_by_id("ctl00_MainContent_TabContainer_TabDetails_IncidentDetailsView_IncidentEditTop")
                history.click()
                time.sleep(5)
                driver.implicitly_wait(60)
                
                #search  id='ValueEnum'
                ids =  driver.find_elements_by_xpath("//*[@id='ValueEnum']")
                
                # Public Postmortem Needed: ids[5]
                '''
                Public Postmortem Needed:
                <select name="ctl00$MainContent$TabContainer$TabDetails$IncidentDetailsView$CustomFieldGroups$ctl00$CustomFieldsBlock$ctl13$ValueEnum" id="ValueEnum" style="width: 75%;">
                    <option value="">(Select)</option>
                    <option selected="selected" value="7">Not Required</option>
                    <option value="5">Post Mortem</option>
                    <option value="4">Standard RCA</option>
                    <option value="6">Unknown</option>
                '''

                select=Select(ids[5])
                #print dir(select)
                select.select_by_value("7")  #change to Not Required
                #select.select_by_index(7)
                
                # find save butten
                driver.find_element_by_id("ctl00_MainContent_TabContainer_TabDetails_IncidentDetailsView_DetailsUpdateBottom").click()
                time.sleep(5)
                driver.implicitly_wait(60)
                driver.close()          
            else:
                driver.switch_to_window(tickets_hand)
                driver.close() 
            
            
        driver.switch_to_window(login_icm_handle)    
        #get icm date over.
    print "************************Get icm data  Done************************************"
    msg = ' Get ICM Date  Run over!!'
    print  time.ctime(),msg 
    logging.info(msg)


    #end
    driver.quit()
    print "Done!!!!!!!!!"
    sys.exit()

    
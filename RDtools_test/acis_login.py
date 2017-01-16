#!/usr/bin/env python
#coding:utf-8
'''
Created on Dec 16, 2015

@author: yang.hongsheng
'''
from distutils import fancy_getopt

username = "cme\oe-yanghongsheng"
password = "zxcvbnmasdfghjkl1@"
pin ="cmehongsheng"
cert_number= 4


import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from autopy import key
import win32gui
import autopy
import win32api,win32con,win32gui,time
from win32file import INVALID_HANDLE_VALUE 


#assert "Python" in driver.title
#elem = driver.find_element_by_name("MC-ADFS-Federation")
def mc_adfs():
    
    try:
        driver.implicitly_wait(5)
        elem = driver.find_element_by_name("MC-ADFS-Federation")
        #elem = driver.find_element_by_tag_name("button")
        elem.click()
        return 
    except Exception, e:
        print e    
        print "mc_adfs: Can not found MC-ADFS-Federation"
        return False


#cme user login input
def login(username,password):
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
        print "login: Not found login!"
        return False


def cert_check(cert_number):
    time.sleep(2)
    windows_name = "Windows Security"
    hn=win32gui.FindWindow(None, windows_name)
    if hn != INVALID_HANDLE_VALUE:
        win32gui.ShowWindow(hn,1)   
        win32gui.SetForegroundWindow(hn)
        for i in range(1,cert_number):
            #send key  down
            win32api.keybd_event(40,0,0,0)
            win32api.keybd_event(40,0,win32con.KEYEVENTF_KEYUP,0)

        #send key  enter
        win32api.keybd_event(13,0,0,0)
        win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
        print "cert_check: Select cert ok"
        return True
    else:
        print "cert_check: Select cert issue!"
        return False

def input_pin(pin):
    pin_name ="Verify User PIN"
    time.sleep(2)
    hn=win32gui.FindWindow(None, pin_name)
    if hn != INVALID_HANDLE_VALUE: 
        hn2=win32gui.FindWindowEx(hn,None,'Edit',None)
        win32gui.ShowWindow(hn2,1)   
        win32gui.SetForegroundWindow(hn2)
        key.type_string(pin,120)
        time.sleep(1)
        #enter
        win32gui.PostMessage(hn2, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)  
        win32gui.PostMessage(hn2, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
        
        return True
    else:
        
        print "input_pin: Input user pin issue! "
        return False

def new_table(url):
    #main_window =driver.current_window_handle
    script_url= "window.open('%s','_blank');" % url
    driver.execute_script(script_url)
    driver.find_element_by_tag_name('body')
    hands = driver.window_handles
    driver.implicitly_wait(5)
    mc_adfs()
    if len(hands) >1 :
        driver.switch_to_window(driver.window_handles[1])
        return driver.current_window_handle
        print "new_table:successfull change the windows hands"
    else:
        print "new_table:Please check Ie setting"
        return False 


def ACIS_login(url,n= None):
    try:
        if n == 1:
            #driver.get(url)
            mc_adfs() 
            login(username, password) 
            cert_check(cert_number)
            input_pin(pin)
            print "ACIS_login: login OK!"
            return driver.current_window_handle
        else:
            return new_table(url)
            print "ACIS_login: new table"
    except Exception, e:
        return False
        print "ACIS_login:  ISSUE blow!"
        print e
    




if __name__=='__main__':
    url="https://acis.engineering.core.chinacloudapi.cn/"

    iedriver = "C:\Program Files\Internet Explorer\IEDriverServer.exe"
    os.environ["webdriver.ie.driver"] = iedriver
    driver = webdriver.Ie(iedriver)
    driver.get(url)
    #global driver
    ACIS_login(url, n=1) 
    time.sleep(5)
    
    ACIS_login(url)
    time.sleep(10)
    print "OK"
    #driver.close()
    #driver.quit()
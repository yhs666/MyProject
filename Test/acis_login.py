#!/usr/bin/env python
#coding:utf-8
'''
Created on Dec 12, 2015

@author: yang.hongsheng
'''


import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from autopy import key
import win32gui
import autopy

username ="cme\oe-yanghongsheng"
password ="asdfghjklzxcvbnm1@"
pin="cmehongsheng"

#selenium  webdriver
iedriver = "C:\Program Files\Internet Explorer\IEDriverServer.exe"

os.environ["webdriver.ie.driver"] = iedriver
driver = webdriver.Ie(iedriver)
url="https://acis.engineering.core.chinacloudapi.cn/"

driver.get(url)
#assert "Python" in driver.title


#elem = driver.find_element_by_name("MC-ADFS-Federation")
elem = driver.find_element_by_tag_name("button")
elem.click()



#cme user login input

try:
    elem = driver.find_element_by_id("userNameInput")
    elem.clear()
    elem.send_keys(username)
    elem = driver.find_element_by_id("passwordInput")
    elem.clear()
    elem.send_keys(password)
    elem = driver.find_element_by_id("submitButton")
    elem.click() 
except Exception, e:
    print "Don't need username and password"




print "Loging succeefully"

windows_name = "Windows Security"
import win32api,win32con,win32gui,time
hn=win32gui.FindWindow(None, windows_name)  

print hn
n = 3
for i in range(1,n):
    keys(key.K_DOWN)

key.K_RETURN

find_element=True
while find_element:
    try:
        elem = driver.find_element_by_id("submitButton")
        elem.click()
        find_element=False   
    except Exception, e:
        time.sleep(1)

now_handle=driver.window_handles
'''
for handle in driver.window_handles:
    print handle
    driver.switch_to_window(handle)
'''    
        
# driver.implicitly_wait(3)        
# for handle in driver.window_handles:
#     print handle
#     driver.switch_to_window(handle)
time.sleep(1)    
key.tap("\r", )
#driverwitchTo().window(ie_handle)

#driver.switch_to_window("Verify User Pin")
#last_handle=driver.window_handles.pop()
#driver.switch_to_window(last_handle)
#driver.switch_to_alert()


#usb key check
wdname=u"Verify User PIN"
while True:     
    if fun.find_windows(wdname):
        time.sleep(3)
        fun.input_string(pin)
        time.sleep(2)
        key.tap("\r")
        time.sleep(1)
        break
    else:
        time.sleep(1)
    

#assert "Google" in driver.title

time.sleep(20)
driver.close()
driver.quit()
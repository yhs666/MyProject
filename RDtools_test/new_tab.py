#!/usr/bin/env python
#coding:utf-8
'''
Created on Dec 14, 2015

@author: yang.hongsheng
'''

from selenium import webdriver
import time,os



def new_table(url):
    main_window =driver.current_window_handle
    script_url= "window.open('%s','_blank');" % url
    driver.execute_script(script_url)
    driver.find_element_by_tag_name('body')
    hands = driver.window_handles
    if len(hands) >1 :
        driver.switch_to_window(driver.window_handles[1])
        print "new_table:successfull change the windows hands"
    else:
        print "new_table:Please check Ie setting"
        main_window ="" 
    return main_window
print "open url"

if __name__=='__main__':
    
    iedriver = "C:\Program Files\Internet Explorer\IEDriverServer.exe"
    
    os.environ["webdriver.ie.driver"] = iedriver
    driver = webdriver.Ie(iedriver)
    driver.get("https://passport.baidu.com/v2/?login")
    
    #login baidu.com
    driver.find_element_by_id("TANGRAM__PSP_3__userName").clear()
    driver.find_element_by_id("TANGRAM__PSP_3__userName").send_keys("zhinengdns")
    driver.find_element_by_id("TANGRAM__PSP_3__password").clear()
    driver.find_element_by_id("TANGRAM__PSP_3__password").send_keys("yhs2044999")
    driver.find_element_by_id("TANGRAM__PSP_3__submit").click()
    #driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    driver.implicitly_wait(2)
    
    print driver.title
    url = "http://www.baidu.com/"
    main_window =driver.current_window_handle
    # open new tab
    if new_table(url) != "":
        driver.implicitly_wait(5)
        driver.find_element_by_id("kw").send_keys("this is test")
        b = driver.find_element_by_id("su")
        b.click()
    else:
        print "change windows handle issue."
          
    #driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
    
    time.sleep(5)
    driver.close()

    driver.switch_to_window(main_window)
    print driver.title
    
    time.sleep(5)
    driver.close() 
    print "ok"
    driver.quit()
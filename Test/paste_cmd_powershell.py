#!/usr/bin/env python
#coding:utf-8
'''
Created on Dec 5, 2015

@author: yang.hongsheng
'''
import win32clipboard as w
import win32con
from autopy import key
import time
from autopy.mouse import RIGHT_BUTTON



def getText():
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_TEXT)
    w.CloseClipboard()
    return d

def setText(aString):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_TEXT, aString)
    w.CloseClipboard()
    
def paste_cmd_current(one_cmd):
    try:  
        setText(one_cmd)
        key.toggle(key.K_CONTROL,True)
        key.tap("v")
        key.toggle(key.K_CONTROL,False)
        return True
    except Exception:
        return False
    
    
if __name__=="__main__":

#     titles = set()
#     def foo(hwnd,mouse):
#     #去掉下面这句就所有都输出了，但是我不需要那么多
#         if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
#             #if GetWindowText(hwnd) == "Select Microsoft Azure PowerShell":
#             titles.add(GetWindowText(hwnd))
#     from win32con
#     EnumWindows(foo, 0)
#     lt = [t for t in titles if t]
#     lt.sort()
#     for t in lt:
#         print t
#         print(t.decode('GB2312'))
#               
#     a =FindWindow(None,"Select Microsoft Azure PowerShell")
#     print a
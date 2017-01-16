#!/usr/bin/env python
#coding:utf-8
'''
Created on Jan 1, 2016

@author: yang.hongsheng
'''
import win32api
import win32con
import win32gui
from ctypes import *
import time
from autopy import alert,mouse

class POINT(Structure):
    _fields_ = [("x", c_ulong),("y", c_ulong)]
def get_mouse_point():
    po = POINT()
    windll.user32.GetCursorPos(byref(po))
    return int(po.x), int(po.y)
def mouse_click(x=None,y=None):
    if not x is None and not y is None:
        mouse_move(x,y)
        time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def mouse_right_click(x=None,y=None):
    if not x is None and not y is None:
        mouse_move(x,y)
        time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
def mouse_dclick(x=None,y=None):
    if not x is None and not y is None:
        mouse_move(x,y)
        time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
def mouse_move(x,y):
    windll.user32.SetCursorPos(x, y)

 
 
def paste_cmd(x=700,y=350):
    a=70
    b=61
    mouse_click(x, y)
    mouse_right_click(x, y)
    mouse.smooth_move(x+a, y+b)
    mouse_click(x+a, y+b)



#alert.alert(msg, title="AutoPy Alert", default_button="OK", [cancel_button])

from win32api import GetSystemMetrics

offset_w = 150
offset_h = 60
round_time = 60

sys_width =GetSystemMetrics(0)
sys_height =GetSystemMetrics(1)

mouse_move(sys_width/2, sys_height/2)
while True:
    a, b = get_mouse_point()
    s = "Do you want the Robot check blow point?\n %s ,%s" % (a,b)

    if alert.alert(s,"Robot message", default_button="OK",cancel_button="Cancel"):
        mouse_w =a
        mouse_h =b
        break
    else:
        s = "Please move your mouse! 5s will confirm to you!"
        time.sleep(5)
    

print mouse_w,mouse_h

while True:
    mouse_right_click(x=mouse_w,y=mouse_h)
    time.sleep(1)
    x = mouse_w+offset_w
    y = mouse_h+offset_h
    mouse_move(x,y)
    time.sleep()
    mouse_click(x,y)
    print time.ctime()
    time.sleep(60)

#!/usr/bin/env python
#coding:utf-8
'''
Created on Dec 5, 2015

@author: yang.hongsheng
'''
import win32api
import win32con
import win32gui

MAIN_HWND = 0

def is_win_ok(hwnd, starttext):
    s = win32gui.GetWindowText(hwnd)
    if s.startswith(starttext):
        print (s)
        global MAIN_HWND
        MAIN_HWND = hwnd
        return None
    return 1


def find_main_window(starttxt):
    global MAIN_HWND
    win32gui.EnumChildWindows(0, is_win_ok, starttxt)
    return MAIN_HWND


def winfun(hwnd, lparam):
    s = win32gui.GetWindowText(hwnd)
    if len(s) > 3:
        print("winfun, child_hwnd: %d   txt: %s" % (hwnd, s))
    return 1

def main():
    main_app = 'Microsoft Azure PowerShell'
    hwnd = win32gui.FindWindow(None,main_app)
    print hwnd
    win32gui.ShowWindow(hwnd, 0)
    if hwnd < 1:
        hwnd = find_main_window(main_app)
        print (hwnd)
        # Shows or hides a window and changes its state
        win32gui.ShowWindow(hwnd, 0)
    def show(self):
        # windows handlers
        hwnd = self.window.handle
        win32gui.SetForegroundWindow (hwnd)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE| win32con.SWP_NOOWNERZORDER|win32con.SWP_SHOWWINDOW)    
        #X11LockScreenWindow.show(self)
        
    def hide(self):
        #X11LockScreenWindow.hide(self)
        # windows handlers
        hwnd = self.window.handle
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0,win32con.SWP_HIDEWINDOW|win32con.SWP_NOMOVE|win32con.SWP_NOSIZE|win32con.SWP_NOACTIVATE|win32con.SWP_NOOWNERZORDER)    



    #win32gui.SetForegroundWindow(hwnd)
    #win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE )
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE| win32con.SWP_NOOWNERZORDER|win32con.SWP_SHOWWINDOW)
          
main()      
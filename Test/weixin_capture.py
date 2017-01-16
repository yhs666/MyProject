#!/usr/bin/env python
#coding:utf-8
'''
Created on Sep 11, 2015

@author: yang.hongsheng
'''

import os
import sys
import win32gui
import win32con
from PIL import ImageGrab
from win32con import NULL
game_hwnd= win32gui.FindWindow(None,"Windows PowerShell ISE") 
print game_hwnd

win32gui.ShowWindow(game_hwnd, win32con.SW_RESTORE) # 强行显示界面后才好截图 
win32gui.SetForegroundWindow(game_hwnd) # 将游戏窗口提到最前  
# 裁剪得到全图 
game_rect = win32gui.GetWindowRect(game_hwnd)

from autopy import mouse

print mouse.get_pos()

src_image = ImageGrab.grab((game_rect[0] + 9, game_rect[1] + 190, game_rect[2] - 9, game_rect[1] + 190 + 450)) #
src_image.show()   
# 分别裁剪左右内容图片 
left_box = (9, 0, 500, 450)
right_box = (517, 0, 517 + 500, 450)
image_left = src_image.crop(left_box)
image_right = src_image.crop(right_box) # 
image_left.show() # 
image_right.show()

src_image.crop()
# sys.path.append('.')
# addr=r'D:\test.jpeg'
# from PIL import ImageGrab
# im = ImageGrab.grab()
# 
# im= ImageGrab.grab()
# 
# im.save(addr,'jpeg')


#im.save



#!/usr/bin/env python
#coding:utf-8
'''
Created on Nov 30, 2016

@author: yang.hongsheng
'''
#from curses.ascii import isdigit
total = 0.0
while True:
    value = raw_input('Enter the value for the seat [\'q\' to quit] :')
    
    try:
        value = float(value)
        total = total + value
        print "Current is {} ".format(total)
        
    except:
        print "I'm sorry, but {} isn't valid. Please try again".format(value)
   
    
    if value == 'q':
        break

        
print "Here is the total money, {} ".format(total)
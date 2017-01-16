#!/usr/bin/env python
#coding:utf-8
'''
Created on Nov 11, 2016

@author: yang.hongsheng
'''



def get_users():
    users = open("users.txt","r")
    qs = users.readline()
    user_key=""
    while qs:
        s = qs.strip()
        if len(s) != 0  and  s[0] != "#"  :
            user_key="'" + s + "'," +user_key
        qs = users.readline()
    users.close() 
    user_key= user_key.strip(",") 
    return user_key

#print get_users()
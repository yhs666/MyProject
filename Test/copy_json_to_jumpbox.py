#!/usr/bin/env python
#coding:utf-8
'''
Created on Apr 1, 2016

@author: yang.hongsheng
'''

import json

ddict =[{"name":"yang-dir","path":"Fabric","cmd":"dir"},{"name":"yang-pwd","path":"Fabric","cmd":"pwd"}]


print json.dumps(ddict)
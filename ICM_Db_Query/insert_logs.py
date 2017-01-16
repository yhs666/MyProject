#!/usr/bin/env python
#coding:utf-8
'''
Created on Nov 2, 2016

@author: yang.hongsheng
'''

import os
import logging
from datetime import datetime
FILE=os.getcwd()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename = os.path.join(FILE,'logs_log.txt'),
                    filemode='a')
DATETIME_FMT = '%Y-%m-%d %H:%M:%S'
updatetime = datetime.strftime(datetime.now(), DATETIME_FMT)
def print_logs(loggs):
    print updatetime,":",loggs
    msg =""
    if type(loggs) is str:
        logging.info(loggs)
    elif type(loggs) is list:
        for i in loggs:
            msg= str(i)+ ","
        logging.info(msg)
    elif type(loggs) is dict:
        for (k,v) in  loggs.items():
            msg =k + " : " + v +";"
        logging.info(msg)
    elif type(loggs) is tuple:
        msg =str(loggs)
        logging.info(msg)
    else:
        print type(loggs)
        logging.info("Input not string/list/dict")
        
        
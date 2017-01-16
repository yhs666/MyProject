#!/usr/bin/env python
#coding:utf-8
'''
Created on Jul 8, 2016

@author: yang.hongsheng
'''

import os
import time
import redis
import logging
import sys
import getpass

ip ="172.31.4.119"
password = "wasu.com"
time_out = 60
import crypto
import sys
sys.modules['Crypto'] = crypto
from crypto.Cipher import AES

FILE=os.getcwd()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename = os.path.join(FILE,'log.txt'),
                    filemode='w')
try:
    myredis = redis.Redis(host=ip,password=password,port = 6379)
    print "Connect Redis OK!"
    logging.info('Connect Redis OK!')

except:
    print "Redis connect issue!"
    logging.info('Redis connect issue!')
    sys.exit()


from binascii import b2a_hex, a2b_hex
 
class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC
     
    #加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        #这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        #所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)
     
    #解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')
 
if __name__ == '__main__':
    pc = prpcrypt('wasuwasuwasuwasu')      #初始化密钥
    pwd =getpass.getpass("Please input the oe-yanghongsheng cme password:")
    
    e = pc.encrypt(pwd)                     
    print e
    if myredis.set('cmepwd',e):
        myredis.set('cmepwd:time',time.ctime())
        print "set passwrod ok"
    else:
        print "set password have issue!!"
    sys.exit()

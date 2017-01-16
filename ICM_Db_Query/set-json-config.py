#!/usr/bin/env python
#coding:utf-8
'''
Created on Jan 3, 2017

@author: yang.hongsheng
'''


config={
        'mysqldb':{'host':'172.31.4.101',
                   'username':'icm',
                   'password':'wasu@1234',
                   'db':'icm'
                   },
        'DataWarehouse':{'host':'suodk6gsjy.database.windows.net',
                        'username':'nanboli@suodk6gsjy.database.windows.net',
                        'password':'oarnAlUzNblwkw13',
                        'db':'Azure-China-DataWarehouse'
                        },
        'wasu-users':"'oe-fansongchen-china','oe-quanzhiyang-china','oe-yanghongsheng-china','oe-yangfacai-china','oe-zhanglianhui-china','oe-luowei-china','oe-zoulili-china','oe-zhangyuan-china','oe-jiangshixun-china','oe-lichuangcheng-china','oe-guofei-china'",
        
        }

import json

json.dump(config,open('config.dat', 'w'))
global config2

config2 = json.load(open('config.dat', 'r'))

print config2



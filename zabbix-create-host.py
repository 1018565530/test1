#!/usr/bin/env python
#coding:utf-8
#mail:yikun@
#datetime:2018-10-02
#version:1.0

import urllib2
import json
import sys
import os
import argparse
import re

class zabbixapi:
    def __init__(self):
        self.url = ""
        self.header = {"Content-Type":"application/json"}
        self.auth = self.login()

        ####   自定义 groupname,proxyname,templatename #######
        #parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser()
        parser.add_argument('-G',action='store',dest='groupname',nargs='*',default=[],help='please input your groupname')
        parser.add_argument('-T', action='store', dest='templatename', nargs='*', default=[],help='please input your templatename')
        parser.add_argument('-P', action='store', dest='proxyname', nargs='*', default=[],help='please input your proxyname')
        args = parser.parse_args()
        self.groupname = args.groupname
        self.templatename = args.templatename
        self.proxyname = args.proxyname

    def login(self):
        data = json.dumps(
        {
           "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                 "user":"",
                 "password":""
                },
            "id": 0
        })
        req = urllib2.Request(self.url,data)
        for key in self.header:
            req.add_header(key,self.header[key])
        try:
            result = urllib2.urlopen(req)
        except URLError as e:
            print("Auth Failed, Please Check Your Name AndPassword:",e.code)
        else:
            response = json.loads(result.read())
            auth = response['result']
            #print auth
            return auth
            #print("Auth Successful. The Auth ID Is:",response['result'])
          #####################################################################

    def get_date(self,data):
        req = urllib2.Request(self.url,data)
        for key in self.header:
            req.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(req)
        except URLError as e:
            print("Auth Failed, Please Check Your Name AndPassword:", e.code)
        else:
            response = json.loads(result.read())
            result.close()
            return response


    def get_host(self,ip):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.get",
            "params":{
                "output": "extend",
                "filter":{
                    "host":ip
                }
            },
            "auth":self.auth,
            "id":2
            })
        result = self.get_date(data)['result']
        if result > 0:
            for host in result:
                bus = host['name']
                return bus
                #print 'host is create arealy'  + 'ip:',host['host'],' ','业务模块:',host['name'],' hostid:',host['hostid']
        else:
            print "Error host,check over!!!"
    

    #######  获取 host -> hostid #######
    def get_groupid(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params":{
                "output": "extend",
                "filter":{
                    "name":self.groupname
                    }
            },
            "auth":self.auth,
            "id":3
         })
        result = self.get_date(data)['result']
        #print(result)
        if len(result) >0:
            for groupid in result:
                groupid = groupid['groupid']
                #print(groupid)
                return groupid

    
    ###### 获取templateid #######
    def get_templateid(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.get",
            "params":{
                "output": "extend",
                "filter":{
                    "host":self.templatename
                    }
            },
            "auth":self.auth,
            "id":4
        })
        
        result = self.get_date(data)['result']
        for templateid in result:
            templateid = templateid['templateid']
            #print(templateid)
            return templateid


    ###### 获取proxyid  ########
    def get_proxyid(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "proxy.get",
            "params":{
                "output": "extend",
                "host":self.proxyname
            },
            "auth":self.auth,
            "id":5
        })
        result = self.get_date(data)['result']
        for proxyid in result:
            proxyid = proxyid['proxyid']
            print(proxyid) 
            return proxyid


    ####### 批量创建主机 host ######
    def create_host(self):
        with open('./1.txt','r') as f:
            lines = f.readlines()
            for i in lines:
                if i.strip():
                    line = i.strip()
                    tmp = re.split('\s+', line)
                    ip = tmp[0].strip()
                    Business = tmp[1].strip() + '-' + tmp[0].strip()
                    #print(ip + ' ' + Business)
                    #host = self.get_host(ip)
                    #if self.get_host(ip):
                    #    return 0
                        
                    if not self.get_host(ip):
                        data = json.dumps({
                            "jsonrpc":"2.0",
                            "method":"host.create",
                            "params":{
                                "name":Business,
                                "host":ip,
                                "proxy_hostid":self.get_proxyid(),
                                #"proxy_hostid":12738,
                                "interfaces":[{
                                    "type":1,
                                    "main":1,
                                    "useip":1,
                                    "ip":ip,
                                    "dns":"",
                                    "port":"10050"
                                }],
                                "groups":[{"groupid":self.get_groupid()}],
                                "templates":[{"templateid":self.get_templateid()}]
                            },
                            "auth":self.auth,
                            "id":5

                        })
                        result = self.get_date(data)
                        #print(result)
                        if len(result) >0:
                            print "\033[1;32m [%s]:create hostname monitor  success!  \033[0m"   % Business
                        else:
                            print "Create host is bad,check it !!!"

                    else:
                        print "\033[1;32m [%s]:create is already!  \33[0m"   % Business
    ################################             


def main():
    zapx = zabbixapi()
    zapx.get_proxyid()
    zapx.create_host()

if __name__ == '__main__':
    main()

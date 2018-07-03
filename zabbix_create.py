#!/usr/bin/env python
import urllib2
import json
import sys
import re

url = "https://xxx//api_jsonrpc.php"
header = {"Content-Type":"application/json"}
data = json.dumps(
{
   "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
         "user": "xxx",
         "password": "xxx"
               },
    "id": 0
})

req = urllib2.Request(url,data)
for key in header:
    req.add_header(key,header[key])
try:
    result = urllib2.urlopen(req)
except URLError as e:
    print("Auth Failed, Please Check Your Name AndPassword:",e.code)
else:
    #print type(result)
    response = json.loads(result.read())
    auth = response['result']
    result.close()
    print(auth)
	#print("Auth Successful. The Auth ID Is:",response['result'])
  #####################################################################
with open('1.txt') as f:
    lines = f.readlines()
    for line in lines:
        i = line.strip()
        tmp = re.split("\s",i)
        ip = tmp[0]
        templatename = tmp[1]
        groupname = tmp[2]
        proxyname = tmp[3]

data1 = json.dumps(
{
    "jsonrpc": "2.0",
    "method": "template.get",
    "params": {
        "output": "extend",
        "filter": {
            "host": [templatename]
        }
    },
    "auth": auth,
    "id": 1
}
)
req = urllib2.Request(url,data1)
for key in header:
    req.add_header(key,header[key])
try:
    result = urllib2.urlopen(req)
except URLError as e:
    print("Auth Failed, Please Check Your Name AndPassword:",e.code)
else:
    response = json.loads(result.read())
    if len(response['result']):
	    for templateid in response['result']:
		templateid = templateid['templateid']
    else:
        sys.exit(1)


data2 = json.dumps(
{
    "jsonrpc": "2.0",
    "method": "hostgroup.get",
    "params": {
        "output": "extend",
        "filter": {
            "name": [groupname]
        }
    },
    "auth": auth,
    "id": 1
}
)
req = urllib2.Request(url,data2)
for key in header:
    req.add_header(key,header[key])
try:
    result = urllib2.urlopen(req)
except URLError as e:
    print("Auth Failed, Please Check Your Name AndPassword:",e.code)
else:
    response = json.loads(result.read())
    if len(response['result']):
        groupid = response['result']['groupid']
    '''for groupid in response['result']:
        groupid = groupid['groupid']'''
    else:
        sys.exit(1)



data3 = json.dumps(
{
    "jsonrpc": "2.0",
    "method": "proxy.get",
    "params": {
        "output": "extend",
        "filter": {
            "host": [proxyname],
        }
    },
    "auth": auth,
    "id": 1
}
)
req = urllib2.Request(url,data3)
for key in header:
    req.add_header(key,header[key])
try:
    result = urllib2.urlopen(req)
except URLError as e:
    print("Auth Failed, Please Check Your Name AndPassword:",e.code)
else:
    response = json.loads(result.read())
    if len(response['result']):
        proxyid = response['result']['proxyid']
    else:
        sys.exit(1)


data4 = json.dumps(
{
    "jsonrpc": "2.0",
    "method": "host.create",
    "params": {
        "host": ip,
        "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": "10050"
            }
        ],
        "groups": [
            {
                "groupid": groupid
            }
        ],
        "templates": [
            {
                "templateid": templateid
            }
        ],
        "proxys":[
            {
                "proxyid":proxyid
            }
        ],
    },
    "auth": auth,
    "id": 1
}
)
req = urllib2.Request(url,data4)
for key in header:
    req.add_header(key,header[key])
try:
    result = urllib2.urlopen(req)
except URLError as e:
    print("Auth Failed, Please Check Your Name AndPassword:",e.code)
else:
    response = json.loads(result.read())
    if len(response['result']):
        print "***********************"
    else:
        sys.exit(1)

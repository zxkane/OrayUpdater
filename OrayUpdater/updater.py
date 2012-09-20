# -*- coding: utf-8 -*-
# encoding: utf-8
'''
A script will register current IP to dynamic DNS service provided by oray.com
Created on 2012-9-19

@author: kane
@contact: kane.mx@gmail.com
@license: EPL
'''

import urllib2
import re
import httplib
import base64
import os
import argparse
import sys
try:
    import ConfigParser as configparser
except ImportError:
    import configparser

CONFIG_LASTIP = u'.orayupdater_last'
IP_PATTERN = r'(?P<ip>((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(2[0-4][0-9]|25[0-5]|1[0-9]{2}|[1-9][0-9]|[0-9])))'

def _getLastIP():
    try:
        with open(os.getenv("HOME") + "/" + CONFIG_LASTIP) as lastIPFile:
            line = lastIPFile.readline()
            if line:
                rt = re.search(IP_PATTERN, line)
                if rt:
                    return rt.group('ip')
    except:
        pass
    return None

def _rememberLastIP(currentIP):
    f = open(os.getenv("HOME") + "/" + CONFIG_LASTIP, 'w')
    f.write(currentIP)
    
def _loadConf():
    config = configparser.ConfigParser()
    configs = {}
    try:
        config.readfp(open(os.path.expanduser('~/.orayupdater.cfg')))
        configs['USERNAME'] = config.get("OrayUpdator", "Username")
        configs['HOSTNAME'] = config.get("OrayUpdator", "Hostname")
        configs['PASSWORD'] = config.get("OrayUpdator", "Password")
    except:
        pass
    return configs
    

SERVICE_STATUS = {
'good': u'更新成功',
'nochg': u'更新成功，但没有改变IP。',
'notfqdn': u'未有激活花生壳的域名',
'nohost':  u'域名不存在或未激活花生壳',
'abuse':  u'请求失败，频繁请求或验证失败',
'badauth':  u'验证失败，用户名或密码错误',
'badagent': u'请求的User-Agent不合法',
'!donator': u'此功能需要付费用户才能使用，如https',
'911': u'系统错误',
}

class C(object):
    USERNAME, HOSTNAME, PASSWORD = [None, None, None]
    FORCE = False

c = C()
parser = argparse.ArgumentParser(description='Update your current IP to your dynamic DNS service provided by oray.com.')
parser.add_argument('-f', '--force', dest='FORCE', action='store_true', help='force updating IP address of ddns')
parser.add_argument('-s', '--hostname', dest='HOSTNAME', help='hostname to be updated')
parser.add_argument('-u', '--username', dest='USERNAME', help='username of Oray.com')
parser.add_argument('-p', '--password', dest='PASSWORD', help='password of Oray.com')
parser.parse_args(namespace=c)

if not c.HOSTNAME or not c.USERNAME or not c.PASSWORD:
    configs = _loadConf()
    if 'USERNAME' in configs:
        c.USERNAME = configs['USERNAME']
    if 'HOSTNAME' in configs:
        c.HOSTNAME = configs['HOSTNAME']
    if 'PASSWORD' in configs:
        c.PASSWORD = configs['PASSWORD']

if not c.HOSTNAME or not c.USERNAME or not c.PASSWORD:
    parser.print_help()
    sys.exit(-1)

output = urllib2.urlopen("http://ddns.oray.com/checkip").read()
rt = re.search(IP_PATTERN, output)
if rt is None:
    print u'Looks like checkip service is down. Or your Internet connection is down.'
else:
    currentIP = rt.group('ip')
    lastIP = _getLastIP()
    if lastIP != currentIP or c.FORCE:
        print u"Will register %s for host %s" %(currentIP, c.HOSTNAME)
        conn = httplib.HTTPConnection("ddns.oray.com")
        passcode = u'%s:%s' %(c.USERNAME, c.PASSWORD)
        headers = {"Authorization": "Basic %s" %(base64.b64encode(passcode.encode('ascii'))),
            "User-Agent": "Oray"}
        conn.request("GET", "/ph/update?hostname=%s&myip=%s" %(c.HOSTNAME, currentIP), headers=headers)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            statusCode = data.split()[0]
            if statusCode in SERVICE_STATUS:
                print SERVICE_STATUS.get(statusCode)
                if statusCode == 'good' or statusCode == 'nochg':
                    _rememberLastIP(currentIP)
            else:
                print data
        else:
            print u'网络错误 %s: %s' %(response.status, response.reason)
        conn.close()
    else:
        print u'%s 已经注册到 %s。' %(currentIP, c.HOSTNAME)
    

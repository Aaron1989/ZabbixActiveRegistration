#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import json
import logging
import os.path
import sys
import subprocess
import time
import commands
import re
import sys
import os
import smtplib
import fcntl
import struct
import signal
import socket
import urllib, urllib2
import logging
import json
import sys
import datetime, time
import os
import argparse
import requests
import re

sys.getdefaultencoding()
import requests
import re

reload(sys)
sys.setdefaultencoding("utf-8")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    # filename='/usr/lib/zabbix/alertscripts/alertor/alertor.log',
                    filename='/usr/lib/zabbix/alertscripts/alertor/alertor.log',
                    filemode='w')

__URL_TEMPLATE_GET_TOKEN = "%s?corpid=%s&corpsecret=%s"
__URL_TEMPLATE_SEND_MESSAGE = "%s?access_token=%s"


class wechat(object):
    def __init__(self, user, message):
        logging.info('Send to user is: %s' % (user))
        logging.info('Send message is: %s' % (message))

        dict1 = {'nec': '2', 'qybx': '4', 'qypay': '10', 'kypay': '10', 'web': '6', 'plugins': '6', 'middle': '6',
                 'hms': '5', 'devops': '9'}
        # conf = '/usr/lib/zabbix/alertscripts/alertor/alertor.conf'
        conf = 'alertor.conf'
        config = ConfigParser.ConfigParser()
        config.read(conf)

        self.__URL_TEMPLATE_GET_TOKEN = '%s?corpid=%s&corpsecret=%s'
        self.__URL_TEMPLATE_SEND_MESSAGE = '%s?access_token=%s'
        self.__crop_id = config.get('wechat', 'CorpId')
        self.__secret = config.get('wechat', 'Secret')
        self.__get_token_uri = config.get('wechat', 'TokenURI')
        self.__send_message_uri = config.get('wechat', 'MessageURI')
        self.__data = '{\n\
            "touser":"%s",\n\
            "toparty":"",\n\
            "totag":"@all",\n\
            "msgtype":"text",\n\
            "agentid":"0",\n\
            "text":{\
                "content":"%s"\n\
            },\n\
            "safe":"0",\n}' % (user, message)

    def __get_token(self):
        result = requests.get(self.__URL_TEMPLATE_GET_TOKEN % (self.__get_token_uri, self.__crop_id, self.__secret))
        result = json.loads(result.text)
        return result['access_token'].encode('utf-8')

    def alert(self):
        logging.info('Post messages is: %s' % (self.__data))
        result = requests.post(self.__URL_TEMPLATE_SEND_MESSAGE % (self.__send_message_uri, self.__get_token()),
                               data=self.__data)
        result = json.loads(result.text)
        result = result['errcode']
        logging.info('Post result is: %s' % (result))
        return result


class jumpserver(object):
    def __init__(self, users, subject, message):
        logging.info('Send to user is: %s' % (users))
        logging.info('subject is: %s' % (subject))
        logging.info('Send message is: %s' % (message))
        conf = '/usr/lib/zabbix/alertscripts/alertor/alertor.conf'
        config = ConfigParser.ConfigParser()
        config.read(conf)
        self.__JPS_API_URL = config.get('wechat', 'JPS_API_URL')
        self.__JPS_TOKEN = config.get('wechat', 'JPS_TOKEN')
        self.__subject = subject
        self.__message = message
        # print re.split(r'[:\n]',self.__message)[3]

    def generate_request(self):
        self.__message = sel.__message.replace('\r', '')
        if 'OK' in self.__subject.split(',')[0]:
            req_body = {

                "alert_id": re.split(r'[:\n]', self.__message)[17],
                "alert_type": re.split(r'[:\n]', self.__message)[9],  # cpu,mem,disk,iops
                "instance": re.split(r'[:\n]', self.__message)[1],  # IP
                "instance_name": self.__subject.split(':')[1],
                "message": re.split(r'[:\n]', self.__message)[7],
                "CreateTime": '',
                "CloseTime": re.split(r'[:\n]', self.__message)[3] + ':' + re.split(r'[:\n]', self.__message)[4] + ':' +
                             re.split(r'[:\n]', self.__message)[5]
            }
        else:
            req_body = {
                "alert_id": re.split(r'[:\n]', self.__message)[17],
                "alert_type": re.split(r'[:\n]', self.__message)[9],  # cpu,mem,disk,iops
                "instance": re.split(r'[:\n]', self.__message)[1],  # IP
                "instance_name": self.__subject.split(':')[1],
                "message": re.split(r'[:\n]', self.__message)[7],
                "CreateTime": re.split(r'[:\n]', self.__message)[3] + ':' + re.split(r'[:\n]', self.__message)[
                    4] + ':' + re.split(r'[:\n]', self.__message)[5],
                "CloseTime": ''
            }
        print req_body
        return req_body

    def requests_post(self, req_body):
        header = {"token": self.__JPS_TOKEN}
        res = requests.post(url="http://{}/jpatrol/inspect/".format(self.__JPS_API_URL), data=json.dumps(req_body),
                            headers=header, )
        print 'res.code:{},res.body:{}'.format(res.status_code, res.text)


class wechat1(object):
    def __init__(self, corpsecret, corpid, appid):
        self.corpsecret = corpsecret
        self.corpid = corpid
        self.appid = appid

    def gettoken(self):
        tokenURL = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (
        self.corpid, self.corpsecret)
        token_file = urllib2.urlopen(tokenURL)
        token_data = token_file.read().decode('utf-8')
        token_json = json.loads(token_data)
        token_json.keys()
        token = token_json['access_token']
        return token
        # 发送文本信息

    def senddata(self, access_token, user, content):
        PURL = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + access_token
        dict = {'nec': '2', 'qybx': '4', 'qypay': '10', 'kypay': '10', 'web': '6', 'plugins': '6', 'middle': '6',
                'hms': '5', 'devops': '9', 'xianop': '11'}
        send_values = {
            'touser': '',
            'toparty': dict[user],
            'totag': "@all",
            'msgtype': "text",
            'agentid': self.appid,
            'text': {
                'content': content
            },
            'safe': "0"
        }
        send_data = json.dumps(send_values, ensure_ascii=False, indent=2).encode('utf-8')
        send_request = urllib2.Request(PURL, send_data)
        response = json.loads(urllib2.urlopen(send_request).read())
        return str(response)


if __name__ == '__main__':
    logging.info('main in')
    # wechat(sys.argv[1], sys.argv[2] + '\n' + sys.argv[3]).alert()
    # jumpservers = jumpserver(sys.argv[1], sys.argv[2], sys.argv[3])
    # jumpservers.requests_post(jumpservers.generate_request())
    # jumpservers.generate_request()
    logging.info('main out')
    wechataccount = wechat1('<corpsecret>', '<corpid>', '<appid>')
    access_token = wechataccount.gettoken()
    content = str(sys.argv[2] + '\n' + sys.argv[3])
    user = sys.argv[1]
    logging.info(user)
    wechataccount.senddata(access_token, user, content)

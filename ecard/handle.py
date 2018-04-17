import re
import os
import json
import time
import logging
import requests
from bs4 import BeautifulSoup
from hashlib import sha256, md5
from datetime import datetime, timedelta

from django.conf import settings
from django.http import JsonResponse

from ecard.models import EcardProfile
from utils.auth import UserManager
from ecard.apps import APIServerErrorCode as ASEC

app = logging.getLogger('app.custom')


class EcardManager(object):
    """docstring for EcardManager"""
    key = ''
    ecardurl = 'https://ecard.neusoft.edu.cn/'
    Balance = 'https://ecard.neusoft.edu.cn/zh-hans/user/balance'
    detail = 'https://ecard.neusoft.edu.cn/zh-hans/user/detail/'
    ecardinfo = 'https://ecard.neusoft.edu.cn/zh-hans/user/me'

    def __init__(self, postdata, user):
        self.data = postdata
        self.user = user

    @staticmethod
    def split_key(key):
        return key.split('/')[3]

    # @staticmethod
    # def check_key_exist(key):
    #     try:
    #         UserProfile.objects.get

    def bind_card(self):
        key = EcardManager.split_key(self.data['key'])
        client = requests.Session()

        try:
            client.get(self.ecardurl + str(key))

            info_html = client.get(self.ecardinfo)
        except Exception as e:
            app.error(str(e))
            return {'message': 'failed'}

        try:
            soup = BeautifulSoup(info_html.text, 'lxml')

            txt = soup.select('div.container')[1].text

            name = re.findall(r'姓名：(.*)', txt)[0]
            subject = re.findall(r'专业：(.*)', txt)[0]
            grade = re.findall(r'年级：(.*)', txt)[0]
        except Exception as e:
            app.info(str(e))
            return {'message': 'failed'}

        user = EcardProfile(open_id=self.user,
                           ecard_key=key,
                           name=name,
                           subject=subject,
                           grade=grade)

        self.user.is_bind = 0
        self.user.save()

        user.save()

        return {'message': 'ok', 'info': UserManager.get_user_info(self.user)}

    def balance_card(self):
        client = requests.Session()

        if self.user.is_bind == 1:
            return {'message': 'failed'}

        self.key = UserManager.get_user_key(self.user)

        client.get(self.ecardurl + str(self.key))
        balance_html = client.get(self.Balance)

        soup = BeautifulSoup(balance_html.text, 'lxml')
        tmp = soup.select('div.container p')[0].text.split()

        info = {}

        info['kpye'] = tmp[1]
        info['zhye'] = tmp[4]
        info['gdye'] = tmp[7]

        return {'message': 'ok',
                'info': info}

    def detail_card(self):
        client = requests.Session()

        if self.user.is_bind == 1:
            return {'message': 'failed'}

        self.key = UserManager.get_user_key(self.user)
        client.get(self.ecardurl + str(self.key))
        month = self.data.get('month', 0)
        detail_html = client.get(self.detail + str(month))

        soup = BeautifulSoup(detail_html.text, 'lxml')
        alldetail = soup.select('tr')
        tmpinfo = []

        for deta in alldetail:
            tmp = []
            res = {}

            for li in deta.select('td'):
                tmp.append(li.text.strip())
            print(tmp)
            if len(tmp) != 0:
                res['time'] = tmp[1]
                res['type'] = tmp[2]
                res['skck'] = tmp[4]
                res['jye'] = tmp[5]
                res['yue'] = tmp[6]
                tmpinfo.append(res)

        tmpinfo.reverse()

        return {'message': 'ok',
                'info': tmpinfo}

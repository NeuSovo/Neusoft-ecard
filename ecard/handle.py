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
from utils.tools import redis_global

app = logging.getLogger('app.custom')


class EcardManager(object):
    """docstring for EcardManager"""
    key = ''
    ecardurl = 'https://ecard.neusoft.edu.cn/zh-hans/'
    Balance = 'https://ecard.neusoft.edu.cn/zh-hans/user/balance'
    detail = 'https://ecard.neusoft.edu.cn/zh-hans/user/detail/'
    ecardinfo = 'https://ecard.neusoft.edu.cn/zh-hans/user/me'

    def __init__(self, postdata, user):
        self.data = postdata
        self.user = user

    @staticmethod
    def split_key(key):
        return key.split('/')[3]

    def bind_card(self):
        has_bind = True
        try:
            ecard = EcardProfile.objects.get(open_id=self.user)
        except Exception:
            has_bind = False

        key = EcardManager.split_key(self.data['key'])
        client = requests.Session()

        cookies_dict = self.update_session(key)
        if cookies_dict:
            client.cookies = self.get_session(key)
        else:
            app.error("cookies_dict")
            return {'message': 'failed'}

        info_html = self.get_html(client, self.ecardinfo)
        try:
            soup = BeautifulSoup(info_html.text, 'lxml')

            txt = soup.select('div.container')[1].text

            name = re.findall(r'姓名：(.*)', txt)[0]
            subject = re.findall(r'专业：(.*)', txt)[0]
            grade = re.findall(r'年级：(.*)', txt)[0]
        except Exception as e:
            app.info(str(e))
            return {'message': 'failed'}

        if has_bind:
            ecard.ecard_key = key
            ecard.name = name
            ecard.subject = subject
            ecard.grade = grade
        else:
            ecard = EcardProfile(open_id=self.user,
                                 ecard_key=key,
                                 name=name,
                                 subject=subject,
                                 grade=grade)

            self.user.is_bind = 1
            self.user.save()
        ecard.save()
        return {'message': 'ok', 'info': UserManager.get_user_info(self.user)}

    def balance_card(self):
        if self.user.is_bind == 0:
            return {'message': '请先绑定饭卡'}

        self.key = UserManager.get_user_key(self.user)
        client = self.get_client(self.key)


        redis_key = 'balance_' + self.key
        # Redis
        if redis_global.exists(redis_key):
            return eval(redis_global.get(redis_key))

        # client.get(self.ecardurl + str(self.key))
        balance_html = self.get_html(client, self.Balance)

        try:
            soup = BeautifulSoup(balance_html.text, 'lxml')
            tmp = soup.select('div.container p')[0].text.split()

            info = {}

            info['kpye'] = tmp[1]
            info['zhye'] = tmp[4]
            info['gdye'] = tmp[7]

            result = {'message': 'ok',
                      'info': info}
        except Exception as e:
            app.warn(str(e))
            info = {}
        # Redis
        if info:
            redis_global.set(redis_key, result, ex=600)
        return result

    def detail_card(self):
        if self.user.is_bind == 0:
            return {'message': '请先绑定饭卡'}
        self.key = UserManager.get_user_key(self.user)
        client = self.get_client(self.key)
        month = self.data.get('month', 0)

        redis_key = 'detail_' + str(month) + '_' + self.key
        # Redis
        if redis_global.exists(redis_key):
            return eval(redis_global.get(redis_key))

        # client.get(self.ecardurl + str(self.key))

        detail_html = self.get_html(client, self.detail + str(month))

        try:
            soup = BeautifulSoup(detail_html.text, 'lxml')
            alldetail = soup.select('tr')
            info = []

            for deta in alldetail:
                tmp = []
                res = {}

                for li in deta.select('td'):
                    tmp.append(li.text.strip())
                if len(tmp) != 0:
                    res['time'] = tmp[1]
                    res['type'] = tmp[2]
                    res['skck'] = tmp[4]
                    res['jye'] = tmp[5]
                    res['yue'] = tmp[6]
                    info.append(res)

            info.reverse()
        except Exception as e:
            app.warn(str(e))
            info = []

        result = {'message': 'ok',
                  'info': info}
        # Redis
        if info:
            redis_global.set(redis_key, result, ex=600)
        return result

    def proxy_get(self, url="https://www.baidu.com"):
        p = Proxy()
        retry_count = 5
        proxy = p.get()
        while retry_count > 0:
            try:
                requests.get(url, proxies={"http": "http://{}".format(proxy)})
                # 使用代理访问
                return proxy
            except Exception:
                retry_count -=1

        return None

    def update_session(self, key):
        client = requests.Session()
        try:
            proxy = self.proxy_get()
            if not proxy:
                client.get(self.ecardurl + key, proxies={"http": "http://{}".format(proxy)})
            else:
                client.get(self.ecardurl + key)

            cookies_dict = json.dumps(client.cookies.get_dict())
            redis_global.set('cookies:dict:'+ key, cookies_dict)
            return cookies_dict
        except Exception as e:
            app.error(e)
            return False

    def get_session(self, key):
        if redis_global.exists('cookies:dict:'+ key):
            cookies_jar = requests.utils.cookiejar_from_dict(
                eval(redis_global.get('cookies:dict:'+ key)), cookiejar=None, overwrite=True)
            return cookies_jar
        return {}

    def get_html(self, client, url):
        proxy = self.proxy_get()
        if not proxy:
            html = client.get(url, proxies={"http": "http://{}".format(proxy)})
        else:
            html = client.get(url)
        if html.text.find('refresh') != -1:
            self.update_session(self.key)
        return html

    def get_client(self, key):
        client = requests.Session()
        client.cookies = self.get_session(key)
        return client


class Proxy:
    proxy_url = 'http://123.207.35.36:5010/'
    def __init__(self):
        pass

    def get(self):
        proxy = requests.get(self.proxy_url + 'get/').content
        return proxy.decode('utf-8')

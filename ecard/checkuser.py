# coding:utf-8
import os
import requests
from hashlib import md5, sha256

Appid = 'wx5c7d55175f3872b7'
SECRET = '18e18b264801eb53c9fe7634504f2f15'


def getOpenid(code):
    s = requests.Session()
    params = {
        'appid': Appid,
        'secret': SECRET,
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    data = s.get('https://api.weixin.qq.com/sns/jscode2session', params=params)

    return data.json()


def gen3rdkey(count=24):
    return (sha256(os.urandom(count)).hexdigest())


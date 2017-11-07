# coding:utf-8
import requests
from bs4 import BeautifulSoup

ecardurl = 'https://ecard.neusoft.edu.cn/'
Balance = 'https://ecard.neusoft.edu.cn/zh-hans/user/balance'
detail = 'https://ecard.neusoft.edu.cn/zh-hans/user/detail/'
info = 'https://ecard.neusoft.edu.cn/zh-hans/user/me'

def getB(key):
    s = requests.Session()
    s.get(key, timeout=4)
    data = s.get(Balance, timeout=4)
    soup = BeautifulSoup(data.text, 'lxml')
    Tmp = soup.select('div.container p')[0].text.split()
    res = {}

    res['kpye'] = Tmp[1]
    res['zhye'] = Tmp[4]
    res['gdye'] = Tmp[7]

    return res


def getD(key, month=''):
    s = requests.Session()
    s.get(key, timeout=4)
    data = s.get(detail + str(month), timeout=4)
    soup = BeautifulSoup(data.text, 'lxml')
    Alldetail = soup.select('tr')
    result = {}
    tmpinfo = []
    for deta in Alldetail:
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
            tmpinfo.append(res)
    tmpinfo.reverse()
    result['info'] = tmpinfo

    return result

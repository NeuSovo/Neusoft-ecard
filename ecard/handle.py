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

from ecard.models import *
from ecard.apps import APIServerErrorCode as ASEC

app = logging.getLogger('app.custom')


def parse_info(data):
    """
    parser_info:
    :param data must be a dict
    :return dict data to json,and return HttpResponse
    """
    return JsonResponse(data)


def usercheck():
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            result = {}
            request = args[0]
            try:
                body = json.loads(request.body)
                wckey = body['base_req']['wckey']
            except Exception as e:
                app.info(str(e))
                result['code'] = ASEC.ERROR_PARAME
                result['message'] = ASEC.getMessage(ASEC.ERROR_PARAME)
                response = parse_info(result)
                response.status_code = 400

                return response

            try:
                user_key = Sessions.objects.get(session_data=wckey)
            except Exception as e:
                app.info(str(e) + 'wckey:{}'.format(wckey))
                result['code'] = ASEC.SESSION_NOT_WORK
                result['message'] = ASEC.getMessage(ASEC.SESSION_NOT_WORK)

                return parse_info(result)

            if user_key.expire_date < datetime.now():
                result['code'] = ASEC.SESSION_EXPIRED
                result['message'] = ASEC.getMessage(ASEC.SESSION_EXPIRED)

                return parse_info(result)

            user = UserManager.get_user(wckey=wckey)

            # app.info("[{}][{}][{}]".format(
            #     func.__name__, user.wk, user.user_type))

            # request_backup.info(str(body))

            return func(*args, **kwargs, user=user)

            # if user_type == -1 or user.user_type <= user_type:
            #     return func(*args, **kwargs, user=user)
            # else:
            #     return parse_info({'message': 'user_type failed'})

        return inner_wrapper

    return wrapper


class UserManager(object):

    @staticmethod
    def get_user(wckey=None):
        """     
        :param wckey:
        :return: user
        """
        if None:
            return None

        user_key = Sessions.objects.get(session_data=wckey)
        user = User.objects.get(open_id=user_key.session_key)

        return user

    @staticmethod
    def get_user_info(user):
        """
        :param user:
        :return: name,avatar_links
                and base64(user.wk)
        """
        result = {}

        if user.is_bind == 0:
            profile = UserProfile.objects.get(open_id=user)
            result['is_bind'] = 0
            result['name'] = profile.name
            result['subject'] = profile.subject
            result['grade'] = profile.grade
        else:
            result['is_bind'] = 1

        return result

    @staticmethod
    def get_user_key(user):
        return UserProfile.objects.get(open_id=user).ecard_key


class WechatSdk(object):
    __Appid = 'wx5c7d55175f3872b7'
    __SECRET = '6050b3ca9c9b3823768ae1867ef9036e'
    """
    WechatSdk
    Based on Wechat user code
    """
    openid = ''
    wxsskey = ''

    def __init__(self, code):
        super(WechatSdk, self).__init__()
        self.code = code

    @staticmethod
    def gen_hash():
        """
        gen_hash as session data.
        The repetition should be a very small probability event,
        and from a statistical point of view, the probability is zero.
        Return a string of length 64.
        """
        return sha256(os.urandom(24)).hexdigest()

    def get_openid(self):
        params = {
            'appid': self.__Appid,
            'secret': self.__SECRET,
            'js_code': self.code,
            'grant_type': 'authorization_code'
        }

        try:
            data = requests.get(
                'https://api.weixin.qq.com/sns/jscode2session', params=params)
        except Exception as e:
            app.error(str(e) + '\tcode:' + str(self.code))
            return False

        info = data.json()
        # print(info)
        if 'openid' not in info:
            app.info('parameter \'{}\' error'.format(self.code))
            if settings.DEBUG:
                info = {
                    'openid': self.code,
                    'session_key': 'SESSIONKEY',
                }
            else:
                return False

        self.openid = info['openid']
        self.wxsskey = info['session_key']

        app.info(self.code + ':\t' + self.openid)

        return True

    def save_user(self):
        have_user = User.objects.filter(open_id=self.openid)
        if have_user.exists():
            # 已注册过
            return self.flush_session()

        sess = WechatSdk.gen_hash()

        Sessions(session_key=self.openid,
                 session_data=sess,
                 we_ss_key=self.wxsskey,
                 expire_date=datetime.now() + timedelta(30)).save()

        user = User(open_id=self.openid)
        user.save()
        # 自动为用户生成Profile
        # Profile(wk=user).save()

        # 注册成功，分配cookie
        return {'sess': sess,
                'code': ASEC.REG_SUCCESS,
                'message': ASEC.getMessage(ASEC.REG_SUCCESS)}

    def flush_session(self):
        try:
            this_user = Session.objects.get(session_key=self.openid)
        except Exception as e:
            this_user = Session()        

        sess = WechatSdk.gen_hash()

        this_user.we_ss_key = self.wxsskey
        this_user.session_data = sess
        this_user.expire_date = datetime.now() + timedelta(30)
        this_user.save()

        # 刷新Cookie成功
        return {'sess': sess,
                'code': ASEC.FLUSH_SESSION_SUCCESS,
                'message': ASEC.getMessage(ASEC.FLUSH_SESSION_SUCCESS)}


class LoginManager(object):
    TOKEN = '031r987y7p!3'

    def __init__(self, user):
        super(LoginManager, self).__init__()
        self.user = user

    def __str__(self):
        return self.user

    def check(self, sign, checktime):
        if time.time() - int(checktime) > 5:
            return False

        to_check_str = str(self.TOKEN) + str(checktime)
        to_check_str = to_check_str.encode('utf-8')

        m = md5()
        m.update(to_check_str)

        cc_str = m.hexdigest()
        del m
        if settings.DEBUG:
            return True
        else:
            return cc_str == sign

    @staticmethod
    def gen_base64(txt):
        tmp = base64.b64encode(str(txt).encode('utf-8'))
        return str(tmp, 'utf-8')

    def reply(self):
        user = self.user
        user.last_login = datetime.now()
        user_info = UserManager.get_user_info(user)
        user.save()

        return {'code': ASEC.LOGIN_SUCCESS,
                'info': user_info,
                'message': ASEC.getMessage(ASEC.LOGIN_SUCCESS)}


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

        user = UserProfile(open_id=self.user,
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

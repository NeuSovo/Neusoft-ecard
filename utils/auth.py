import time
import json
import logging
from utils.models import *
from utils.tools import *
from django.http import JsonResponse
from datetime import datetime, timedelta
from utils.apps import APIServerErrorCode as ASEC


app = logging.getLogger('app.custom')
request_backup = logging.getLogger('app.backup')


def parse_info(data):
    """
    parser_info:
    param must be a dict
    parse dict data to json,and return HttpResponse
    """
    return JsonResponse(data)


def usercheck(user_type=-1):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            result = {}
            request = args[0] 

            action = kwargs.get('action', None) or 'None'

            try:
                body = json.loads(request.body)
                wckey = body['base_req']['wckey']
            except:
                result['code'] = ASEC.ERROR_PARAME
                result['message'] = ASEC.getMessage(ASEC.ERROR_PARAME)
                response = parse_info(result)
                response.status_code = 400

                return response

            if redis_session.exists(wckey):
                wk = redis_session.get(wckey).decode('utf-8')
            else:
                result['code'] = ASEC.SESSION_NOT_WORK
                result['message'] = ASEC.getMessage(ASEC.SESSION_NOT_WORK)
                return parse_info(result)            

            user = User.objects.get(wk=str(wk))

            app.info("[{}][{}][{}][{}]".format(
                func.__name__, user.wk, action, user.user_type))

            request_backup.info(str(body))

            if user_type == -1 or user.user_type <= user_type:
                return func(*args, **kwargs, user=user, body=body)
            else:
                return parse_info({'message': 'user_type failed'})

        return inner_wrapper

    return wrapper


class WechatSdk(object):

    """
    WechatSdk
    Based on Wechat user code
    """
    openid = ''
    wxsskey = ''

    def __init__(self, code):
        super(WechatSdk, self).__init__()
        self.code = code

    def check(self):
        res = get_openid(self.code)
        if res:
            self.openid = res['openid']
            self.wxsskey = res['session_key']
            return True
        else:
            return False

    def save_user(self):
        have_user = User.objects.filter(wk=self.openid)
        if have_user.exists():
            # 已注册过
            return self.flush_session()

        sess = gen_hash()
        redis_session.set(sess,self.openid,ex=259200)
        user = User(wk=self.openid)
        user.save()
        # 自动为用户生成Profile
        # Profile(wk=user).save()

        # 注册成功，分配cookie
        return {'sess': sess,
                'code': ASEC.REG_SUCCESS,
                'message': ASEC.getMessage(ASEC.REG_SUCCESS)}

    def flush_session(self):
        sess = gen_hash()
        redis_session.set(sess,self.openid,ex=259200)
        # 刷新Cookie成功
        return {'sess': sess,
                'code': ASEC.FLUSH_SESSION_SUCCESS,
                'message': ASEC.getMessage(ASEC.FLUSH_SESSION_SUCCESS)}


class LoginManager(object):
    TOKEN = 'eq021n!3'

    def __init__(self, user):
        super(LoginManager, self).__init__()
        self.user = user

    def __str__(self):
        return self.user

    def check(self, sign, checktime):
        if time.time() - int(checktime) > 5:
            return False

        check_str = en_md5(str(self.TOKEN) + str(checktime))

        if settings.DEBUG:
            return True
        else:
            return check_str == sign

    def reply(self):
        user = self.user
        user.last_login = datetime.now()
        user_info = UserManager.get_user_info(user)

        if not settings.DEBUG:
            user_info['qrcode'] = 'https://wash.wakefulness.cn/tools/qrcode/' + \
                                  user_info['qrcode']
        user.save()

        return {'code': ASEC.LOGIN_SUCCESS,
                'user_type': user.user_type,
                'info': user_info,
                'message': ASEC.getMessage(ASEC.LOGIN_SUCCESS)}


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

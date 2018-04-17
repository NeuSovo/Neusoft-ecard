import json
from utils.auth import WechatSdk, LoginManager, usercheck
from django.shortcuts import render
from django.http import JsonResponse

from utils.apps import APIServerErrorCode as ASEC
# Create your views here.
def parse_info(data):
    """
    parser_info:
    :param data must be a dict
    :return dict data to json,and return HttpResponse
    """
    return JsonResponse(data)


def register_view(request):
    """
    view for register
    Accept the code from WeChat, and register this user on the server
    return body :{code,message}
           headers:wckey
    """
    result = {}
    if 'code' not in request.GET:
        result['code'] = ASEC.ERROR_PARAME
        result['message'] = ASEC.getMessage(ASEC.ERROR_PARAME)
        response = parse_info(result)
        response.status_code = 400
        return response

    # update 2018/03/07
    # request.GET['name'],request.GET['url'])
    wk = WechatSdk(request.GET['code'])
    if not wk.check():
        result['code'] = ASEC.WRONG_PARAME
        result['message'] = ASEC.getMessage(ASEC.WRONG_PARAME)
        response = parse_info(result)
        return response

    result = wk.save_user()
    if 'sess' not in result:
        response = parse_info(result)
        return response

    sess = result['sess']

    response = parse_info(result)
    response.set_cookie('wckey', sess)

    return response


@usercheck()
def login_view(request, user, body=None):
    """
    view for login
    Accept User Cookies and return user info,
    This interface must Verify sign.
    :param request:
            sign : md5 (time + Token)
            time : now time and 6s effective
    :param user:
    :return: user_type,user_info
    """

    result = {}
    login = LoginManager(user=user)

    if login.check(sign=body['sign'],
                   checktime=body['time']):
        result = login.reply()
        response = parse_info(result)

        return response
    else:
        result['code'] = ASEC.CHECK_USER_FAILED
        result['message'] = ASEC.getMessage(ASEC.CHECK_USER_FAILED)
        response = parse_info(result)

        return response

import json
from django.shortcuts import HttpResponse
from ecard.apps import APIServerErrorCode as ASEC
from ecard.handle import (usercheck,WechatSdk,LoginManager,EcardManager)
# Create your views here.

def parse_info(data):
    """
    parser_info:
    :param data must be a dict
    :return dict data to json,and return HttpResponse
    """
    return HttpResponse(json.dumps(data, indent=4),
                        content_type="application/json")


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

    wk = WechatSdk(request.GET['code'])
    if not wk.get_openid():
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
def login_view(request, user):
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
    body = json.loads(request.body)
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


@usercheck()
def card_view(request, action, user):
    response = ''
    body = json.loads(request.body)
    response = parse_info({'message': 'failed'})

    result = EcardManager(postdata=body, user=user)

    if action == 'bind':
        response = parse_info(result.bind_card())

    if action == 'balance':
        response = parse_info(result.balance_card())

    if action == 'detail':
        response = parse_info(result.detail_card())

    return response



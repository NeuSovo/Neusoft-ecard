# coding:utf-8
from django.template.loader import render_to_string
from django.shortcuts import render, HttpResponse
# Create your views here.
from .models import Ecard, Sessions
from .demo import getB, getD
from .checkuser import getOpenid, gen3rdkey
import json
import logging

logger = logging.getLogger('django')

def index(request):
    return HttpResponse('It worked!')

def help_info(request):
    return render(request,'info.html')


def check(request):
    try:
        code = request.GET['code']
    except:
        logger.info('No request code')
        return HttpResponse(json.dumps({'code': '99999',
                                        'message': 'failed'}, indent=4),
                            content_type="application/json")
    data = getOpenid(code)
    if 'openid' not in data:
        logger.warn('{} is is wrong'.format(code))
        return HttpResponse(json.dumps({'code': '99999',
                                        'message': 'failed'}, indent=4),
                            content_type="application/json")

    have_user = Ecard.objects.filter(wechat_key=data['openid'])

    # data = {'openid': code, 'session_key': code}
    # have_user = ''

    if len(have_user) != 0:
        logger.warn('This user {} has been bound'.format(data['openid']))
        return HttpResponse(json.dumps({'code': '10001',
                                        'message': 'failed'}, indent=4),
                            content_type="application/json")
    else:
        rdkey = gen3rdkey()
        this_user = Sessions(rd_session=rdkey,
                             open_id=data['openid'],
                             sess_key=data['session_key'])

        this_user.save()
        ecard_user = Ecard(wechat_key=data['openid'])
        ecard_user.save()

        response = HttpResponse(json.dumps({'code': '10000',
                                            'message': 'Success'}, indent=4),
                                content_type="application/json")
        response.set_cookie('rdkey',rdkey)
        response['rdkey'] = rdkey

        logger.info('{} Bind success'.format(data['openid']))
        return response


def recheck(request):
    if 'code' not in request.GET:
        logger.info('No request code')
        return HttpResponse(json.dumps({'code': '99999',
                                        'message': 'failed'}, indent=4),
                            content_type="application/json")

    code = request.GET['code']
    data = {}
    data = getOpenid(code)

    if code =='debug':
        logger.info('debug is run')
        data['openid'] = 'test'

    if 'openid' not in data:
        logger.warn('{} is is wrong'.format(code))
        return HttpResponse(json.dumps({'code': '99999',
                                        'message': 'failed'}, indent=4),
                            content_type="application/json")

    open_id = data['openid']

    # open_id = 'test'

    have_user = Sessions.objects.filter(open_id=open_id)
    if len(have_user) == 0:
        logger.warn('{} Not yet bound'.format(open_id))
        return HttpResponse(json.dumps({'code': '99999',
                                        'message': 'failed'}, indent=4),
                            content_type="application/json")

    this_user = Sessions.objects.get(open_id=open_id)
    # print (this_user.open_id)

    rdkey = gen3rdkey()
    this_user.rd_session = rdkey
    this_user.save()

    response = HttpResponse(json.dumps({'code': '10002',
                                        'message': 'Success'}, indent=4),
                            content_type="application/json")

    response.set_cookie('rdkey',rdkey,3600)
    response['rdkey'] = rdkey

    logger.info('{} recheck success'.format(open_id))
    return response


def Bind(request):
    if 'ek' not in request.GET:
        logger.info('No request ek')
        return HttpResponse(json.dumps({'code': '99999',
                                        'message': 'failed'}, indent=4),
                            content_type="application/json")

    ek = request.GET['ek']

    try:
        sess = request.COOKIES['rdkey']
    except:
        logger.warn('{} corresponding session expired or not available'.format(ek))
        return HttpResponse(json.dumps({'code': '10003',
                                        'message': 'failed'}, indent=4),
                            content_type="application/json")

    this_user = Sessions.objects.filter(rd_session=sess)

    if len(this_user) == 0:
        logger.warn('{} corresponding session expired or not available'.format(ek))
        return HttpResponse(json.dumps({'code': '10003',
                                        'message': 'failed'}, indent=4),
                            content_type="application/json")

    if len(Ecard.objects.filter(ecard_key=ek)) != 0:
        logger.warn('{} Try the second binding '.format(ek))
        return HttpResponse(json.dumps({'code': '10004',
                                        'message': 'failed'}, indent=4),
                            content_type="application/json")

    this_user = Sessions.objects.get(rd_session=sess)

    this_ek = Ecard.objects.get(wechat_key=this_user.open_id)

    this_ek.ecard_key = ek
    this_ek.save()

    logger.info('{} bind Success'.format(ek))
    response = HttpResponse(json.dumps({'code': '10005',
                                        'message': 'Success'}, indent=4),
                            content_type="application/json")

    return response


def rebind(request):
    pass


def getBalance(request):
    try:
        sess = request.COOKIES['rdkey']
    except:
        logger.warn('no request sess ')
        sess = 'null'

    data = {}
    this_user = Sessions.objects.filter(rd_session=sess)
    if len(this_user) == 0:
        logger.warn('Corresponding session expired or not available')
        return HttpResponse(json.dumps({'code': '10003',
                                        'message': 'failed'}, indent=4),
                            content_type="application/json")

    this_user = Sessions.objects.get(rd_session=sess)
    this_ek = Ecard.objects.get(wechat_key=this_user.open_id)

    if this_ek.ecard_key == 'NULL':
        logger.warn('{} no Bind ek'.format(this_user.open_id))
        return HttpResponse(json.dumps({'code': '10001',
                                        'message': 'failed'}, indent=4),
                            content_type="application/json")

    data['info'] = getB(this_ek.ecard_key)
    if data:
        data['code'] = '10006'
        data['message'] = 'Success'
        logger.info('{} get balance ok'.format(this_ek.ecard_key))
    else:
        data['code'] = '10007'
        data['message'] = 'failed'

    response = HttpResponse(json.dumps(data, indent=4,ensure_ascii = False),
                            content_type="application/json")
    return response


def getDetail(request):
    try:
        sess = request.COOKIES['rdkey']
    except:
        logger.warn('no request sess ')
        sess = 'null'

    this_user = Sessions.objects.filter(rd_session=sess)
    if len(this_user) == 0:
        logger.warn('Corresponding session expired or not available')
        return HttpResponse(json.dumps({'code': '10003',
                                        'message': 'failed'}, indent=4),
                            content_type="application/json")

    this_user = Sessions.objects.get(rd_session=sess)
    this_ek = Ecard.objects.get(wechat_key=this_user.open_id)

    if 'month' in request.GET:
        month = request.GET['month']
    else:
        month = ''

    if this_ek.ecard_key == 'NULL':
        logger.warn('{} no Bind ek'.format(this_ek.wechat_key))
        return HttpResponse(json.dumps({'code': '10001',
                                        'message': 'failed'}, indent=4),
                            content_type="application/json")

    data = getD(this_ek.ecard_key, month)
    if data['info']:
        data['code'] = '10008'
        data['message'] = 'Success'

    else:
        data['code'] = '10009'
        data['message'] = 'Success'

    response = HttpResponse(json.dumps(data, indent=4,ensure_ascii = False),
                            content_type="application/json")

    logger.info('{} get detail ok'.format(this_ek.ecard_key))
    return response

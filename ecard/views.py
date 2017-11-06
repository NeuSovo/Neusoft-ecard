# coding:utf-8
from django.shortcuts import render, HttpResponse
# Create your views here.
from .models import Ecard, Sessions
from .demo import getB, getD
from .checkuser import getOpenid, gen3rdkey
import json

#
# code : 10000 -> ���û��ɹ���û�а�
#        10001 -> �Ѱ󶨴��û�����û�а�
#        10002 -> Session ���³ɹ�
#        10003 -> Session ������ ��Ҫִ��recheck
#        10004 -> �󿨵�ʱ�򣬿�Ƭ�����˰�
#        10005 -> �󿨳ɹ�
#        10006 -> ��ȡ���ɹ�
#        10007 -> ��ȡ���ʧ��,���ܿ�ƬʧЧ,��Ҫ���°�
#        10008 -> ��ȡ��Ϣ�ɹ�
#
#
#

def index(request):
    return HttpResponse('It worked!')


def check(request):
    code = request.GET['code']
    # data = getOpenid(code)
    # have_user = Ecard.objects.filter(wechat_key=data['openid'])
    data = {'openid':'1','session_key':'2'}
    have_user = ''
    if len(have_user) != 0:
        return HttpResponse(json.dumps({'code': '10001',
                                        'message': 'failed'}),
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
                                            'message': 'Success'}),
                                content_type="application/json")

        response.set_cookie('3rdkey', rdkey)

        return response


def recheck(request):
    code = request.GET['code']
    data = getOpenid(code)
    open_id = data['openid']
    this_user = Sessions.objects.get(open_id=open_id)
    rdkey = gen3rdkey()
    this_user.rd_session = rdkey
    this_user.save()

    response = HttpResponse(json.dumps({'code': '10002',
                                        'message': 'Success'}),
                            content_type="application/json")

    response.set_cookie('3rdkey', rdkey)

    return response



def Bind(request):
    ek = request.GET['ek']
    sess = request.COOKIES['3rdkey']
    this_user = Sessions.objects.filter(rd_session=sess)
    if len(this_user) == 0:
        return HttpResponse(json.dumps({'code': '10003',
                                        'message': 'failed'}),
                            content_type="application/json")

    if len(Ecard.objects.filter(ecard_key=ek)) != 0:
        return HttpResponse(json.dumps({'code': '10004',
                                        'message': 'failed'}),
                            content_type="application/json")

    this_user = Sessions.objects.get(rd_session=sess)

    this_ek = Ecard.objects.get(wechat_key=this_user.open_id)

    this_ek.ecard_key = ek
    this_ek.save()
    response = HttpResponse(json.dumps({'code': '10005',
                                        'message': 'Success'}),
                            content_type="application/json")

    return response


def getBalance(request):
    sess = request.COOKIES['3rdkey']
    data = {}
    this_user = Sessions.objects.filter(rd_session=sess)
    if len(this_user) == 0:
        return HttpResponse(json.dumps({'code': '10003',
                                        'message': 'failed'}),
                            content_type="application/json")

    this_user = Sessions.objects.get(rd_session=sess)
    this_ek = Ecard.objects.get(wechat_key=this_user.open_id)

    data['info'] = getB(this_ek.ecard_key)
    if data:
        data['code'] = '10006'
        data['message'] = 'Success'
    else:
        data['code'] = '10007'
        data['message'] = 'failed'

    response = HttpResponse(json.dumps(data),
                                content_type="application/json")
    return response


def getDetail(request):
    sess = request.COOKIES['3rdkey']

    this_user = Sessions.objects.filter(rd_session=sess)
    if len(this_user) == 0:
        return HttpResponse(json.dumps({'code': '10003',
                                        'message': 'failed'}),
                            content_type="application/json")

    this_user = Sessions.objects.get(rd_session=sess)
    this_ek = Ecard.objects.get(wechat_key=this_user.open_id)

    if 'month' in request.GET:
        month = request.GET['month']
    else:
        month = ''

    data = getD(this_ek.ecard_key, month)
    if data:
        data['code'] = '10008'

    else:
        data['code'] = '10009'

    response = HttpResponse(json.dumps(data),
                             content_type="application/json")

    return response

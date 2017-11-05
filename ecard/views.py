from django.shortcuts import render, HttpResponse
# Create your views here.
from .models import Ecard,Sessions
from .demo import getB, getD
from .checkuser import getOpenid,gen3rdkey
import json

#
# code : 10000 -> 绑定用户成功，没有绑卡
#        10001 -> 已绑定此用户，但没有绑卡
#
#



def firstrun(request):
    code  = request.GET['code']
    data = getOpenid(code)
    have_user = Ecard.objects.filter(wechat_key=data['openid'])
    if len(have_user) != 0:
        return HttpResponse(json.dumps({'code':'10001','message':'The id is exist'}), content_type="application/json")
    else:
        rdkey = gen3rdkey()
        this_user = Sessions(rd_session=rdkey,open_id = data['openid'],sess_key = data['session_key'])
        this_user.save()
        ecard_user = Ecard(wechat_key = data['openid'])
        ecard_user.save()
        return HttpResponse(json.dumps({'code':'10000','message':'Success','3rdkey':rdkey}), content_type="application/json")


def Bind(request):
    sess = request.GET['sess']
    ek = request.GET['ek']

    this_user = Sessions.objects.filter(rd_session=sess)
    if len(this_user) == 0:
        return HttpResponse(json.dumps({'code':'10003','message':'The Sessions not work'}), content_type="application/json")

    if len(Ecard.objects.filter(ecard_key = ek)) != 0:
        return HttpResponse(json.dumps({'code':'10004','message':'The ecard_key is exist'}), content_type="application/json")

    this_user = Sessions.objects.get(rd_session=sess)
    this_ek = Ecard.objects.get(wechat_key = this_user.open_id)

    this_ek.ecard_key = ek
    this_ek.save()
    return HttpResponse(json.dumps({'code':'10005','message':'Success'}), content_type="application/json")


def getBalance(request):
    sess = request.GET['sess']
    this_user = Sessions.objects.get(rd_session=sess)
    this_ek = Ecard.objects.get(wechat_key = this_user.open_id)

    data = getB(this_ek.ecard_key)
    print (len(data))
    data['code'] = 'Success'
    return HttpResponse(json.dumps(data), content_type="application/json")


def getDetail(request):
    sess = request.GET['sess']
    this_user = Sessions.objects.get(rd_session=sess)
    this_ek = Ecard.objects.get(wechat_key = this_user.open_id)

    if 'month' in request.GET:
        month = request.GET['month']
    else:
        month = ''

    data = getD(this_ek.ecard_key,month)
    data['code'] = 'Success'
    return HttpResponse(json.dumps(data), content_type="application/json")

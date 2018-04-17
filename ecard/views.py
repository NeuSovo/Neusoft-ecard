import json
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from ecard.handle import EcardManager
from utils.auth import usercheck
# Create your views here.

def parse_info(data):
    """
    parser_info:
    :param data must be a dict
    :return dict data to json,and return HttpResponse
    """
    return JsonResponse(data)


@usercheck()
def card_view(request, action, user, body=None):
    response = ''
    response = parse_info({'message': 'failed'})

    ecard = EcardManager(postdata=body, user=user)
    try:
        method_name = action + '_card'
        result = getattr(ecard, method_name)
    except AttributeError as e:
        response = HttpResponse()
        response.status_code = 404
        return response

    response = parse_info(result())
    return response

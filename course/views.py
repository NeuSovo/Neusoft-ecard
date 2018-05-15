import json

from django.http import JsonResponse
from django.shortcuts import render

from utils.auth import usercheck
from course.handle import ClassRoom
# Create your views here.


def parse_info(data):
    """
    parser_info:
    :param data must be a dict
    :return dict data to json,and return HttpResponse
    """
    return JsonResponse(data)


@usercheck()
def room_view(request, user=None, action=None, body=None):
    response = ''
    room = ClassRoom(body=body)

    try:
        method_name = action + '_room'
        result = getattr(room, method_name)
    except AttributeError as e:
        response = HttpResponse()
        response.status_code = 404
        return response

    response = parse_info(result())
    return response

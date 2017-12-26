import json
# import
from django.shortcuts import render, HttpResponse
# Create your views here.


def parse_info(data):
    return HttpResponse(json.dumps(data, indent=4),
                        content_type="application/json")


def get_empty_class(request):
    """docs
    空课表
    params:
        floor: 楼号
        week: 周几[0-6]
    return:
        code:
        message:
        info:[
            {
            'roomid':
            'time':[12,34,56,78,90]
            },
        ]        
    """

    # do someting
    # 数据可以被缓冲
    # 临时数据

    result = {
        'code': '0000',
        'message': 'success',
        'info': [{'roomid': 'A1-123', 'time': '12'}]
    }
    response = parse_info(result)

    return response


def rub_class(request):
    """docs
    蹭课
    params:
        title: 课程名
    return:
        code:
        message:
        info:[
            {
            'title':课程名,
            'week':周几,
            'time':[12,34,56,78,90],
            'teacher':教师名,
            'class':上课班级, # 暂时pass
            'stucount':上课人数
            },
        ]        
    """

    # do someting

    # 临时数据
    result = {
        'code': '00000',
        'message': 'success',
        'info': [
            {
                'title': '软件工程',
                'week': '2',
                'time': '34',
                'teacher': 'zz',
                # 'class':上课班级, # 暂时不加
                'stucount': 60
            },
            {
                'title': '软件工程',
                'week': '2',
                'time': '56',
                'teacher': 'zz',
                # 'class':上课班级, # 暂时不加
                'stucount': 30
            },
        ]
    }

    response = parse_info(result)

    return response


def rub_teachter(request):
    """docs
    蹭老师
    params:
        teacher: 老师名
    return:
        code:
        message:
        info:[
            {
            'title':课程名,
            'week':0,
            'time':[12,34,56,78,90],
            'teacher':教师名,
            'class':上课班级, # 暂时pass
            'stucount':上课人数
            },
        ]        
    """

    # do someting

    # 临时数据
    result = {
        'code': '00000',
        'message': 'success',
        'info': [
            {
                'title': 'Java',
                'week': '2',
                'time': '12',
                'teacher': 'zz',
                # 'class':上课班级, # 暂时不加
                'stucount': 60
            },
            {
                'title': 'Java',
                'week': '2',
                'time': '34',
                'teacher': 'zz',
                # 'class':上课班级, # 暂时不加
                'stucount': 60
            },
        ]
    }

    response = parse_info(result)

    return response


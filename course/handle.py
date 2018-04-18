import random
from datetime import datetime
from django.db.models import Q
from django.http import JsonResponse

from course.models import *
from utils.tools import redis_global


class ClassRoom(object):
    """docstring for ClassRoom"""

    def __init__(self, body):
        self.date = body.get('date', datetime.now().strftime("%Y%m%d"))
        self.classname = body.get('class', '0')
        self.teacher = body.get('teacher', '0')
        self.floor = body.get('floor', 'A')
        self.bdate = body.get('bdate', 1)
        self.edate = body.get('edate', 6)
        self.grade = body.get('grade', '无')

    def er_room(self):
        now_week = datetime.strptime(str(self.date), '%Y%m%d').isocalendar()
        all_class = RoomTest.objects.filter(
            Q(RoomID__startswith=self.floor), Q(ClassTimeWeek=now_week[2]))

        def handle_date(date, week):
            res = []
            for i in date.split(','):
                l = [int(i) for i in i.split('-')]
                b, e = l[0], l[len(l)-1] + 1
                res += list(range(b, e))
            return week in res

        def command(floor='A'):
            all_room = {}
            a = RoomTest.objects.raw(
                "select 1 as id,RoomID from course_roomtest where RoomID like '{}%%' group by RoomId ".format(floor))
            for i in a:
                all_room[i.RoomID] = [True, True, True, True, True]

            return all_room

        all_room = command(self.floor)
        for i in all_class.iterator():
            if (handle_date(i.ClassWeek, now_week[1]-9)):
                for tt in i.ClassTimeTime.split('-'):
                    all_room[i.RoomID][int(tt)-1] = False
        info = []
        for item in all_room:
            for index, flag in enumerate(all_room[item]):
                if flag and (index + 1 >= int(self.bdate)) and (index + 1 <= int(self.edate)):
                    info.append({
                        'RoomID': item,
                        'RoomTime': index + 1
                    })

        return {'message': 'ok',
                'info': info,
                'date': self.date}

    def getclass_room(self):
        info = []
        allclass = RoomTest.objects.filter(ClassName__icontains=self.classname)
        for i in allclass.iterator():
            info.append(i.info(has_grade=True))

        return {'message': 'ok', 
                'info': info}

    def getteacher_room(self):
        info = []
        allteacher = RoomTest.objects.filter(ClassTeacher=self.teacher)
        for i in allteacher.iterator():
            info.append(i.info(has_grade=True))

        return {'message': 'ok',
                'info': info}

    def getgrade_room(self):
        info = []
        allcalss = RoomTest.objects.raw(
            "select id from course_roomtest where ClassGrade like '%%{}%%'".format(self.grade))

        def get_info(id):
            return RoomTest.objects.get(id=id).info()
        result = {
            'message': 'ok',
            'info': [get_info(i.id) for i in allcalss]
        }
        return result

    def allclass_room(self):
        info = []
        key = 'allclass_'
        if redis_global.exists(key):
            return eval(redis_global.get(key))
        allclass = RoomTest.objects.raw(
            "select 1 as id,ClassName from course_roomtest group by ClassName")

        for i in allclass:
            info.append(i.ClassName)

        result = {
            'message': 'ok',
            'info': info
        }
        redis_global.set(key, result, ex=600)
        return result

    def allteacher_room(self):
        info = []
        key = 'allteacher_'
        if redis_global.exists(key):
            return eval(redis_global.get(key))
        allteacher = RoomTest.objects.raw(
            "select 1 as id,ClassTeacher from course_roomtest group by ClassTeacher")

        for i in allteacher:
            info.append(i.ClassTeacher)
        result = {'message': 'ok',
                  'info': info}
        redis_global.set(key, result, ex=600)
        return result

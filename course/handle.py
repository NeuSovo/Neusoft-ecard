import random
from datetime import datetime
from django.http import JsonResponse
from course.models import *
from utils.tools import redis_global
class ClassRoom(object):
    """docstring for ClassRoom"""
    def __init__(self, body):
        self.date = body.get('date','20180409')
        self.classname = body.get('class','0')
        self.teacher = body.get('teacher','0')
        self.floor = body.get('floor','A7')

    def er_room(self):
        now_week = datetime.strptime(str(self.date), '%Y%m%d').isocalendar()
        all_class = RoomModel.objects.filter(RoomFloor='{}  '.format(self.floor))
        
        def handle_date(date,week):
            res = []
            for i in date.split(','):
                l = [int(i) for i in i.split('-')]
                b,e = l[0],l[len(l)-1] + 1
                res += list(range(b,e))
            return week in res

        def command(floor='A7'):
            all_room = {}
            a = RoomModel.objects.raw("select 1 as id,RoomId as RoomId from course_roommodel where RoomFloor='{}  ' group by RoomId".format(floor))
            for i in a:
                all_room[i.RoomId] = [True,True,True,True,True]
        
            return all_room

        all_room = command(self.floor)
        for i in all_class.iterator():
            if (handle_date(i.ClassTime,now_week[1]-9) and i.RoomWeek == now_week[2]):
                all_room[i.RoomID][i.RoomTime-1] = False
        info = []
        for item in all_room:
            for index,flag in enumerate(all_room[item]):
                if flag:
                    info.append({
                        'RoomID':item,
                        'RoomTime': index + 1
                    })

        return {'message':'ok',
                'info': info,
                'date': self.date}

    def getclass_room(self):
        info = []
        allclass = RoomModel.objects.filter(ClassName=self.classname)
        for i in allclass.iterator():
            info.append(i.info())

        return {'message': 'ok',
                'info': info}

    def getteacher_room(self):
        info = []
        allteacher = RoomModel.objects.filter(ClassTeacher=self.teacher)
        for i in allteacher.iterator():
            info.append(i.info())

        return {'message': 'ok',
                'info': info}

    def allclass_room(self):
        info = []
        allclass = RoomModel.objects.raw("select 1 as id,ClassName from course_roommodel group by ClassName")
        for i in allclass:
            info.append(i.ClassName)
        return {'message': 'ok',
                'info': info}

    def allteacher_room(self):
        info = []
        allteacher = RoomModel.objects.raw("select 1 as id,ClassTeacher from course_roommodel group by ClassTeacher")
        for i in allteacher:
            info.append(i.ClassTeacher)
        return {'message': 'ok',
                'info': info}

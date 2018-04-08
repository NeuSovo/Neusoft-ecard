import random
from django.http import JsonResponse
from course.models import *
class ClassRoom(object):
    """docstring for ClassRoom"""
    def __init__(self, body):
        self.date = body.get('date','0')
        self.classname = body.get('class','0')
        self.teacher = body.get('teacher','0')

    def er_room(self):
        if int(self.date) <= 0:
            return {'message': 'failed'}
        info = [
            {'RoomID':'A7-213',
             'RoomTotalSeatNum': random.randint(30,100),
             'RoomTime': random.randint(1,5)},
            {'RoomID':'A6-203',
             'RoomTotalSeatNum': random.randint(30,100),
             'RoomTime': random.randint(1,5)},
            {'RoomID':'A5-204',
             'RoomTotalSeatNum': random.randint(30,100),
             'RoomTime': random.randint(1,5)},
            {'RoomID':'A5-210',
             'RoomTotalSeatNum': random.randint(30,100),
             'RoomTime': random.randint(1,5)},
            {'RoomID':'A2-209',
             'RoomTotalSeatNum': random.randint(30,100),
             'RoomTime': random.randint(1,5)},
            {'RoomID':'A1-207',
             'RoomTotalSeatNum': random.randint(30,100),
             'RoomTime': random.randint(1,5)},
            ]
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


def command():
    roompool = RoomModel.objects.all()

    for i in roompool.iterator():
        i.ClassTime = i.ClassTime[1:]
        i.save()
        print (i.ClassTime)
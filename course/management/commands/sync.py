import os
import re
from bs4 import BeautifulSoup as bf
from django.core.management.base import BaseCommand, CommandError
from course.models import RoomTest
all_time = {
    '1-2节]': '1',
    '3-4节]': '2',
    '5-6节]': '3',
    '7-8节]': '4',
    '9-10节]': '5',
    '9-11节]': '5',
    '1-4节]': '1-2',
    '1-8节]': '1-2-3-4',
    '5-7节]':'3-4',
    '5-8节]': '3-4',
    '1-2节]双': '1',
    '1-2节]单': '1',
    '3-4节]单': '2',
    '3-4节]双': '2',
    '1-4节]单': '1-2',
    '1-4节]双': '1-2',
    '5-6节]单': '3',
    '5-6节]双': '3',
    '7-8节]单': '4',
    '7-8节]双': '4',
    '5-7节]单': '3-4',
    '5-8节]单': '3-4',
    '5-8节]双': '3-4',
    '1-8节]单':'1-2-3-4',
    '1-8节]双':'1-2-3-4',
    '9-10节]双': '5',
    '9-10节]单': '5',
    '9-11节]单': '5',
    '9-11节]双': '5',
    '1-10节]' : '1-2-3-4-5',
    '1-10节]单': '1-2-3-4-5',
    '1-10节]双': '1-2-3-4-5',
    '1-11节]': '1-2-3-4-5',
    '1-11节]单': '1-2-3-4-5',
    '1-11节]双': '1-2-3-4-5'
}
all_week = {
    '一':1,
    '二':2,
    '三':3,
    '四':4,
    '五':5,
    '六':6,
    '日':7,
}
def  deal_tmp_info(info, RoomId=None, normal=True) -> dict:
    result = []
    for i in info.select('tr')[1:]:
        all_table = i.find_all('td')
        if not normal:
            ClassName = all_table[0].get_text().strip()
            ClassTeacher = all_table[7].get_text().strip()
            ClassWeek = all_table[11].get_text().lstrip().rstrip()
            ClassTime = all_table[12].get_text().strip().split('[')
        else:
            ClassWeek = all_table[0].get_text()
            ClassTime = all_table[1].get_text().split('[')
            ClassName = all_table[2].get_text()
            ClassTeacher = all_table[3].get_text()
        if ClassName != '':
            result.append({'RoomId': RoomId,
                           'ClassName':ClassName, 
                           'ClassTeacher': ClassTeacher, 
                           'ClassWeek': ClassWeek,
                           'ClassCount': 0,
                           'ClassGrade': '0',
                           'ClassTimeWeek': all_week[ClassTime[0]],
                           'ClassTimeTime': all_time[ClassTime[1]]})    
    return result

def deal(info, get_tmp=False) -> dict:
    result = tmp_result = []
    soup = bf(info,'lxml')
    allinfo = soup.select('table')
    try:
        table_title = allinfo[1]
        class_info = allinfo[2]
        if get_tmp:
            calss_tmp_info = allinfo[4]
            try:
                RoomId = re.findall(r'教室：教学楼(.*)', table_title.get_text())[0]
            except:
                RoomId = re.findall(r'教室：图书馆(.*)', table_title.get_text())[0]
            tmp_result = deal_tmp_info(calss_tmp_info, RoomId, normal=True)
    except Exception as e:
        if get_tmp:
            table_title = allinfo[0]
            calss_tmp_info = allinfo[1]
            RoomId = re.findall(r'教学楼(.*)临时活动安排', table_title.get_text())
            if len(RoomId) !=0:
                tmp_result = deal_tmp_info(calss_tmp_info, RoomId[0])
            else:
                return tmp_result
        else:
            return

    if get_tmp:
        return tmp_result

    try:
        RoomId = re.findall(r'教室：教学楼(.*)', table_title.get_text())[0]
    except Exception as e:
        try:
            RoomId = re.findall(r'教室：图书馆(.*)', table_title.get_text())[0]
        except Exception as e:
            RoomId = re.findall(r'教室：(.*)', table_title.get_text())[0]
    
    print (RoomId)    
    index = 0
    def handle(l):
        while '' in l:
            l.remove('')
        return l

    for i in class_info.select('tr')[1:]:
        all_table = i.find_all('td')
        ClassName = all_table[0].get_text().strip() or result[index - 1]['ClassName']
        ClassTeacher = all_table[7].get_text().strip() or result[index - 1]['ClassTeacher']
        ClassCount = all_table[9].get_text().strip() or result[index - 1]['ClassCount']
        ClassGrade = ','.join(handle(all_table[10].get_text().strip().replace('\n','').split(' '))) or result[index - 1]['ClassGrade']
        ClassWeek = all_table[11].get_text().lstrip().rstrip()
        ClassTime = all_table[12].get_text().strip().split('[')
        result.append({'RoomId': RoomId,
                       'ClassName':ClassName, 
                       'ClassTeacher': ClassTeacher, 
                       'ClassWeek': ClassWeek,
                       'ClassCount': ClassCount,
                       'ClassGrade': ClassGrade,
                       'ClassTimeWeek': all_week[ClassTime[0]],
                       'ClassTimeTime': all_time[ClassTime[1]]})
        index += 1

    return result

def main(get_tmp=False):
    path = os.path.join(os.getcwd(),'course', 'management','commands','result.txt')
    with open(path, 'r',encoding='utf-8') as f:
        for i in f.readlines():
            yield deal(i,get_tmp=get_tmp)


def sync_course_to_db(get_tmp=False,debug=True):
    for j in main(get_tmp):
        allclass = []
        try:
            for i in j:
                if not debug:
                    allclass.append(RoomTest(RoomID=i['RoomId'],
                                             ClassName=i['ClassName'],
                                             ClassTeacher=i['ClassTeacher'],
                                             ClassWeek=i['ClassWeek'],
                                             ClassCount=int(i['ClassCount']),
                                             ClassGrade=i['ClassGrade'],
                                             ClassTimeWeek=int(i['ClassTimeWeek']),
                                             ClassTimeTime=i['ClassTimeTime']))
                print (i)
        except Exception as e:
            continue

        if not debug:
            RoomTest.objects.bulk_create(allclass)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-t', type=int,help="get tmp_info [0, 1]", default=0)
        parser.add_argument('-d', type=int,help="debug [0, 1]", default=0)

    def handle(self, *args, **options):
        get_tmp = True if options['t'] else False
        debug = False if options['d'] else True
        sync_course_to_db(get_tmp,debug)

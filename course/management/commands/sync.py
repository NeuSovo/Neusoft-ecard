import os
import re
import requests
from bs4 import BeautifulSoup as bf
from django.core.management.base import BaseCommand, CommandError
from course.models import RoomTest
from classinfo import roominfo
from aip import AipOcr
from tenacity import retry, retry_if_exception_type

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
def deal_tmp_info(info, RoomId=None, normal=True) -> dict:
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



APP_ID = '11517608'
API_KEY = 'qGCmlacGw3YS6GA6bcN2AUa9'
SECRET_KEY = 'k8urPaXfjxaNqaW4rD6WTlhoAGXmMHw0'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

class VaildCodeError(Exception):
    pass


class Crawer:
    """docstring for Crawer"""
    def __init__(self, xnxq = '20172', debug = True):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            'Cookie': 'ASP.NET_SessionId=x1vexibsducg1taqamzeed3d',
            'Host': 'newjw.neusoft.edu.cn',
            'Origin': 'http://newjw.neusoft.edu.cn',
            'Referer': 'http://newjw.neusoft.edu.cn/jwweb/ZNPK/KBFB_RoomSel.aspx',
        }
        self.data = {
            'Sel_XNXQ': xnxq,
            'rad_gs': '2',
            'Sel_XQ': '1',

            # to change
            'txt_yzm': 'yzm',
            'Sel_JXL': 'classkey',
            'Sel_ROOM': 'classkey',
        }
        self.client = requests.Session()

        self.yzm_url = 'http://newjw.neusoft.edu.cn/jwweb/sys/ValidateCode.aspx'
        self.class_url = 'http://newjw.neusoft.edu.cn/jwweb/ZNPK/KBFB_RoomSel_rpt.aspx'
        self.debug = debug
    
    def update_yzm(self):
        yzm = self.client.get(self.yzm_url, headers=self.headers)
        res = client.basicAccurate(yzm.content)
        yzm = res['words_result'][0]['words'].replace(' ','') if res['words_result_num'] else ''
        self.yzm = yzm
        if self.debug:
            print (res)
        return yzm

    def write_data(self, data):
        if data[1:]:
            with open('result.txt', 'a+', encoding='utf-8') as f:
                f.write(str(data[1:]) + '\n')

    @retry(retry=retry_if_exception_type(VaildCodeError))
    def crawer_signle_class(self, classkey):
        self.data['txt_yzm'] = self.yzm
        self.data['Sel_JXL']= classkey[:3]
        self.data['Sel_ROOM'] = classkey

        detail = self.client.post(self.class_url, headers=self.headers, data=self.data)
        soup = bf(detail.text, 'lxml')
        if "alert('验证码错误！');" in detail.text:
            self.update_yzm()
            raise VaildCodeError()

        soup = soup.select('table')
        self.write_data(soup)

    def start(self):
        self.update_yzm()
        for i in roominfo:
            self.crawer_signle_class(i)



class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-t', type=int,help="get tmp_info [0, 1]", default=0)
        parser.add_argument('-d', type=int,help="debug [0, 1]", default=0)
        parser.add_argument('-c', type=str,help="crawer xnnq [20172, 20180]", default='20172')

    def handle(self, *args, **options):
        get_tmp = True if options['t'] else False
        debug = False if options['d'] else True
        if options['c']:
            a = Crawer(xnnq=options['c'], debug=debug)
            a.start()
        else:
            sync_course_to_db(get_tmp,debug)

import re
from bs4 import BeautifulSoup as bf
# from course.models import RoomTest
all_time = {
    '1-2节]': '1',
    '1-2节]双': '1',
    '1-2节]单': '1',
    '3-4节]': '2',
    '3-4节]单': '2',
    '3-4节]双': '2',
    '5-6节]': '3',
    '5-6节]单': '3',
    '5-6节]双': '3',
    '7-8节]': '4',
    '7-8节]单': '4',
    '7-8节]双': '4',
    '9-10节]': '5',
    '9-11节]': '5',
    '1-4节]': '1-2',
    '5-7节]':'3-4',
    '5-8节]': '3-4',
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
def  deal_tmp_info(info, RoomId=None, normal=True):
    for i in info.select('tr')[1:]:
        all_table = i.find_all('td')
        if not normal:
            # print （）
            ClassName = all_table[0].get_text().strip()
            ClassTeacher = all_table[7].get_text().strip()
            ClassCount = all_table[9].get_text().strip()
            ClassGrade = all_table[10].get_text().strip().replace('\n','').split(' ')
            ClassWeek = all_table[11].get_text().lstrip().rstrip()
            ClassTime = all_table[12].get_text().strip().split('[')
        else:
            ClassWeek = all_table[0].get_text()
            ClassTime = all_table[1].get_text()
            ClassName = all_table[2].get_text()
            ClassTeacher = all_table[3].get_text()
            ClassCount = None
            ClassGrade = None

        if ClassName != '':
            pass
            print (RoomId, ClassWeek,ClassTime,ClassName)


def deal(info) -> dict:
    result = []
    soup = bf(info,'lxml')
    allinfo = soup.select('table')
    try:
        table_title = allinfo[1]
        class_info = allinfo[2]
        calss_tmp_info = allinfo[4]
        deal_tmp_info(re.findall(r'教室：教学楼(.*)', table_title.get_text())[0], calss_tmp_info, normal=True)
        # print(table_title)
    except Exception as e:
        table_title = allinfo[0]
        calss_tmp_info = allinfo[1]
        RoomId = re.findall(r'教学楼(.*)临时活动安排', table_title.get_text())
        if len(RoomId) !=0:
            # pass
            deal_tmp_info(calss_tmp_info, RoomId[0])
        else:
            table_title = allinfo[1]
            calss_tmp_info = allinfo[2]
            RoomId = re.findall(r'教室：教学楼(.*)', table_title.get_text())
            if len(RoomId) !=0:
                # pass
                deal_tmp_info (calss_tmp_info, RoomId[0], normal=False)

    # RoomId = re.findall(r'教室：教学楼(.*)', table_title.get_text())[0]
    # print (RoomId)
    
    # index = 0
    # def handle(l):
    #     while '' in l:
    #         l.remove('')
    #     return l

    # for i in class_info.select('tr')[1:]:
    #     all_table = i.find_all('td')
    #     ClassName = all_table[0].get_text().strip() or result[index - 1]['ClassName']
    #     ClassTeacher = all_table[7].get_text().strip() or result[index - 1]['ClassTeacher']
    #     ClassCount = all_table[9].get_text().strip() or result[index - 1]['ClassCount']
    #     ClassGrade = ','.join(handle(all_table[10].get_text().strip().replace('\n','').split(' '))) or result[index - 1]['ClassGrade']
    #     ClassWeek = all_table[11].get_text().lstrip().rstrip()
    #     ClassTime = all_table[12].get_text().strip().split('[')
    #     result.append({'RoomId': RoomId,
    #                    'ClassName':ClassName, 
    #                    'ClassTeacher': ClassTeacher, 
    #                    'ClassWeek': ClassWeek,
    #                    'ClassCount': ClassCount,
    #                    'ClassGrade': ClassGrade,
    #                    'ClassTimeWeek': all_week[ClassTime[0]],
    #                    'ClassTimeTime': all_time[ClassTime[1]]})
    #     index += 1
    # return result


def main():
    with open('result.txt','r',encoding='utf-8') as f:
        for i in f.readlines():
            deal(i)


# def test():
#     for j in main():
#         allclass = []
#         try:
#             for i in j:
#                 print (i)
#                 allclass.append(RoomTest(RoomID=i['RoomId'],
#                                          ClassName=i['ClassName'],
#                                          ClassTeacher=i['ClassTeacher'],
#                                          ClassWeek=i['ClassWeek'],
#                                          ClassCount=int(i['ClassCount']),
#                                          ClassGrade=i['ClassGrade'],
#                                          ClassTimeWeek=int(i['ClassTimeWeek']),
#                                          ClassTimeTime=i['ClassTimeTime']))
#         except:
#             continue

#         RoomTest.objects.bulk_create(allclass)
main()
import re
from bs4 import BeautifulSoup as bf
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
result = []
def deal(info) -> dict:
    soup = bf(info,'lxml')
    allinfo = soup.select('table')
    try:
        table_title = allinfo[1]
        class_info = allinfo[2]
        calss_tmp_info = allinfo[4]
        # print(table_title)
    except Exception as e:
        return

    RoomId = re.findall(r'教室：教学楼(.*)', table_title.get_text())[0]
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

def main():
    with open('course/result.txt','r',encoding='utf-8') as f:
        for i in f.readlines():
            yield deal(i)
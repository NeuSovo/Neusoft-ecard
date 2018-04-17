# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bf
# from prettytable import PrettyTable
from classinfo import roominfo

# table = PrettyTable(["一", "二", "三", "四", "五", "六", "日"])
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Cookie': 'ASP.NET_SessionId=x1vexibsducg1taqamzeed3d',
    'Host': 'newjw.neusoft.edu.cn',
    'Origin': 'http://newjw.neusoft.edu.cn',
    'Referer': 'http://newjw.neusoft.edu.cn/jwweb/ZNPK/KBFB_RoomSel.aspx',
}
s = requests.Session()


def getinfo(c, classkey):
    data = {
        'Sel_XNXQ': '20171',
        'rad_gs': '2',
        'txt_yzm': c,
        'Sel_XQ': '1',
        'Sel_JXL':classkey[:3],
        'Sel_ROOM': classkey,
    }
    print (classkey,roominfo[classkey])
    detail = s.post(
        'http://newjw.neusoft.edu.cn/jwweb/ZNPK/KBFB_RoomSel_rpt.aspx', headers=headers, data=data)
    # print (detail)
    soup = bf(detail.text, 'lxml')
    
    try:
        yzmflag = soup.find('script').get_text()
        if "alert('验证码错误！');" == yzmflag:
            raise Exception("1")
    except Exception as e:
        if str(e) == "1":
            print (e)
            raise e
        else:
            pass



    all = soup.select('table')
    with open('result.txt', 'a+', encoding='utf-8') as f:
        f.write(str(all[1:]) + '\n')


def get_class_code():
    for i in range(1, 15):
        data = s.get(
            'http://newjw.neusoft.edu.cn/jwweb/ZNPK/Private/List_ROOM.aspx?w=150&id={}'.format(101 + i), headers=headers)
        # print (data.text)
        soup = bf(data.text, 'lxml')
        info = soup.select('script')
        info = bf(info[0].text, 'lxml')
        for cl in info.select('option'):
            # print (error_message='')
            print(cl.get('value'), cl.text)


def main():
    code = s.get('http://newjw.neusoft.edu.cn/jwweb/sys/ValidateCode.aspx',headers=headers)

    with open('cap.jpg', 'wb') as file:
        file.write(code.content)
    c = input()

    for key in roominfo:
        try:
            getinfo(c,key)
        except Exception as e:
            if str(e) == "1":
                try:
                    code = s.get('http://newjw.neusoft.edu.cn/jwweb/sys/ValidateCode.aspx',headers=headers)
                    with open('cap.jpg', 'wb') as file:
                        file.write(code.content)
                    c = input()
                    getinfo(c,key)
                except:
                    continue
            else:
                continue

    # with open('result.txt', 'r', encoding='utf-8') as f:
    #     for fff in f.readlines()[:1]:
    #         deal(fff)
    #         print ('-'*100)
            
# def deal(info) -> str:
#     weekd = ['一','二','三','四','五','六','日']
#     sttt = 0
#     wkkk = 0
#     soup = bf(info,'lxml')
#     jxl = soup.find_all('td',attrs={'align':'left'})
#     print ('-'*30,jxl[0].get_text(),'-'*30)
#     for week in soup.find_all('tr')[2:]:
#         cl = week.find_all('td',attrs={'valign':'top'})
#         wkkk = 0
#         for i in cl:
#             info = str(i).split('<br/>')
#             # print (weekd[wkkk],info[0],info[1:])
#             for tt in info:
#                 if tt == info[0]:
#                     subject = bf(tt,'lxml').get_text()
#                     print (weekd[wkkk],subject,end='')
#                 elif tt != '</td>':
#                     print (tt, end='')
#             print (end='\n')
#             wkkk +=1
#         print ('-'*100)

main()
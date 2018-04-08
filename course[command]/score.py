import random
import requests
import string
from hashlib import md5
url = 'http://newjw.neusoft.edu.cn/jwweb/xscj/Stu_MyScore_Drawimg.aspx?x=1&h=2&w=958&xnxq=20170&xn=2017&xq=0&rpt=0&rad=2&zfx=0'
url2 = 'http://newjw.neusoft.edu.cn/jwweb/xscj/Stu_MyScore_Drawimg.aspx?x=1&h=2&w=873&xnxq=20170&xn=2017&xq=0&rpt=1&rad=2&zfx=0'
sel = 'http://newjw.neusoft.edu.cn/jwweb/znpk/Pri_StuSel_Drawimg.aspx?type=1&w=1100&h=580&xnxq=20171'
ssel = 'http://newjw.neusoft.edu.cn/jwweb/znpk/Pri_StuSel_rpt.aspx?m={}'

data = {
    'Sel_XNXQ':'20171',
    'rad':'0',
    'px':'0',
    'txt_yzm':' ',
    'hidyzm':'cbf8e320a8278541dd8233fb454f37z',
    'hidsjyzm':'46F15A220385F4D9C63C7C2371A71356',
}
headers = {
   'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
   'Accept-Encoding': 'gzip, deflate',
   'Accept-Language': 'zh-CN,zh;q=0.9',
   'Connection': 'keep-alive',
   'Cookie': 'pgv_pvi=4405037056; ASP.NET_SessionId=232fo0rapamghxvjn05ndkjt',
   'Host': 'newjw.neusoft.edu.cn',
   'Referer': 'http://newjw.neusoft.edu.cn/jwweb/xscj/Stu_MyScore_rpt.aspx',
   # 'Referer' : 'http://newjw.neusoft.edu.cn/jwweb/znpk/Pri_StuSel_rpt.aspx?m=2DcAIUvuFiSZMi1',
   'Referer': 'http://newjw.neusoft.edu.cn/jwweb/znpk/Pri_StuSel.aspx',
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36 ',
}

def pk():
    m = md5()
    rs = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
    s = ('13168' + '20171' + rs).encode('utf-8')
    m.update(s)
    cc_str = m.hexdigest()
    return rs,cc_str # m,o
def base_req():
    s = requests.session()
    m,o = pk()
    sssel = ssel.format(m)
    data['hidsjyzm'] = o
    s.post(sssel,headers=headers,data=data)
    headers['Referer'] = 'http://newjw.neusoft.edu.cn/jwweb/znpk/Pri_StuSel_rpt.aspx?m={}'.format(m)
    info = s.get(sel,headers=headers)
    print (info.text)
    with open('demo.jpg','wb') as f:
        f.write(info.content)

base_req()
# info = requests.get(url2,headers=headers)
# with open('demo.jpg','wb') as f:
#     f.write(info.content)
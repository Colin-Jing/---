# 这段代码在本地运行
from bs4 import BeautifulSoup
import time
import openpyxl
import requests


def get_data(website,kind,url):
    print(url)
    try:
        res = requests.get(url) # 访问页面
        res.encoding = "GB2312"
        if res.status_code != 200:
            print(res.status_code)
            return
    except:
        print("页面不存在，该板块加载完毕！！！")
        return
    soup = BeautifulSoup(res.text, 'html.parser')
    label = soup.find_all('li')
    try:
        wb = openpyxl.load_workbook(r"./{0}/{1}.xlsx".format(website,kind))
        print("./{0}/{1}.xlsx".format(website,kind)+"被打开")
    except:
        print("./{0}/{1}.xlsx不存在！！！将自动创建".format(website,kind))
        wb = openpyxl.Workbook()
    finally:
        ws = wb.active
    # for title in label:
    #     title = title.find_all('a')
    #     for j in range(len(title)):
    #         print('{}'.format(j)+'\t'+title[j].text) # 打印label的文本
    #         ws.append([title[j].text, kind])
    for i in range(len(label)):
        if label[i].find('a',target="_blank") != None :
            if i % 5 == 0:
                print('{}'.format(i)+'\t'+label[i].find('a',target="_blank").text) # 打印label的文本
            ws.append([label[i].find('a',target="_blank").text, kind])
    wb.save(r'./{0}/{1}.xlsx'.format(website,kind))
    print(r'./{0}/{1}.xlsx'.format(website,kind)+'保存成功！！！')
    wb.close()


type_list = ['房产','教育','科技','军事','体育','游戏','娱乐','其他']
url_list = [
    'http://house.people.com.cn/GB/194441/index{}.html',
    'http://edu.people.com.cn/GB/1053/index{}.html',
    'http://scitech.people.com.cn/GB/1057/index{}.html',
    'http://military.people.com.cn/GB/172467/index{}.html',
    'http://sports.people.com.cn/GB/436800/index{}.html',
    'http://game.people.com.cn/GB/48661/index{}.html',
    'http://ent.people.com.cn/GB/86955/index{}.html',
    'http://health.people.com.cn/GB/415859/index{}.html'
]
for i in range(len(type_list)):
    print("-*"*20)
    print('当前爬取内容：%s'%type_list[7])
    for j in range(1,50):
        if j % 5 == 0:
            print("当前爬取页面：第%d页"%j)
        get_data('人民网',type_list[7],url_list[7].format(7))
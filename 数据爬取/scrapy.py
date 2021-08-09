# 这段代码在本地运行
from bs4 import BeautifulSoup
from selenium import webdriver #从selenium库中调用webdriver模块
import time

driver = webdriver.Chrome() # 设置引擎为Chrome，从本地打开一个Chrome浏览器
driver.get('https://new.qq.com/ch2/hyrd') # 访问页面
time.sleep(3)
for i in range(100):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    HTML = driver.page_source
    if i%10 ==0:
        print(i)
    time.sleep(1.5)

HTML = driver.page_source
time.sleep(3) # 等待3秒
bs = BeautifulSoup(HTML,'html.parser')
label = bs.find_all('img',class_="Monograph")  # 解析网页并提取第一个<label>标签
#print(label.get_attribute('alt')) # 获取type这个属性的值
with open(r'./car.txt','a',encoding='UTF-8') as file:
    for i in range(len(label)):
        if i % 10 == 0:
            print('{}'+'\t'+label[i]['alt'].format(i)) # 打印label的文本
        file.write(label[i]['alt']+'\t'+'5'+'\n')


driver.close() # 关闭浏览器
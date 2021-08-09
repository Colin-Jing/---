import scrapy
import bs4
from ..items import DoubanBookItem

class DoubanSpider(scrapy.Spider):

    name = 'douban_book'  # 定义爬虫的名字

    allowed_domains = ['book.douban.com']  # 定义允许爬取网站的域名，如果域名不在这里面，就会被过滤掉

    start_urls = ['https://book.douban.com/top250?start=0']  # 爬虫开始爬的起始网站

    for x in range(3):
        url = 'https://book.douban.com/top250?start={0}'.format(x * 25)
        start_urls.append(url)


    def parse(self, response):

        # parse是默认处理response的方法

        bs = bs4.BeautifulSoup(response.text, 'html.parser')

        # 用BeautifulSoup解析response

        datas = bs.find_all('tr', class_="item")

        # 用find_all提取<tr class="item">元素，这个元素里含有书籍信息

        for data in datas:
            # 遍历data

            item = DoubanBookItem()

            # 实例化DoubanItem这个类

            item['title'] = data.find_all('a')[1]['title']

            # 提取出书名，并把这个数据放回DoubanItem类的title属性里

            item['publish'] = data.find('p', class_='pl').text

            # 提取出出版信息，并把这个数据放回DoubanItem类的publish里

            item['score'] = data.find('span', class_='rating_nums').text

            # 提取出评分，并把这个数据放回DoubanItem类的score属性里。

            print(item['title'])

            # 打印书名

            yield item

            # yield item是把获得的item传递给引擎
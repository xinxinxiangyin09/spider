'''
本次升级,将原来的代码改为多线程爬虫
'''

import requests
from lxml import etree
import time
from threading import Thread
from queue import Queue
import json
import pymysql

from config import *

class MiSpider(object):
    def __init__(self):
        self.url = "http://app.mi.com/categotyAllListApi?page={}&categoryId=15&pageSize=30"
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3895.5 Safari/537.36"}
        # 创建URL队列
        self.url_queue = Queue()

    # 把所有要爬取的页面放进队列
    def url_in(self):
        for page in range(67):
            url = self.url.format(page)
            # 加入队列
            self.url_queue.put(url)


    # 线程事件函数
    def get_data(self):
        while True:
            # 如果结果 为True,则队列为空了
            if self.url_queue.empty():
                break
            # get地址,请求一级页面
            url = self.url_queue.get()
            html = requests.get(url=url, headers=self.headers).content.decode("utf-8")
            html = json.loads(html) # 转换为json格式
            # 解析数据
            app_list = [] # 定义一个列表,用来保存所有的APP信息 [(name,url,info),(),(),...]
            for app in html["data"]:
                # 应用链接
                app_link = "http://app.mi.com/details?id=" + app["packageName"]
                app_list.append(self.parse_two_page(app_link))

            return app_list

    def parse_two_page(self, app_link):
        html = requests.get(url=app_link, headers=self.headers).content.decode('utf-8')
        parse_html = etree.HTML(html)

        app_name = parse_html.xpath('//div[@class="intro-titles"]/h3/text()')[0].strip()
        app_url = "http://app.mi.com" + parse_html.xpath('//div[@class="app-info-down"]/a/@href')[0].strip()
        app_info = parse_html.xpath('//p[@class="pslide"][1]/text()')[0].strip()

        info = (app_name, app_url, app_info)

        print(app_name)

        return info


    # 主函数
    def main(self):
        # url入队列
        self.url_in()
        # 创建多线程
        t_list = []
        for i in range(67):
            t = Thread(target=self.get_data)
            t_list.append(t)
            t.start()

        for i in t_list:
            i.join()

        db = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DB, charset=CHARSET)
        cursor = db.cursor()

        ins = 'insert into app values (%s, %s, %s)'

        app_list = self.get_data()
        print("正在写入数据库")
        cursor.executemany(ins, app_list)

        db.commit()
        cursor.close()
        db.close()


if __name__ == '__main__':
    start = time.time()
    spider = MiSpider()
    spider.main()
    end = time.time()

    print("执行时间:%.2f"% (end - start))
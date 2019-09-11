import requests
from lxml import etree
import pymysql
from fake_useragent import UserAgent
import time
import random

class ManyanSpider(object):
    def __init__(self):
        self.url = "https://maoyan.com/board/4?offset={}"
        self.headers = {"User-Agent":UserAgent().random}
        self.page = 1 # 用于监控爬虫,即记页功能

        #创建游标对象
        self.db = pymysql.connect("10.0.0.7", "root", "Asd.1234", "spider", charset="utf8")
        self.cursor = self.db.cursor()

    # 构造URL并发起请求
    def get_page(self, url):
        html = requests.get(url, headers=self.headers).content.decode("utf-8")
        self.parse_html(html)

        return html

    # 解析网页
    def parse_html(self, html):
        # 创建解析对象
        parse_html = etree.HTML(html)
        movie_dict = {}
        # 基准xpath:匹配每个电影的节点对象
        dd_list = parse_html.xpath('//dl[@class="board-wrapper"]/dd')
        # for循环遍历节点对象,获取信息
        for dd in dd_list:
            movie_dict["name"] = dd.xpath('./a/@title')[0].strip() # 电影名称
            movie_dict["star"] = dd.xpath('.//p[@class="star"]/text()') # 主演
            movie_dict["time"] = dd.xpath('.//p[@class="releasetime"]/text()') # 上映时间

        print(movie_dict)

    # 保存至MySQL数据库,终端提示
    def write_page(self, r_list):
        # 定义空列表
        film_list = []
        ins = "insert into maoyan (name, star, time) values (%s, %s, %s)"
        #处理数据,放到大列表film_list中
        for rt in r_list:
            one_film = [rt[0], rt[1].strip(), rt[2].strip()[5:15]]
            # 添加到大列表中
            film_list.append(one_film)
        self.cursor.executemany(ins, film_list)
        # 提交到数据库
        self.db.commit()

    # 主函数
    def main(self):
        for offset in range(0, 91, 10):# 构造URL
            url = self.url.format(offset)
            self.get_page(url)
            # time.sleep(random.randint(1, 3))

            print("第%d页爬取完成"%self.page)
            self.page += 1

        # 断开数据库
        self.cursor.close()
        self.db.close()

if __name__ == '__main__':

    start = time.time()

    spider = ManyanSpider()
    spider.main()

    end = time.time()

    print("执行时间为:%.2f"%(end - start))
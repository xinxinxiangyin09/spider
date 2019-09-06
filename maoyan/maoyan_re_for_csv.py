from urllib import request
from fake_useragent import UserAgent
import time
import re
import csv
import random

class ManyanSpider(object):
    def __init__(self):
        self.url = "https://maoyan.com/board/4?offset={}"
        self.headers = {"User-Agent":UserAgent().random}
        self.page = 1 # 用于监控爬虫,即记页功能

    # 构造URL并发起请求
    def get_page(self, url):
        req = request.Request(url=url, headers=self.headers)
        res = request.urlopen(req)
        html = res.read().decode("utf-8")

        self.parse_html(html)

    # 解析网页
    def parse_html(self, html):
        pattern = re.compile('<div class="movie-item-info">.*?title="(.*?)".*?class="star">.*?主演：(.*?)</p>.*?releasetime">(.*?)</p>', re.S)
        # r_list: [('霸王别姬','张国荣','1993'), (), ()]
        r_list = pattern.findall(html)

        self.write_page(r_list)

    # 保存,终端提示
    def write_page(self, r_list):
        film_list = []
        with open("movie.csv", "a") as f:
            write = csv.writer(f)
            for rt in r_list:
                name = rt[0]
                star = rt[1].strip()
                time = rt[2].strip()[5:15]

                film_list.append((name, star, time))

            write.writerows(film_list)

    def main(self):
        for offset in range(0, 91, 10):# 构造URL
            url = self.url.format(offset)
            self.get_page(url)
            time.sleep(random.randint(1, 3))

            print("第%d页爬取完成"%self.page)
            self.page += 1

if __name__ == '__main__':

    start = time.time()

    spider = ManyanSpider()
    spider.main()

    end = time.time()

    print("执行时间为:%.2f"%(end - start))
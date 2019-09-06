from urllib import request
from fake_useragent import UserAgent
import re
import time
import random
import pymysql

class MovieSky(object):
    def __init__(self):
        self.url = "https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html"
        self.headers = {"User-Agent":UserAgent().random}
        self.db = pymysql.connect("10.0.0.7", "root", "Asd.1234", "spider", charset="utf8")
        self.cursor = self.db.cursor()

    # 获取页面的html
    def get_page(self, url):
        req = request.Request(url=url, headers=self.headers)
        res = request.urlopen(req)
        html = res.read().decode("gbk", "ignore")
        return html

    # 解析二级页面,获取下载链接
    def parse_two_html(self, film_link):
        two_html = self.get_page(film_link)
        pattern = re.compile('<tr>.*?style="WORD-WRAP: break-word".*?href="(.*?)">', re.S)
        down_link = pattern.findall(two_html)[0]

        return down_link

    # 解析页面,提取电影名称和下载链接
    def parse_page(self, html): # html 为一级页面的响应内容
        # 解析一级页面(提取 电影名称 和 详情链接)
        pattern = re.compile('<td height="26">.*?href="(.*?)".*?"ulink">(.*?)</a>.*?</td>',re.S)
        # film_list:[("详情链接", "电影名称"), (), ()]
        film_list = pattern.findall(html)

        ins = "insert into `moviesky` (`name`, `link`) values(%s, %s)"
        i = 1 # 计数
        for film in film_list:
            film_name = film[1]
            film_link = "https://www.dytt8.net" + film[0]
        # 请求二级页面详情链接之后提取下载链接
            download_link = self.parse_two_html(film_link)

            print(i, film_name, download_link)
            i += 1

            self.cursor.execute(ins, [str(film_name), str(download_link)])
            self.db.commit()



    def main(self):
        for page in range(1,91):
            url = self.url.format(page)
            html = self.get_page(url)
            self.parse_page(html)
            # time.sleep(random.randint(1, 3))
            print("第%d页完成"%page)
        self.cursor.close()
        self.db.close()
if __name__ == '__main__':
    spider = MovieSky()
    spider.main()
# encoding="gbk"

import requests
from lxml import etree
import csv
from fake_useragent import UserAgent

class QiushiSpider(object):
    def __init__(self):
        self.headers = {"User-Agent":UserAgent().random}
        self.url = "https://www.qiushibaike.com/hot/page/{}/"

    def get_page(self, url):
        html = requests.get(url, headers=self.headers).content.decode("utf-8")
        self.parse_page(html)

    def parse_page(self, html):
        parse_html = etree.HTML(html)
        info_list = parse_html.xpath('//div[@id="content-left"]/div')
        for info in info_list:
            username = info.xpath('.//h2/text()')[0].strip()
            content = info.xpath('.//div[@class="content"]/span/text()')[0].strip()
            funny = info.xpath('./div/span/i/text()')[0].strip()
            comment = info.xpath('./div/span/a/i/text()')[0].strip()

            self.write_page(username, content, int(funny), int(comment))


    def write_page(self, username, content, funny, comment):
        with open("糗事百科.csv", "a", encoding="utf-8") as f:
            write = csv.writer(f)
            write.writerow([username, content, funny, comment])


    def main(self):
        for page in range(1, 101):
            url = self.url.format(page)
            self.get_page(url)
            print("正在爬取第 {} 页。。。".format(page))

if __name__ == '__main__':
    try:
        spider = QiushiSpider()
        spider.main()
    except KeyboardInterrupt:
        print("用户自行退出")
    except:
        print("异常终止")
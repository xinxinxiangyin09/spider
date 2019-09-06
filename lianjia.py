import requests
from fake_useragent import UserAgent
from lxml import etree
import time

class LianJiaSpider(object):
    def __init__(self):
        self.url = "https://xa.lianjia.com/ershoufang/pg{}/"
        self.headers = {"User-Agent":UserAgent().random}

    def get_page(self, url):
        res = requests.get(url, headers=self.headers)
        res.encoding = "utf-8"
        html = res.text
        # 调用解析函数
        self.parse_page(html)

    def parse_page(self, html):
        parse_html = etree.HTML(html)
        li_list = parse_html.xpath('//ul[@class="sellListContent"]/li')
        house_dict = {}
        for li in li_list:
            # 标题
            house_dict["title"] = li.xpath('.//a[@class="no_resblock_a"]/text()')[0].strip()
            # 总价
            total_price = li.xpath('./div/div[@class="priceInfo"]/div[@class="totalPrice"]/span/text()')[0].strip()
            total_price = float(total_price) * 10000
            house_dict["total_price"] = total_price

            # 单价
            unit_price = li.xpath('./div/div[@class="priceInfo"]/div[2]/span/text()')[0].strip()[2:-4]
            unit_price = float(unit_price)
            house_dict["unit_price"] = unit_price
            # 简介
            house_dict["info"] = li.xpath('.//div[@class="houseInfo"]/text()')[1].strip()
            print(house_dict)

    def main(self):
        for pg in range(1,2):
            url = self.url.format(pg)
            self.get_page(url)

if __name__ == '__main__':
    start = time.time()
    spider = LianJiaSpider()
    spider.main()
    end = time.time()

    print(("执行时间:%.2f") % (end - start))
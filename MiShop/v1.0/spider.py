'''
小米应用商店的APP信息爬取,分别获取app的名字和APP的介绍
'''

import requests
from lxml import etree
import csv


class MiSpider(object):
    def __init__(self):
        self.url = "http://app.mi.com/categotyAllListApi?page={}&categoryId=5&pageSize=30"
        self.headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3895.5 Safari/537.36"}

    # 获取一级页面,为json格式, 并提取APP详情链接
    def get_list_page(self, url):
        html = requests.get(url=url, headers=self.headers).json()
        apps = html["data"]
        for app in apps:
            app_url = "http://app.mi.com/details?id=" + app["packageName"]
            self.parse_info(app_url)



    # 请求详情页面,提取APP介绍
    def parse_info(self, app_url):
        html = requests.get(url=app_url, headers=self.headers).text
        parse_html = etree.HTML(html)
        name = parse_html.xpath('//div[@class="intro-titles"]/h3/text()')[0].strip()
        info = parse_html.xpath('//p[@class="pslide"][1]/text()')[0].strip()
        self.write_data(name, info, app_url)

    def write_data(self, name, info, app_url):
        with open("/home/chancey/project/spider/11-MiShop/小米应用商店.csv", 'a+') as f:
            writer = csv.writer(f)
            writer.writerow([name, app_url, info])
            print(name, "已写入")

    # 主函数
    def main(self):
        try:
            page = int(input("请输入页数:")) - 1
            for p in range(0, page):
                url = self.url.format(p)
                self.get_list_page(url)
        except ValueError:
            print("请输入纯数字")
        except KeyboardInterrupt:
            print("\n用户退出")

if __name__ == '__main__':
    spider = MiSpider()
    spider.main()
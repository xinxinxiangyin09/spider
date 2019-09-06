import requests
from lxml import etree
import random
import time

class BaiduSpider(object):
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0"}

    def get_html(self, url): # 下边会请求多次,封装以减少代码量
        content = requests.get(url, self.headers).content
        return content

    # 获取帖子链接
    def get_t_link(self, url):
        html = self.get_html(url).decode("utf-8")
        # 提取帖子链接
        parse_html = etree.HTML(html)
        # t_list:['p/123213123', 'p/3245434']
        t_list = parse_html.xpath('//*[@id="thread_list"]/li//div[@class="t_con cleafix"]/div/div/div/a/@href')
        for t in t_list:
            t_link = "http://tieba.baidu.com/" + t
            self.write_image(t_link)

    def write_image(self, t_link):
        html = self.get_html(t_link).decode("utf-8")
        parse_html = etree.HTML(html)
        # img_list: ["https:xx.jpg","",""]
        img_list = parse_html.xpath('//img[@class="BDE_Image"]/@src')
        for img_url in img_list:
            # print(img_url)
            html = self.get_html(img_url)
            filename = "image/" + img_url[-10:]
            with open(filename, "wb")as f:
                f.write(html)
                print("%s 下载成功" % filename)


if __name__ == '__main__':
    try:
        spider = BaiduSpider()
        spider.get_t_link("http://tieba.baidu.com/f?kw=%CC%A9%C0%D5%A1%A4%CB%B9%CD%FE%B7%F2%CC%D8")
    except KeyboardInterrupt:
        print("用户退出!")
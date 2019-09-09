'''
v1.0 版本
'''

import requests
from lxml import etree
import pymysql
import re

from config import *

class MinzhengSpider(object):
    def __init__(self):
        self.base_url = "http://www.mca.gov.cn/article/sj/xzqh/2019/"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}
        self.db = pymysql.connect(HOST, USER, PASSWORD, DB, charset="utf8")
        self.cursor = self.db.cursor()

    # 提取二级页面的假链接
    def get_false_link(self):
        html = requests.get(self.base_url, headers=self.headers).text
        parse_html = etree.HTML(html)
        r_list = parse_html.xpath('//table[@class="article"]//tr/td/a')

        for a in r_list:
            title = a.get("title")
            if re.findall('.*以上行政区划代码', title, re.S): # 过滤掉变更情况
                two_false_link = "http://www.mca.gov.cn/" + a.get("href")

                return two_false_link

    # 提取真实的二级页面的链接
    def get_true_link(self):
        # 获取响应内容
        false_link = self.get_false_link()
        html = requests.get(url=false_link, headers=self.headers).text

        pattern = re.compile(r'window.location.href="(.*?)"')
        real_link = pattern.findall(html)[0]

        # 实现增量爬取
        sql = 'select link from version where link="%s"'%(real_link)
        self.cursor.execute(sql)

        if self.cursor.fetchall():
            print("数据已是最新")
        else:
            self.get_data(real_link)
            ins = 'insert into version values ("%s")'%(real_link)
            self.cursor.execute(ins)
            self.db.commit()

    # 提取数据
    def get_data(self, real_link):
        # 基准xpath
        html = requests.get(url=real_link, headers=self.headers).text
        parse_html = etree.HTML(html)
        tr_list = parse_html.xpath('//tr[@style="mso-height-source:userset;height:14.25pt"]')
        for tr in tr_list:
            code = tr.xpath('.//td[2]/text()')[0].strip()
            name = tr.xpath('.//td[3]/text()')[0].strip()
            self.write_data(code, name) # 写进数据库

    def write_data(self, code, name):

        # 查询是否存在该数据
        query = "select * from addr_info where name='%s'"%(name)
        self.cursor.execute(query)
        result = self.cursor.fetchall() # ((654201, '塔城市'),)
        # 倘若查询结果有数据
        if result:
            if result[0][0] != code: # 爬下来的数据和原来的数据库里面的数据不一样
                del_sql = "delete from addr_info where name='{}'".format(name) # 删除原来的数据
                self.cursor.execute(del_sql)
                self.db.commit()
                ins = "insert into addr_info values ('%s', '%s')" % (code, name) # 插入新的数据
                self.cursor.execute(ins)
                self.db.commit()

                print(code, name, "数据已更新")
            else:
                print("数据已存在")
        else:
            ins = "insert into addr_info values ('%s', '%s')" %(code, name)
            self.cursor.execute(ins)

            print(code, name, "已写入数据库")

        self.db.commit()

    # 主函数
    def main(self):
        self.get_true_link()

        self.cursor.close()
        self.db.close()

if __name__ == '__main__':
    spider = MinzhengSpider()
    spider.main()
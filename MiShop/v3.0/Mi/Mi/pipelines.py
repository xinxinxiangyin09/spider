# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

# from settings import *

class MiPipeline(object):

    def process_item(self, item, spider):
        # print(item['app_name'])
        # print(item['app_info'])
        # print(item['app_download'])
        return item

class MysqlPipeline(object):

    # 连接数据库
    def open_spider(self, spider):
        self.db = pymysql.connect(host='localhost', user='root', password='Asd.1234', database='spider', charset='utf8mb4')
        self.cursor = self.db.cursor()

    # 存储抓取到的数据
    def process_item(self, item, spider):
        ins = '''
        insert into mi(app_name, app_info, app_url) values ("%s","%s","%s")
        '''

        self.cursor.execute(ins, [item['app_name'], item['app_info'], item['app_download']])
        self.db.commit()

        return item

    # 断开数据库连接
    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()
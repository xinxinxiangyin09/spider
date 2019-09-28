# -*- coding: utf-8 -*-

import scrapy
import json
import requests
from lxml import etree


from ..items import *

class MiSpider(scrapy.Spider):
    name = 'mi'
    allowed_domains = ['app.mi.com']

    # 重写start_request 方法
    def start_requests(self):
        for page in range(67):
            url = 'http://app.mi.com/categotyAllListApi?page={}&categoryId=15&pageSize=30'.format(page)
            # 交给调度器
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        load_json = json.loads(response.text)
        app_list = load_json['data']
        for app in app_list:
            app_url = 'http://app.mi.com/details?id='+ app['packageName']
            yield scrapy.Request(url=app_url, callback=self.parse_two)

    # 解析二级页面,获取所有信息
    def parse_two(self, response):
        parse_html = etree.HTML(response.text)

        # app名称
        app_name = parse_html.xpath('//div[@class="intro-titles"]/h3/text()')[0].strip()
        # app简介
        app_info = parse_html.xpath('//div[@class="app-text"]/p[1]/text()')[0].strip()
        # app下载链接,需要和https://b6.market.xiaomi.com 拼接
        app_download = 'https://b6.market.xiaomi.com' + parse_html.xpath('//div[@class="app-info-down"]/a/@href')[0].strip()

        item = MiItem()
        item['app_name'] = app_name
        item['app_info'] = app_info
        item['app_download'] = app_download

        yield item

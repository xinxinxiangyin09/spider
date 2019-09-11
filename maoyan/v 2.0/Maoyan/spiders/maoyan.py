# -*- coding: utf-8 -*-
import scrapy
from ..items import MaoyanItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']

    def start_requests(self):
        for offset in range(0, 91, 10):
            url = 'https://maoyan.com/board/4?offset={}'.format(str(offset))
            # 交给调度器
            yield scrapy.Request(url=url, callback=self.parse_html)

    def parse_html(self, response):
        # 基准xpath,匹配每个电影信息节点对象列表
        dd_list = response.xpath('//dl[@class="board-wrapper"]/dd')
        # dd_list : [<element dd at xxx>,<...>]
        for dd in dd_list:
            # 创建item对象
            item = MaoyanItem()
            # [<selector xpath='' data='霸王别姬'>]
            # dd.xpath('')结果为[选择器1,选择器2]
            # .extract() 把[选择器1,选择器2]所有选择器序列化为unicode字符串
            # .extract_first() : 取第一个字符串
            item['name'] = dd.xpath('./a/@title').extract_first().strip()
            item['star'] = dd.xpath('.//p[@class="star"]/text()').extract()[0].strip()
            item['time'] = dd.xpath('.//p[@class="releasetime"]/text()').extract()[0]

            yield item

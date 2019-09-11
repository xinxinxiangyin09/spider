# -*- coding: utf-8 -*-
import scrapy
from ..items import MaoyanItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']

    # 起始的URL地址,即第一页地址
    start_urls = ['https://maoyan.com/board/4?offset=0']
    offset = 0

    def parse(self, response):
        # 基准的xpath
        dd_list = response.xpath('//dl[@class="board-wrapper"]/dd')
        # 依次遍历
        for dd in dd_list:
            # 创建item对象(./Maoyan/items.py)
            item = MaoyanItem()
            # 电影名称
            item['name'] = dd.xpath('./a/@title').extract_first().strip()
            # 电影主演
            item['star'] = dd.xpath('.//p[@class="star"]/text()').extract_first().strip()
            # 电影上映时间
            item['time'] = dd.xpath('.//p[@class="releasetime"]/text()').extract_first().strip()

            # 把爬取的数据交给管道文件pipelines处理
            yield item  # 倘若函数里面有yield关键字,则将该函数当做生成器使用

        self.offset += 10
        if self.offset <= 90:
            url = 'https://maoyan.com/board/4?offset={}'.format(self.offset)  # 拼接下一页的地址
            # 交给调度器入队列
            yield scrapy.Request(url=url, callback=self.parse)
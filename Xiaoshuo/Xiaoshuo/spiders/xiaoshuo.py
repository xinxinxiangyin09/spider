# -*- coding: utf-8 -*-
import scrapy

from ..items import XiaoshuoItem

class XiaoshuoSpider(scrapy.Spider):
    name = 'xiaoshuo'
    allowed_domains = ['www.daomubiji.com']
    start_urls = ['http://www.daomubiji.com/']

    # 解析一级页面,提取卷名及卷链接
    def parse(self, response):
        # link_list:['http://xxx/dao-mu-bi-ji-1', '', '']
        link_list = response.xpath('//ul[@class="sub-menu"]/li/a/@href').extract()
        for link in link_list:
            # 交给调度器
            yield scrapy.Request(url=link, callback=self.parse_two_html)

    # 解析二级页面
    def parse_two_html(self, response):
        # 基准的xpath
        article_list = response.xpath('/html/body/section/div[2]/div/article')
        for article in article_list:
            # 创建items对象
            item = XiaoshuoItem()
            # info_list:['七星鲁王', '第一章', '血尸']
            info_list = article.xpath('./a/text()').extract_first().split()
            item['volume_name'] = info_list[0]
            item['zh_num'] = info_list[1]
            item['zh_name'] = info_list[2]

            # 提取链接出来继续跟进,即继续发送给调度器
            item['zh_link'] = article.xpath('./a/@href').extract_first()
            yield scrapy.Request(url=item['zh_link'], meta={'item':item},callback=self.parse_three_html) # mate参数:传递itme对象到下一个解析函数

    def parse_three_html(self, response):
        item = response.meta['item']
        item['zh_content'] = '\n'.join(response.xpath('//article[@class="article-content"]//p/text()').extract())

        yield item
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaoshuoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 卷名
    volume_name = scrapy.Field()
    # 章节数
    zh_num = scrapy.Field()
    # 章节名称
    zh_name = scrapy.Field()
    # 章节链接
    zh_url = scrapy.Field()
    # 章节内容
    zh_content = scrapy.Field()
    zh_link = scrapy.Field()

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class XiaoshuoPipeline(object):
        def process_item(self, item, spider):

            filename = '/home/chancey/demo/盗墓笔记/{}-{}-{}.txt'.format(
                item['volume_name'],
                item['zh_num'],
                item['zh_name']
            )

            f = open(filename, 'w')
            f.write(item['zh_content'])
            f.close()
            return item

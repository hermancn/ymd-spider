# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import operator
from scrapy.contrib.exporter import CsvItemExporter
from .services import send_email


class YangmaodangPipeline(object):
    '''
    保存采集的水木羊毛信息，将其保存到csv文件中，并将其传到邮箱中。
    '''
    def __init__(self):
        self.filename = 'output/newsmth-'+time.strftime('%Y%m%d')+'.csv'
        self.file = open(self.filename, 'wb')
        self.items = []
        # self.file.write('$$'.join(YangmaodangItem.fields))

    def open_spider(self, spider):
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        # 利用回复数对文章排序
        sortedlist = sorted(self.items, key=lambda x: int(operator.itemgetter('reply_num')(x)), reverse=True)
        for item in sortedlist:
            self.exporter.export_item(item)

        self.exporter.finish_exporting()
        self.file.close()

        send_email(self.filename)


    def process_item(self, item, spider):
        self.items.append(item)
        # self.exporter.export_item(item)
        return item

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import time
from yangmaodang.items import YangmaodangItem
from scrapy.contrib.exporter import CsvItemExporter
from scrapy import signals
from .services import send_email


class YangmaodangPipeline(object):
    '''
    保存采集的水木羊毛信息，将其保存到csv文件中，并将其传到邮箱中。
    '''
    def __init__(self):
        self.filename = 'output/newsmth-'+time.strftime('%Y%m%d')+'.csv'
        self.file = open(self.filename, 'wb')
        # self.file.write('$$'.join(YangmaodangItem.fields))

    def open_spider(self, spider):
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        send_email(self.filename)


    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

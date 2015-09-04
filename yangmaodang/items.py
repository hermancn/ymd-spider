# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class YangmaodangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    article_url = Field()
    publish_date = Field()
    # score = Field()
    like = Field()
    reply_num = Field()
    crawl_time = Field()

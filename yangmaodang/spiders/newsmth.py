# -*- coding: utf-8 -*-
import scrapy

from scrapy.selector import Selector
from scrapy.http import FormRequest, Request


class NewsmthSpider(scrapy.Spider):
    name = "newsmth"
    allowed_domains = ["newsmth.net"]
    start_urls = (
        'http://www.newsmth.net/nForum/#!board/CouponsLife',
    )


    def start_requests(self):
        return [FormRequest('http://www.newsmth.net',
                            formdata = {'id':'herman3', 'passwd':'sm908819nhb'},
                            callback = self.after_login)]

    def after_login(self, response):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        print response.body
        selector = Selector(response)
        title = selector.xpath('//*[@id="body"]/div[3]/table/tbody/tr[13]/td[2]/a').extract()
        print title

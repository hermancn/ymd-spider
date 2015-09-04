# -*- coding: utf-8 -*-
'''
利用selenium爬取水木辣妈羊毛党页面

date: 2015/09/04 周五
author: hiber_niu@163.com
'''

import scrapy

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from yangmaodang.items import YangmaodangItem

import time
from datetime import date


class NewsmthSpider(scrapy.Spider):
    '''
    此处parse中直接使用start_urls的地址
    ，导致spider其实访问了两次URL（一次
    是scrapy默认访问，一次是selenium访问。）
    '''
    name = "newsmth"
    allowed_domains = ["www.newsmth.net"]
    start_urls = [
        # 带有'#'符号scrapy无法解析其后的地址。会跳转到登录页.
        'http://www.newsmth.net/nForum/#!board/CouponsLife',
    ]
    # 爬取的页面数
    pages = 3

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.driver = webdriver.Chrome('D:/chromedriver')

    def parse(self, response):
        for url in self.start_urls:
            self.driver.get(url)
            # waitting until element is already reloaded
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="body"]/div[4]/div[1]/ul/li[2]/ol/li[3]/a')))

            for page in range(2, self.pages+1):
                try:
                    # 30 articles each page
                    for index in range(1, 31):
                        try:
                            title = self.driver.find_element_by_xpath('//*[@id="body"]/div[3]/table/tbody/tr['+str(index)+']/td[2]/a')
                            publish_date = self.driver.find_element_by_xpath('//*[@id="body"]/div[3]/table/tbody/tr['+str(index)+']/td[3]')
                            # score = self.driver.find_element_by_xpath('//*[@id="body"]/div[3]/table/tbody/tr['+str(index)+']/td[5]')
                            like = self.driver.find_element_by_xpath('//*[@id="body"]/div[3]/table/tbody/tr['+str(index)+']/td[6]')
                            reply_num = self.driver.find_element_by_xpath('//*[@id="body"]/div[3]/table/tbody/tr['+str(index)+']/td[7]')

                            ymditem = YangmaodangItem()
                            ymditem['title'] = title.text
                            ymditem['article_url'] = title.get_attribute('href')
                            ymditem['publish_date'] = self._date_parse(publish_date.text)

                            ymditem['like'] = like.text
                            ymditem['reply_num'] = reply_num.text
                            ymditem['crawl_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                            import uniout
                            print ('@'*10)
                            print ymditem
                            yield ymditem
                        except Exception:
                            continue


                    # 翻页
                    next_page = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="body"]/div[4]/div[1]/ul/li[2]/ol/li['+str(page)+']/a')))
                    next_page.click()
                    self.driver.implicitly_wait(3) # seconds
                except Exception:
                    continue

            self.driver.close()

    def _date_parse(self, date_str):
        '''
        parse date_str to consistent format.
        '''
        year = str(date.today().year)
        today = time.strftime('%Y-%m-%d ')

        if year in date_str:
            return date_str
        else:
            return today+date_str

# -*- coding: utf-8 -*-
import scrapy

from scrapy.selector import Selector
from scrapy.http import FormRequest, Request
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class NewsmthSpider(scrapy.Spider):
    name = "newsmth"
    allowed_domains = ["newsmth.net"]
    start_urls = [
        'http://www.newsmth.net/nForum/#!board/CouponsLife',
    ]

    def __init__(self):
        self.driver = webdriver.Chrome('D:/chromedriver')

    def get_cookies(self):
        # add driverwait
        login_url = 'http://www.newsmth.net'
        self.driver.get(login_url)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'b_login')))
        self.driver.find_element_by_name('id').clear()
        self.driver.find_element_by_name('id').send_keys('herman3')
        self.driver.find_element_by_name('passwd').clear()
        self.driver.find_element_by_name('passwd').send_keys('sm908819nhb')
        self.driver.find_element_by_id('b_login').click()
        cookies = self.driver.get_cookies()
        return cookies

    def parse(self, response):
        for scrape_url in self.start_urls:
            yield Request(url=scrape_url, cookies=self.get_cookies(),
                          callback=self.login)

    def login(self, response):
        return [FormRequest('http://www.newsmth.net/nForum/#!board/CouponsLife',
                            formdata = {'id':'herman3', 'passwd':'sm908819nhb'},
                            callback = self.after_login)]

    def after_login(self, response):
        title = self.driver.find_element_by_xpath('//*[@id="body"]/div[3]/table/tbody/tr[13]/td[2]/a').extract()

        print title

        # hxs = Selector(response)
        # title = hxs.select('//*[@id="body"]/div[3]/table/tbody/tr[13]/td[2]/a').extract()
        # print title

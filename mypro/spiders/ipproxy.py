# -*- coding: utf-8 -*-

import scrapy
# from scrapy.xlib.pydispatch import dispatcher
from pydispatch import dispatcher
from scrapy import signals
# from selenium import webdriver


class IpproxySpider(scrapy.Spider):
    name = 'ipproxy'
    allowed_domains = ['xicidaili.com']
    start_urls = ['https://www.xicidaili.com/wn/']
    executable_path = r'C:\Users\abel\AppData\Local\Google\Chrome\Application\chromedriver.exe'

    def __init__(self):
        super().__init__()
        self.browser = webdriver.Chrome(executable_path=self.executable_path)
        dispatcher.connect(self.spider_closed, signals.spider_closed)  ##建立信号和槽，在爬虫关闭时调用

    # 爬虫关闭时 调用本方法
    def spider_closed(self):
        print("爬虫结束，关闭browser")
        self.browser.quit()

    def parse(self, response):
        pass

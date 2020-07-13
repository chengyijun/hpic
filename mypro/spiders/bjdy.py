# -*- coding: utf-8 -*-
import scrapy

from mypro.items import BjdyItem
from mypro.tools import get_config


class BojieSpider(scrapy.Spider):
    name = 'bjdy'
    # allowed_domains = ['www.bvn2.com']
    config = get_config()
    target_url = config.get('bjdy').get('url')
    base_url = target_url.split("/shipin")[0]
    start_urls = [target_url]

    def is_keywords_in_title(self, title):
        flag = False
        keywords = self.config.get('bjdy').get('keywords')
        for keyword in keywords:
            if keyword in title:
                flag = True
                break
        return flag

    def get_next_url(self, i):
        """
        将原始目标链接进行处理加入页码翻页
        :param i:
        :return:
        """
        x1 = self.target_url[:-5]
        x2 = self.target_url[-5:]
        return f'{x1}-{i}{x2}'

    def parse(self, response):
        lias = response.xpath('//*[@id="tpl-img-content"]/li/a')
        for lia in lias:
            dname = lia.xpath('./h3/text()').get()
            if not self.is_keywords_in_title(dname):
                continue
            durl = self.base_url + lia.xpath('./@href').get()
            item = BjdyItem(dname=dname, durl=durl)
            yield item

        last_page = response.xpath('//a[@class="visible-xs"]/text()').get()
        last_page_num = int(last_page.split('/')[-1])
        # 判断是否存在下一页
        i = 1
        while True:
            i += 1
            if i > last_page_num:
                break
            next_page_url = self.get_next_url(i)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

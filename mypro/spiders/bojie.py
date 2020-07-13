# -*- coding: utf-8 -*-
import scrapy

from mypro.items import MyproItem
from mypro.tools import get_config


class BojieSpider(scrapy.Spider):
    name = 'bojie'
    # allowed_domains = ['www.bvn2.com']
    config = get_config()
    target_url = config.get('bojie').get('url')
    base_url = target_url.split("/tupian")[0]
    start_urls = [target_url]

    def parse_detail(self, response):
        item = response.meta.get('item')
        imgs = response.xpath('//div[@class="content"]//img//@data-original').getall()
        item['imgs'] = imgs
        yield item

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
        lias = response.xpath('//div[@class="text-list-html"]//li/a')
        for lia in lias:
            title = lia.xpath('./@title').get()
            # if ('波多' not in title) and ('波姐' not in title):
            # if '蕾丝兔宝宝' not in title:
            if not self.is_keywords_in_title(title):
                continue
            detail_url = self.base_url + lia.xpath('./@href').get()

            item = MyproItem(dname=title)
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'item': item})

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

    def is_keywords_in_title(self, title):
        flag = False
        keywords = self.config.get('bojie').get('keywords')
        for keyword in keywords:
            if keyword in title:
                flag = True
                break
        return flag

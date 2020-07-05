# -*- coding: utf-8 -*-
import scrapy

from mypro.items import MyproItem


class BojieSpider(scrapy.Spider):
    name = 'bojie'
    # allowed_domains = ['www.bvn2.com']
    target_url = 'https://bhk5.com/tupian/list-%E4%BA%9A%E6%B4%B2%E5%9B%BE%E7%89%87.html'
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
            if '黑丝' not in title:
                # if all(['波多' not in title, '波姐' not in title]):
                # if '女仆' not in title:
                # if '无码' not in title:
                # if '学生' not in title:
                # if '援交' not in title:
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

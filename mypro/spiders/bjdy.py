# -*- coding: utf-8 -*-
import scrapy

from mypro.items import MyproItem, BjdyItem


class BojieSpider(scrapy.Spider):
    name = 'bjdy'
    # allowed_domains = ['www.bvn2.com']
    target_url = 'https://bou4.com/shipin/list-%E5%8A%A8%E6%BC%AB%E7%94%B5%E5%BD%B1.html'
    base_url = target_url.split("/shipin")[0]
    start_urls = [target_url]

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
            # if all(['波多' not in dname, '波姐' not in dname]):
            if all(['议员' not in dname]):
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

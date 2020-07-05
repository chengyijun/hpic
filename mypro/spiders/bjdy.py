# -*- coding: utf-8 -*-
import scrapy

from mypro.items import MyproItem, BjdyItem


class BojieSpider(scrapy.Spider):
    name = 'bjdy'
    # allowed_domains = ['www.bvn2.com']
    target_url = 'https://bhk5.com/shipin/list-%E5%8F%98%E6%80%81%E5%8F%A6%E7%B1%BB.html'
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
            if all(['束' not in dname, '缚' not in dname, '拘' not in dname]):
                # if all(['波多' not in dname, '波姐' not in dname]):
                # if all(['议员' not in dname]):
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

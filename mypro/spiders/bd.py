import scrapy


class BdSpider(scrapy.Spider):
    name = 'bd'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        print('__init__()')

    def parse(self, response):
        print('parse')

import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from mypro.items import DmpItem
from tools import get_config


class DmpSpider(CrawlSpider):
    name = 'dmp'
    allowed_domains = ['qxs.la']

    config = get_config()
    url = config.get('fiction').get('url')
    book_id = url.split('/')[-2]
    start_urls = [url]

    rules = (
        # Rule(LinkExtractor(allow=r'/225289/\d+'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=rf'/{book_id}/\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        index = self.get_index(response)
        title = self.get_title(response)
        url = self.get_url(response)
        content = self.get_content(response)

        item = DmpItem(index=index, title=title, url=url, content=content)
        return item

    def get_url(self, response):
        url = "NAN"
        try:
            url = response.url
        except:
            pass
        return url

    def get_index(self, response):
        index = -1
        try:
            index = int(str(response.url).split('/')[-2])
        except:
            pass
        return index

    def get_title(self, response):
        title = "NAN"
        try:
            title = response.xpath('//h1/text()').get()
        except:
            pass
        return title

    def get_content(self, response):
        content = "NAN"
        try:
            content = response.xpath('//div[@id="content"]').xpath('string(.)').get()
            content = re.sub(r'全新的短域名 qxs.la 提供更快更稳定的访问，亲爱的读者们，赶紧把我记下来吧：qxs.la （全小说无弹窗）', '', content)
            content = re.sub(r'ad\d\(\);', '', content)
            content = '\t' + content.strip()
        except:
            pass
        return content

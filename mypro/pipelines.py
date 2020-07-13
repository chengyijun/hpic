# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

import scrapy
from scrapy.exporters import JsonLinesItemExporter
from scrapy.pipelines.images import ImagesPipeline

from mypro.settings import IMAGES_STORE
from mypro.tools import get_config


class BoDuoImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        # super().file_path(request, response, info)
        # original_path  'full/%s.jpg'
        item = request.item
        index = request.index
        dname = item['dname']
        # 定义图片保存位置   setting中定义的位置+分类文件夹名称+图片名
        new_path = os.path.join(IMAGES_STORE, dname, '{}.jpg'.format(index + 1))
        return new_path

    def get_media_requests(self, item, info):
        """
        重写父类中的 get_media_requests() 发送多媒体文件请求
        """
        imgs = item['imgs']
        for index, img in enumerate(imgs):
            request = scrapy.Request(img)
            request.item = item
            request.index = index
            yield request


class BjdyPipeline(object):
    def __init__(self):
        self.fp = open("bjdy.json", 'wb')
        self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')
        self.fp.write(b"[")

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        self.fp.write(b',')
        return item

    def close_spider(self, spider):
        self.fp.write(b"]")
        pass


class DmpPipeline(object):
    def __init__(self):
        import pymongo

        config = get_config()
        name = config.get('fiction').get('name')
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["fcitions"]
        self.mycol = self.mydb[name]

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        x = self.mycol.insert_one(dict(item))
        return item

    def close_spider(self, spider):
        self.myclient.close()
        print('*' * 50)
        print('数据已经存入mongodb')

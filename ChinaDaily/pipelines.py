# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

#from itemadapter import ItemAdapter
import csv

from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes
from ChinaDaily.elasticsearch_orm import ChinaDaily_es  #导入elasticsearch操作模块
from ChinaDaily.settings import IMAGES_STORE as images_store
from scrapy.exporters import JsonItemExporter
import os #文件重命名用
import scrapy
import json
import time
import hashlib
import re
import PIL #图片处理所需包，pillow包的升级版
#import MySQLdb
#import codecs



class JsonWithEncodingPipeline(object):
    #自定义json文件的导出
    def __init__(self):
        self.file = open('article.json', 'wb')

    def process_item(self,item,spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.write(lines.encode("utf-8"))
        return item

    def spider_closed(self,spider):
        self.file.close()


#class JsonExporterPipleline(object):
    #调用scrapy提供的json export导出json文件
#    def __init__(self):
#        self.file = open('articleexport.json', 'wb')
#        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
#        self.exporter.start_exporting()
#    def process_item(self, item, spider):
#        self.exporter.export_item(item)
#        return item
#    def close_spider(self, spider):
#        self.exporter.finish_exporting()
#        self.file.close()


#class ArticleImagePipeline(ImagesPipeline):
#    def get_media_requests(self, item, info):
        """
        下载图片用
        :param item:
        :param info:
        :return:
        """
#        front_image_path ='http:' + str(item["thumbnail"])
#        yield scrapy.Request(front_image_path)

class ArticleImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        thumbnail_url = str(item["thumbnail"])
        yield scrapy.Request(thumbnail_url)


    def file_path(self, request, response=None, info=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return 'full/%s.jpg' % (image_guid)




#class MysqlPipeline(object):
#    def __init__(self):
#        self.conn = MySQLdb.connect('127.0.0.1', 'root', '123456','chinadaily',charset="utf8", use_unicode=True)
#       self.cursor = self.conn.cursor()
#    def process_item(self, item, spider):
#        insert_sql = """
#            insert into chinadaily_article(tittle, url, url_object_id, thumbnail , info, content)
#            VALUES (%s, %s, %s, %s, %s, %s)
#        """
#        self.cursor.execute(insert_sql, (item["tittle"], item["url"], item["url_object_id"], item["thumbnail"] ,item["info"], item["content"]))
#        self.conn.commit()


from ChinaDaily.elasticsearch_orm import ChinaDaily_es
# 去除html　tags
from w3lib.html import remove_tags


class ElasticsearchPipeline(object):
    # 将数据写入到ES中

    def process_item(self,item,spider):
        # 将item转换为ES的数据
        article = ChinaDaily_es()

        article.thumbnail = item['thumbnail']
        article.title = item['title']
        article.url = item['url']
        article.url_object_id = item['url_object_id']
        article.content = item['content']
        article.category = item['category']
        article.author = item['author']


        article.save()

        return item

class CSVPipeline(object):
    def __init__(self):
        self.f = open("article.csv", "w")
        self.writer = csv.writer(self.f)
        self.writer.writerow(['thumbnail', 'title', 'url', 'url_object_id','content','path'])

    def process_item(self, item, spider):
        article_list =  [item['thumbnail'], item['title'], item['url'], item['url_object_id'],item['content'], item['path']]

        self.writer.writerow(article_list)
        return item
    def close_spider(self, spider):#关闭
        self.writer.close()
        self.f.close()
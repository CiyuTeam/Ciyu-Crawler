# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from ChinaDaily.elasticsearch_orm import ChinaDaily_es  #导入elasticsearch操作模块




class ChinadailyArticleItem(scrapy.Item):
    #文章列表栏图片url
    thumbnail = scrapy.Field()
    #文章标题
    title = scrapy.Field()
    #文章url
    url = scrapy.Field()
    #文章url转码为md5码
    url_object_id = scrapy.Field()
    #文章正文
    content = scrapy.Field()
    #图片本地路径
    path = scrapy.Field()
    #文章分类
    category = scrapy.Field()
    #作者
    author = scrapy.Field()

    def save_to_es(self):
        cd = ChinaDaily_es()  # 实例化elasticsearch(搜索引擎对象)
        cd.thumbnail = self['thumbnail'] #字段名称 = 值
        cd.title = self['title']
        cd.url = self['url']
        cd.url_object_id = self['url_object_id']
        cd.content = self['content']
        cd.category = self['category']
        cd.author = self['author']
        cd.save()  # 将数据写入elasticsearch(搜索引擎对象)
        return

    #来源、作者、发布时间
    #info = scrapy.Field()
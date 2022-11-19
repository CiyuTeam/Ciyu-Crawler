
from datetime import datetime
from elasticsearch_dsl import Document, Date, Nested, Boolean, \
    analyzer,  Completion, Keyword, Text, Integer

# elasticsearch(搜索引擎)的mapping映射管理

from elasticsearch_dsl.connections import connections       # 导入连接elasticsearch(搜索引擎)服务器方法
connections.create_connection(hosts=['127.0.0.1'])

class ChinaDaily_es(Document):        # 自定义一个类来继承DocType类

    # Text类型需要分词，所以需要知道中文分词器，ik_max_word为中文分词器
    thumbnail = Keyword()
    # 文章标题
    title = Text(analyzer="ik_max_word")
    # 文章url
    url = Keyword()
    # 文章url转码为md5码
    url_object_id = Keyword()
    # 文章正文
    content = Text(analyzer="ik_max_word")


    class Index:                                                             # Meta是固定写法
        name = "ciyu"                                                # 设置索引名称(相当于数据库名称)
        doc_type = 'article'                                                # 设置表名称

if __name__ == "__main__":          # 判断在本代码文件执行才执行里面的方法，其他页面调用的则不执行里面的方法
    ChinaDaily_es.init()                # 生成elasticsearch(搜索引擎)的索引，表，字段等信息



# 使用方法说明：
# 在要要操作elasticsearch(搜索引擎)的页面，导入此模块
# lagou = lagouType()           #实例化类
# lagou.title = '值'            #要写入字段=值
# lagou.description = '值'
# lagou.keywords = '值'
# lagou.url = '值'
# lagou.riqi = '值'
# lagou.save()                  #将数据写入elasticsearch(搜索引擎)
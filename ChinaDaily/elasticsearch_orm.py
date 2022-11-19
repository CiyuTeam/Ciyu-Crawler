
from datetime import datetime
from elasticsearch_dsl import Document, Date, Nested, Boolean, \
    analyzer,  Completion, Keyword, Text, Integer

# elasticsearch(��������)��mappingӳ�����

from elasticsearch_dsl.connections import connections       # ��������elasticsearch(��������)����������
connections.create_connection(hosts=['[your elasticsearch host]'], http_auth=('[your elasticsearch username]', '[your elasticsearch password]'))

class ChinaDaily_es(Document):        # �Զ���һ�������̳�DocType��

    # Text������Ҫ�ִʣ�������Ҫ֪�����ķִ�����ik_max_wordΪ���ķִ���
    thumbnail = Keyword()
    # ���±���
    title = Text(analyzer="ik_max_word")
    # ����url
    url = Keyword()
    # ����urlת��Ϊmd5��
    url_object_id = Keyword()
    # ��������
    content = Text(analyzer="ik_max_word")
    category = Keyword()
    author = Keyword()


    class Index:                                                             # Meta�ǹ̶�д��
        name = "ciyu"                                                # ������������(�൱�����ݿ�����)
        doc_type = 'article'                                                # ���ñ�����

if __name__ == "__main__":          # �ж��ڱ������ļ�ִ�в�ִ������ķ���������ҳ����õ���ִ������ķ���
    ChinaDaily_es.init()                # ����elasticsearch(��������)�����������ֶε���Ϣ



# ʹ�÷���˵����
# ��ҪҪ����elasticsearch(��������)��ҳ�棬�����ģ��
# lagou = lagouType()           #ʵ������
# lagou.title = 'ֵ'            #Ҫд���ֶ�=ֵ
# lagou.description = 'ֵ'
# lagou.keywords = 'ֵ'
# lagou.url = 'ֵ'
# lagou.riqi = 'ֵ'
# lagou.save()                  #������д��elasticsearch(��������)

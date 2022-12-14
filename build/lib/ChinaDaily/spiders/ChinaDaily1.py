import hashlib
from urllib import parse

import scrapy
from scrapy.http import Request
from scrapy.utils.python import to_bytes

from ChinaDaily.items import ChinadailyArticleItem
from ChinaDaily.utils.common import get_md5


class Chinadaily1Spider(scrapy.Spider):
    count = 0
    name = 'ChinaDaily1'
    allowed_domains = ['chinadaily.com.cn']
    start_urls = ['http://www.chinadaily.com.cn/china/governmentandpolicy', ]
    """
                      'http://www.chinadaily.com.cn/china/society',
                  'http://www.chinadaily.com.cn/china/scitech',
                  'http://www.chinadaily.com.cn/china/education',
                  'http://www.chinadaily.com.cn/china/coverstory',
                  'http://www.chinadaily.com.cn/china/environment',
                  'http://www.chinadaily.com.cn/world/asia_pacific',
                  'http://www.chinadaily.com.cn/world/america',
                  'http://www.chinadaily.com.cn/world/europe',
                  'http://www.chinadaily.com.cn/world/middle_east',
                  'http://www.chinadaily.com.cn/world/africa',
                  'http://www.chinadaily.com.cn/world/china-us',
                  'http://www.chinadaily.com.cn/world/cn_eu',
                  'http://www.chinadaily.com.cn/world/china-africa',
                  'http://www.chinadaily.com.cn/life/celebrity',
                  'http://www.chinadaily.com.cn/life/fashion',
                  'http://www.chinadaily.com.cn/life/people',
                  'http://www.chinadaily.com.cn/food',
                  'http://www.chinadaily.com.cn/travel/news',
                  'http://www.chinadaily.com.cn/travel/citytours',
                  'http://www.chinadaily.com.cn/travel/guidesandtips',
                  'http://www.chinadaily.com.cn/travel/footprint',
                  'http://www.chinadaily.com.cn/travel/aroundworld',
                  'http://www.chinadaily.com.cn/business/economy',
                  'http://www.chinadaily.com.cn/business/companies',
                  'http://www.chinadaily.com.cn/business/biz_industries',
                  'http://www.chinadaily.com.cn/business/tech',
                  'http://www.chinadaily.com.cn/business/motoring',
                  'http://www.chinadaily.com.cn/business/money',
                  'http://www.chinadaily.com.cn/opinion/editionals',
                  'http://www.chinadaily.com.cn/opinion/op-ed',
                  'http://www.chinadaily.com.cn/opinion/columnists',
                  'http://www.chinadaily.com.cn/opinion/commentator'
    """

    def parse(self, response):
        """
        1.?????????????????????????????????url?????????scrapy?????????????????????
        2.??????????????????url?????????scrapy????????????????????????????????????parse??????
        :param response:
        :return:
        """

        # ???????????????????????????????????????url?????????scrapy????????????????????????
        post_nodes = response.css(".tw3_01_2 .tw3_01_2_p a")
        for post_node in post_nodes:
            post_url = post_node.css("::attr(href)").extract_first("")
            image_url = post_node.css("img::attr(src)").extract_first("")

            yield Request(parse.urljoin(response.url, post_url), meta={"front-image-url": image_url},
                          callback=self.parse_detail)
            # yield Request(url=parse.urljoin(response.url,post_url),callback = self.parse_detail)-
        # ????????????????????????scrapy????????????
        next_url = response.css(".next a::attr(href)").extract_first("")
        if next_url:  # ????????????????????? and self.count < 20
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
            self.count += 1

    def parse_detail(self, response):
        global content
        content = ''
        article_item = ChinadailyArticleItem()
        # ???????????????????????????
        thumbnail = 'http:' + response.meta.get("front-image-url", "")  # ???????????????
        image_guid = hashlib.sha1(to_bytes('http:' + thumbnail)).hexdigest()
        path = '%s.jpg' % (image_guid)
        title = response.xpath('//*[@id="lft-art"]/h1/text()').extract()[0]
        # info = response.xpath('//*[@id="lft-art"]/div[1]/span[1]/text()').extract()[0].strip()
        passage = response.xpath('//*[@id="Content"]/p/text()')
        for item in passage.extract():
            content = content + item

        pass

        article_item["thumbnail"] = thumbnail
        article_item["title"] = title
        article_item["url"] = response.url
        article_item["url_object_id"] = get_md5(response.url)
        # article_item["info"] = info
        article_item["content"] = content
        article_item["path"] = path

        yield article_item

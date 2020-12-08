
##主要是获取到book_url
import scrapy
from scrapy_redis.spiders import RedisSpider
from ..items import XmlyBook
import pymongo

class XmlyBookSpider(RedisSpider):
    name = 'xmly_book'
    # allowed_domains = ['ximalaya.com']
    # start_urls = ['http://ximalaya.com/']
    redis_key = 'xmly_cate:start_urls'


    def parse(self, response):
        next_page = response.xpath('//ul[@class="pagination-page _Xo"]/li[last()-1]/a/span/text()').extract()
        if len(next_page) >= 1:
            next_page = next_page[0]
        else:
            next_page = 1
        for page in range(1, int(next_page) + 1):
            houzi = "p" + str(page) + "/"
            url_next = response.url + houzi
            yield scrapy.Request(url_next, callback=self.parse_url)

    def parse_url(self,response):
        content = response.xpath('//div[@class="content"]/ul/li')
        for li_c in content:
            item = XmlyBook()
            href = 'https://www.ximalaya.com' + "".join(li_c.xpath('.//a[contains(@class,"album-title")]/@href').extract())
            item['book_url'] = href
            item['status'] = 0
            yield item


    # def start_requests(self):
    #     self.client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
    #     self.db = self.client['xmly']
    #     self.collection = self.db['xmlycate']
    #     url_cate = self.collection.find()
    #     for url in url_cate:
    #         url_ = url['cate_url']
    #         yield scrapy.Request(url_,callback=self.parse)
    #
    # def parse(self, response):
    #     next_page = response.xpath('//ul[@class="pagination-page _Xo"]/li[last()-1]/a/span/text()').extract()
    #     if len(next_page) >= 1:
    #         next_page = next_page[0]
    #     else:
    #         next_page = 1
    #     for page in range(1, int(next_page) + 1):
    #         houzi = "p" + str(page) + "/"
    #         url_next = response.url + houzi
    #         yield scrapy.Request(url_next, callback=self.parse_url)
    #
    #
    # def parse_url(self,response):
    #     content = response.xpath('//div[@class="content"]/ul/li')
    #     for li_c in content:
    #         item = XmlyBook()
    #         href = 'https://www.ximalaya.com' + "".join(li_c.xpath('.//a[contains(@class,"album-title")]/@href').extract())
    #         item['book_url'] = href
    #         item['status'] = 0
    #         yield item







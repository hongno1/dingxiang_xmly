# -*- coding: utf-8 -*-

###全量的喜马拉雅数据爬取
import scrapy
from ..items import XmlyInfo
import re
import datetime
import json


from scrapy_redis.spiders import RedisSpider
class XmlysppppppSpider(RedisSpider):
    name = 'xmly_sp'
    redis_key = 'xmly:taskrw'

    def make_requests_from_url(self, url):
        try:
            r = self.server
            # print(url)
            data =url
            app_json = json.loads(data)
            type = str(app_json["type"])
            rel_url = str(app_json["url"])
            if type =="0":
                print("频道")
                return scrapy.Request(rel_url, dont_filter=True, meta={'item':data}, callback=self.parse)
            elif type == "1":
                print("专辑")
                print(data)
                r.lpush("xmly::start_urls", data)
            elif type == "2":
                print("单集")
                r.lpush("xmlydanji:linkssssd", data)
            # return scrapy.Request(rel_url, dont_filter=True, meta=meta, callback=self.parse)
            # return scrapy.Request(rel_url, dont_filter=True, meta=meta, callback=self.parse)
        except Exception as e:
            print(e)

    ## 专辑的链接开始解析  https://www.ximalaya.com/gerenchengzhang/24785128/
    def parse(self, response):
        meta = response.meta
        next_page = response.xpath('//ul[@class="pagination-page _Xo"]/li[last()-1]/a/span/text()').extract()
        if len(next_page) >= 1:
            next_page = next_page[0]
        else:
            next_page = 1
        for page in range(1, int(next_page) + 1):
            houzi = "p" + str(page) + "/"
            url_next = response.url + houzi
            yield scrapy.Request(url_next, callback=self.parse_url,meta=meta)

    def parse_url(self,response):
        content = response.xpath('//div[@class="content"]/ul/li')
        meta = response.meta
        data =meta['item']
        print(data)
        # print(type(data))
        # exit()
        for li_c in content:
            href = 'https://www.ximalaya.com' + "".join(li_c.xpath('.//a[contains(@class,"album-title")]/@href').extract())
            jsons = json.loads(data)
            jsons['url'] = href
            # print(str(jsons))
            # print(json.dumps(jsons))
            # print(type(json.dumps(jsons)))
            r = self.server
            r.lpush("xmly::start_urls", json.dumps(jsons))





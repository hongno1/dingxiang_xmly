import scrapy
##主要用于对关键词的爬虫进行爬取
from scrapy_redis.spiders import RedisSpider
import json
import re
from redis import Redis

r_dis = Redis(host='localhost', port=6379)

class XmlySpKewwordSpider(RedisSpider):
    name = 'xmly_sp_kewword'
    redis_key = 'xmly:taskkeyword'

    def make_requests_from_url(self, url):
        try:
            data = url
            data_info = json.loads(data)
            keyword = str(data_info['keyword'])
            headers = {
                'authority': 'www.ximalaya.com',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
            }

            params = (
                ('core', 'album'),
                #     ('kw', '\u8FDB\u535A\u4F1A'),
                ('kw', keyword),
                ('page', '1'),
                ('spellchecker', 'true'),
                ('rows', '10'),
                ('condition', 'relation'),
                ('device', 'iPhone'),
                ('fq', ''),
                ('paidFilter', 'false'),
            )
            url_keyword = 'https://www.ximalaya.com/revision/search/main'
            return scrapy.Request(url_keyword, params=params, headers=headers, meta={'item': data}, dont_filter=True, callback=self.parse)

        except Exception as e:
            print(e)

    def parse(self, response):
        item = response.meta['item']
        data = json.loads(response.text)
        docs = data.get('data').get('album').get('docs')
        for doc in docs:
            jsons = json.loads(item)
            url = doc.get('url')
            title = doc.get('title')
            jsons['album_url'] = url
            jsons['title'] = title
            # url_zuanji = []
            # dic_zj = {}

            # dic_zj['url'] = url
            # dic_zj['title'] = title
            # url_zuanji.append(dic_zj)
            r_dis.lpush("xmly_keyword:urls", json.dumps(jsons))


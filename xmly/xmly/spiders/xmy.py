# -*- coding: utf-8 -*-
import scrapy
from ..items import XmlyItem
from lxml import html
import re
import json

class XmySpider(scrapy.Spider):
    name = 'xmy'
    allowed_domains = ['ximalaya.com']
    start_urls = ['https://www.ximalaya.com/keji/']

    def start_requests(self):
        for page in range(1,31):
            base_url = 'https://www.ximalaya.com/keji/'
            url = base_url + 'p'+ str(page) +'/'
            print(url)
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        # tree = html.etree
        # body = tree.HTML(response.text)
        content = response.xpath('//div[@class="content"]/ul/li')
        print(len(content))
        for li_c in content:
            item = XmlyItem()
            item['image'] = "".join(li_c.xpath('.//a[contains(@class,"album-cover")]/img/@src').extract())
            item['count'] = "".join(li_c.xpath('.//p[contains(@class,"listen-count")]/span/text()').extract())
            item['name'] = "".join(li_c.xpath('.//a[contains(@class,"album-title")]/span[contains(@class,"v-m")]/text()').extract())
            href = 'https://www.ximalaya.com' + "".join(li_c.xpath('.//a[contains(@class,"album-title")]/@href').extract())
            item['href'] = href
            item['company'] = "".join(li_c.xpath('.//a[contains(@class,"album-author")]/text()').extract())
            company_href = 'https://www.ximalaya.com/'+ "".join(li_c.xpath('.//a[contains(@class,"album-author")]/@href').extract())
            item['company_href'] = company_href

            yield scrapy.Request(item['href'],callback=self.parse_detail,meta={'item':item})

    def parse_detail(self,response):
        item = response.meta['item']
        next_page = response.xpath('//ul[@class="pagination-page _Xo"]/li[last()-1]/a/span/text()').extract()
        if len(next_page) > 0:
            next_page = next_page[0]
        else:
            next_page = 1

        for p in range(1, int(next_page) + 1):
            albumId = "".join(re.findall('https://www.ximalaya.com/keji/(.*?)/',item['href']))
            pageNum = str(p)

            # data = {"albumId":albumId, "pageNum":pageNum}
            detail_url = 'https://www.ximalaya.com/revision/album/v1/getTracksList?albumId={}&pageNum={}'.format(albumId,pageNum)
            print(detail_url)
            yield scrapy.Request(detail_url, callback=self.parse_loc,meta={"item":item})


    def parse_loc(self,response):
        item = response.meta['item']
        detail_json = json.loads(response.text)
        for dj in detail_json['data']['tracks']:
            item['detail_id'] = dj.get('index')
            item['track_id'] = dj.get('trackId')
            item['detail_title'] = dj.get('title')
            item['detail_count'] = dj.get('playCount')
            item['detail_href'] = 'https://www.ximalaya.com'+dj.get('url')
            item['detail_year'] = dj.get('createDateFormat')
            # video_href = "".join(re.findall('https://www.ximalaya.com/keji/21685160/194763602',item['detail_href']))

            yield item

##主要是获取到url类别
import scrapy
from ..items import XmlyCate

class XmlyCateSpider(scrapy.Spider):
    name = 'xmly_cate'
    allowed_domains = ['ximalaya.com']
    start_urls = ['https://www.ximalaya.com/category/']

    def parse(self, response):
        category = response.xpath('//div[@class="plates _AK"]//div[@class="list _AK"]/a')

        for ca in category:
            item = XmlyCate()
            url = "".join(ca.xpath('./@href').extract())
            ###各个类别的url合计
            url_category = 'https://www.ximalaya.com' + url
            item['cate_url'] = url_category
            yield item
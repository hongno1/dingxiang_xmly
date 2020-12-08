# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
import re
import datetime
import dateparser
import json
from ..items import XmlyUpdate

class XmlyUpdateSpider(RedisSpider):
    name = 'xmly_update'
    redis_key = 'xmly_cate:start_urls'

    def parse(self, response):
        url = response.url
        category = "".join(re.findall("https://www.ximalaya.com/(\w+)/\w+/", url))
        subcategory = "".join(re.findall("https://www.ximalaya.com/\w+/(\w+)/", url))
        url_list = 'https://www.ximalaya.com/revision/category/queryCategoryPageAlbums?category={category}&subcategory={subcategory}&meta=&sort=1&page=1&perPage=1000'.format(
            subcategory=subcategory, category=category)

        yield scrapy.Request(url_list, callback=self.parse_url, dont_filter=True)

    def parse_url(self,response):
        data_list = json.loads(response.text)
        if data_list.get('ret') == 200:
            albums = data_list.get('data').get('albums')
            for album in albums:
                albumId = album.get('albumId')
                title = album.get('title')
                playCount = album.get('playCount')
                trackCount = album.get('trackCount')

                if int(trackCount) > 1000:
                    pageNums = int(int(trackCount) / 1000) + 1
                    for pageNum in range(1, pageNums + 1):
                        url_tracks = 'https://www.ximalaya.com/revision/album/v1/getTracksList?albumId={albumId}&pageNum={pageNum}&sort=1&pageSize=1000'.format(
                            albumId=albumId, pageNum=pageNum)
                        yield scrapy.Request(url_tracks, callback=self.parse_tracks, dont_filter=True)
                else:
                    url_tracks = 'https://www.ximalaya.com/revision/album/v1/getTracksList?albumId={albumId}&pageNum=1&sort=1&pageSize={trackCount}'.format(
                        albumId=albumId, trackCount=trackCount)
                    yield scrapy.Request(url_tracks, callback=self.parse_tracks, dont_filter=True)

    def parse_tracks(self,response):
        data_tracks = json.loads(response.text)
        if data_tracks.get('ret') == 200:
            tracks = data_tracks.get('data').get('tracks')
            for track in tracks:
                createDateFormat = track.get('createDateFormat')
                if createDateFormat == '刚刚':
                    update_time = datetime.datetime.now()
                else:
                    update_time = dateparser.parse(createDateFormat)

                now_time = datetime.datetime.now()
                start_end_time_seconds = (now_time - update_time).total_seconds()
                if int(start_end_time_seconds) < 86400:
                    trackId = track.get('trackId')
                    url = 'https://www.ximalaya.com/revision/track/trackPageInfo?trackId={trackId}'.format(trackId=trackId)
                    item = XmlyUpdate()
                    item['update_url'] = url
                    yield item
                else:
                    break
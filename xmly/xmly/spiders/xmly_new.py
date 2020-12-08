# -*- coding: utf-8 -*-
##实现增量爬虫
import scrapy
import datetime
from scrapy_redis.spiders import RedisSpider
import json
from ..items import XmlyInfo


class XmlyNewSpider(RedisSpider):
    name = 'xmly_new'
    redis_key = 'xmly_update:start_urls'

    def parse(self, response):
        datas = json.loads(response.text)
        if datas.get('ret') == 200:
            try:
                data_trackInfo = datas.get('data').get('trackInfo')
                data_albumInfo = datas.get('data').get('albumInfo')
                trackId = data_trackInfo.get('trackId')

                labels = datas.get('data').get('metas')
                label = []
                for l in labels:
                    metaname = l.get('metaDisplayName')
                    label.append(metaname)

                label = ",".join(label)
                book_id = data_albumInfo['albumId']
                book_name = data_albumInfo['title']
                introduction = data_albumInfo['description']
                link_ = data_trackInfo['link']
                id = link_.replace('/', '')
                link = "https://www.ximalaya.com" + link_
                score = ''
                play_count = data_trackInfo['playCount']
                play_sum = data_albumInfo['playCount']
                times = data_trackInfo['lastUpdate']
                title = data_trackInfo['title']
                catagory = datas['data']['category']['categoryTitle']

                item = XmlyInfo()
                item['id'] = id
                item['label'] = label
                item['book_id'] = book_id
                item['book_name'] = book_name
                item['introduction'] = introduction
                item['link'] = link
                item['score'] = score
                item['play_count'] = play_count
                item['play_sum'] = play_sum
                item['times'] = times
                item['title'] = title
                item['catagory'] = catagory

                if data_trackInfo['isAuthorized'] == True:
                    video_url = 'https://www.ximalaya.com/revision/play/v1/audio?id={}&ptype=1'.format(trackId)
                    yield scrapy.Request(video_url, callback=self.parse_down, dont_filter=True, meta={'item': item})
                else:
                    is_down = 0
                    addtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    status = 0

                    item['is_down'] = is_down
                    item['addtime'] = addtime
                    item['local_path'] = ''
                    item['status'] = status
                    yield item
            except Exception as e:
                print(e)

    def parse_down(self,response):
        item = response.meta['item']
        down_json = json.loads(response.text)
        if down_json.get('ret') == 200:
            url_down = down_json['data']['src']
        else:
            url_down = ''

        addtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = 0
        item['local_path'] = url_down
        item['is_down'] = 0
        item['addtime'] = addtime
        item['status'] = status
        yield item

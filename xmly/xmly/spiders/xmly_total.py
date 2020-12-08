# -*- coding: utf-8 -*-

###全量的喜马拉雅数据爬取
import os
import time
import urllib

import scrapy
from ..items import XmlyInfo
import re
import datetime
import json
import requests
import hashlib
from redis import Redis
redis = Redis(host='localhost', port=6379)

from scrapy_redis.spiders import RedisSpider
class XmlyTotalSpider(RedisSpider):
    name = 'xmly_total'
    redis_key = 'xmly::start_urls'

    def make_requests_from_url(self, url):
        print(333333333333333333333)
        print(url)
        print(4444444444444444444444)
        app_json = json.loads(url)
        curl = app_json['url']
        print(curl)
        return scrapy.Request(curl, dont_filter=True, meta={'datasss': app_json}, callback=self.parse)


    # 专辑的链接开始解析  https://www.ximalaya.com/xiangsheng/35105051/
    def parse(self, response):

        item = XmlyInfo()
        url_ = response.url
        datasss = response.meta.get('datasss')
        # print(datasss)
        # print(type(datasss))
        item['data'] = datasss
        ##专辑名
        book_name = "".join(response.xpath('//h1[@class="title vA_"]/text()').extract())
        item['book_name'] = book_name

        book_id = "".join(re.findall('https://www.ximalaya.com/\w+/(\w+)', url_))
        item['book_id'] = book_id
        ##评分
        score = "".join(response.xpath('//span[@class="d-ib v-m vA_"]/text()').extract()).replace('分', '')
        item['score'] = score
        ##label
        label = response.xpath('//div[@class="xui-tag tag _Pt"]//span[@class="xui-tag-text"]//a//text()').extract()
        label = ",".join(label)
        item['label'] = label
        ##简介
        introduction = " ".join(response.xpath('//article[@class="intro ge_"]//p//text()').extract())
        item['introduction'] = introduction

        ##总播放量
        play_sum = "".join(response.xpath('//span[@class="count vA_"]/text()').extract())
        item['play_sum'] = play_sum

        detail_page = response.xpath('//ul[@class="pagination-page WJ_"]/li[last()-1]/a/span/text()').extract()
        if len(detail_page) >= 1:
            detail_page = detail_page[0]
        else:
            detail_page = 1

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
        }
        for page in range(1, int(detail_page)+1):
            url_track = 'https://www.ximalaya.com/revision/album/v1/getTracksList?albumId={}&pageNum={}'.format(book_id,str(page))
            yield scrapy.Request(url_track,callback=self.parse_info, headers=headers, dont_filter=True, meta={'item':item})

    ##https://www.ximalaya.com/revision/album/v1/getTracksList?albumId=24785128&pageNum=4
    def parse_info(self,response):
        item = response.meta.get('item')

        data = json.loads(response.text)
        if data.get('ret') == 200:
            for track in data['data']['tracks']:

                title = track.get('title')
                trackId = track.get('trackId')
                url_d = 'https://www.ximalaya.com'+ track.get('url')
                url = track.get('url')
                id_ = url.replace('/','')
                playCount = track.get('playCount')
                tag = track.get('tag')

                duration = track.get('duration')
                try:
                    duration = int(duration)
                except:
                    duration = 0

                item['title'] = title
                # item['trackId'] = trackId
                item['id'] = id_
                item['link'] = url_d
                item['play_count'] = playCount
                item['duration'] = duration

                yield scrapy.Request(url_d,callback=self.parse_detail,dont_filter=True,meta={'item':item,'tag':tag,'trackId':trackId})

    ### 详情页链接 https://www.ximalaya.com/youshengshu/3144814/337147690


    def parse_detail(self,response):
        item = response.meta['item']
        tag = response.meta.get('tag')
        trackId = response.meta.get('trackId')

        ###作者
        author = "".join(response.xpath('//div[@class="anchor-info-head gK_"]/p[@class="anchor-info-nick gK_"]/a/text()').extract())
        item['author'] = author

        ##出版时间
        times = "".join(response.xpath('//span[@class="time _Td"]/text()').extract())
        ##出版类别
        catagory = "".join(response.xpath('//div[@class="category _uv"]/a/text()').extract())

        ##评论数
        commentCount = "".join(response.xpath('//h2[@class="xm-comment-title aC_"]/text()').extract()).replace('用户评论(',
                                                                                                               '').replace(
            ')', '')
        if commentCount == '':
            commentCount = 0
        elif '万' in commentCount:
            num = float(commentCount.replace('万', ''))
            commentCount = int(num * 10000)
        else:
            commentCount = int(commentCount)

        ##封面的图链接图

        cover_url = "".join(response.xpath('//img[@class="img nj_"]/@src').extract())
        cover_url = "http:" +cover_url
        vid_im = hashlib.md5(cover_url.encode(encoding='UTF-8')).hexdigest()
        host_path = 'D:/audio'
        timeArray = time.localtime(int(time.time()))
        dt = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        createtimes = dt.split(' ')[0].replace('-', '')
        path_im = host_path + '/%s/%s.jpg' % (createtimes, vid_im)

        if not os.path.exists(host_path + '/%s/' % (createtimes)):
            os.makedirs(host_path + '/%s/' % (createtimes))
        try:
            urllib.request.urlretrieve(cover_url, path_im)

            ##传的图片路径
            local_img = '/audio/%s/%s.jpg' % (createtimes, vid_im)
            item['local_img'] = local_img
        except:
            item['local_img'] = ''
        ##摘要
        description = item['introduction']

        item['commentCount'] = commentCount
        item['times'] = times
        item['catagory'] = catagory

        ##判断此音频是否为付费音频 0为可下载的
        if tag == 0:
            video_url = 'https://www.ximalaya.com/revision/play/v1/audio?id={}&ptype=1'.format(trackId)
            yield scrapy.Request(video_url, callback=self.parse_down, dont_filter=True, meta={'item': item})

        else:
            addtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['local_path'] = ''
            item['isDown'] = 0
            item['addtime'] = addtime
            item['status'] = item['id']
            print(222222222222222222)
            print(item)
            datasss = item['data']
            postbody = [{
                        "imgPath": item['local_img'],
                        "description": item['introduction'],
                        "isDown": 0,
                        "audio_time": 0,

                        "audioId": item['id']+str(int(time.time())),
                        "taskId":datasss['taskId'],
                        "level":int(datasss['level']),
                        "ruleId":datasss['ruleId'],
                        "taskType":datasss['taskType'],
                        "url":item['link'],
                        "filePath":item['local_path'],
                        "title":item['title'],
                        "source":datasss['source'],
                        "column":item['catagory'],
                        "label":item['label'],
                        "author":item['author'],
                        "playCount":int(item['play_count']),
                        "commentCount":item['commentCount'],
                        "addTime":item['addtime'],
                        "releaseTime":item['times'],
                        "nlpSwitch":int(datasss['nlpSwitch']),
                        "voiceToTextSwitch":int(datasss['voiceToTextSwitch']),
                        "type": datasss['type']
                        }]
            print(postbody)
            # print(99999999999999999999999999999)
            # exit()
            #传输数据
            r = requests.post(url='http://192.168.31.156:5012/microserver-businessManagement/task/api/python/insert', data=json.dumps(postbody),headers={'Content-Type': 'application/json'})
            print(r.status_code)
            # exit()
            yield item

    def parse_down(self,response):
        item = response.meta['item']
        down_json = json.loads(response.text)
        if down_json.get('ret') == 200:
            url_down = down_json['data']['src']

            if url_down != None:
                Header = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 QQBrowser/10.4.3469.400'
                }
                # res = requests.get(url_down, headers=Header, timeout=30)
                vid = hashlib.md5(url_down.encode(encoding='UTF-8')).hexdigest()
                host_path ='D:/audio'
                timeArray = time.localtime(int(time.time()))
                dt = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                createtimes = dt.split(' ')[0].replace('-', '')
                path = host_path + '/%s/%s.m4a' % (createtimes, vid)

                if not os.path.exists(host_path + '/%s/' % (createtimes)):
                    os.makedirs(host_path + '/%s/' % (createtimes))

                urllib.request.urlretrieve(url_down,path)
                local_path = '/audio/%s/%s.m4a' % (createtimes, vid)

                addtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                status = 0
                item['local_path'] = local_path
                item['isDown'] = 1
                item['addtime'] = addtime
                item['status'] = status
                print(1111111111111111111111111)
                datasss = item['data']
                postbody = [{
                    "imgPath": item['local_img'],  ##图片路径
                    "description": item['introduction'],  ##摘要
                    "isDown": 1,
                    "audio_time": item['duration'],

                    "audioId": item['id'] + str(int(time.time())),
                    "taskId": datasss['taskId'],
                    "level": int(datasss['level']),
                    "ruleId": datasss['ruleId'],
                    "taskType": datasss['taskType'],
                    "url": item['link'],
                    "filePath": item['local_path'],
                    "title": item['title'],
                    "source": datasss['source'],
                    "column": item['catagory'],
                    "label": item['label'],
                    "author": item['author'],
                    "playCount": int(item['play_count']),
                    "commentCount": item['commentCount'],
                    "addTime": item['addtime'],
                    "releaseTime": item['times'],
                    "nlpSwitch": int(datasss['nlpSwitch']),
                    "voiceToTextSwitch": int(datasss['voiceToTextSwitch']),
                    "type": datasss['type']
                }]

                redis.lpush('xmly_comment:start_urls', json.dumps(postbody[0]))
                print(postbody)
                # r = requests.post(url='http://172.18.155.31:5012/microserver-businessManagement/task/api/python/insert',data=json.dumps(postbody), headers={'Content-Type': 'application/json'})
                r = requests.post(
                    url='http://192.168.31.156:5012/microserver-businessManagement/task/api/python/insert',
                    data=json.dumps(postbody), headers={'Content-Type': 'application/json'})

                print(r.status_code)
                yield item

            else:
                addtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                status = 0
                item['local_path'] = ''
                item['isDown'] = 0
                item['addtime'] = addtime
                item['status'] = status
                print(1111111111111111111111111)
                datasss = item['data']
                postbody = [{
                    "imgPath": item['local_img'],  ##图片路径
                    "description": item['introduction'],  ##摘要
                    "isDown": 0,
                    "audio_time": 0,

                    "audioId": item['id'] + str(int(time.time())),
                    "taskId": datasss['taskId'],
                    "level": int(datasss['level']),
                    "ruleId": datasss['ruleId'],
                    "taskType": datasss['taskType'],
                    "url": item['link'],
                    "filePath": item['local_path'],
                    "title": item['title'],
                    "source": datasss['source'],
                    "column": item['catagory'],
                    "label": item['label'],
                    "author": item['author'],
                    "playCount": int(item['play_count']),
                    "commentCount": item['commentCount'],
                    "addTime": item['addtime'],
                    "releaseTime": item['times'],
                    "nlpSwitch": int(datasss['nlpSwitch']),
                    "voiceToTextSwitch": int(datasss['voiceToTextSwitch']),
                    "type": datasss['type']
                }]

                redis.lpush('xmly_comment:start_urls', json.dumps(postbody[0]))
                print(postbody)
                # r = requests.post(url='http://172.18.155.31:5012/microserver-businessManagement/task/api/python/insert',data=json.dumps(postbody), headers={'Content-Type': 'application/json'})
                r = requests.post(
                    url='http://192.168.31.156:5012/microserver-businessManagement/task/api/python/insert',
                    data=json.dumps(postbody), headers={'Content-Type': 'application/json'})

                print(r.status_code)
                yield item




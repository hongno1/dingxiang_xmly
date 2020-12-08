import datetime

import scrapy
from scrapy_redis.spiders import RedisSpider
import json
import re
import requests
import requests
import time
import hashlib
import urllib
import os

from redis import Redis
redis = Redis(host='localhost', port=6379)

class XmlyDanjianSpider(RedisSpider):
    name = 'xmly_danjian'
    # allowed_domains = ['ximalaya.com']
    # start_urls = ['http://ximalaya.com/']
    redis_key = 'xmlydanji:linkssssd'

    ##url传入的是json的字符串
    def make_requests_from_url(self, url):
        print(333333333333333333333)
        print(url)
        print(4444444444444444444444)
        app_json = json.loads(url)
        curl = app_json['url']
        print(curl)

        return scrapy.Request(curl, dont_filter=True, meta={'datasss': app_json}, callback=self.parse)

    ## https://www.ximalaya.com/gerenchengzhang/24785128/254862026
    def parse(self, response):
        url_info = response.url
        datasss = response.meta['datasss']
        id_ = "".join(re.findall('www.ximalaya.com/(.*)', url_info)).replace('/', '')
        book_id = "".join(re.findall('www.ximalaya.com/\w+/(\w+)/\w+', url_info))
        trackId = "".join(re.findall('www.ximalaya.com/\w+/\w+/(\w+)', url_info))

        ##简介描述
        introduction = ",".join(response.xpath('//article[@class="intro  eX_"]/p//text()').extract())

        ##出版时间
        times = "".join(response.xpath('//span[@class="time _uv"]/text()').extract())
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

        title = ", ".join(response.xpath('//div[@class="info _uv"]/h1/text()').extract())
        label = ", ".join(response.xpath('//div[@class="tags _uv"]//a//text()').extract())
        author = "".join(response.xpath('//a[@class="nick-name gK_"]/text()').extract())
        play_count = "".join(response.xpath('//span[@class="count _uv"]/text()').extract())
        if '万' in play_count:
            f_play = float(play_count.replace('万', ''))
            read_count = int(f_play * 10000)
        elif '亿' in play_count:
            f_p = float(play_count.replace('亿', ''))
            read_count = int(f_p * 100000000)
        elif play_count != '':
            try:
                read_count = int(play_count)
            except:
                read_count = 0

        times = "".join(response.xpath('//span[@class="time _uv"]/text()').extract())

        ##封面的图链接图
        cover_url = "".join(response.xpath('//img[@class="img nj_"]/@src').extract())
        cover_url = "http:" + cover_url

        vid_im = hashlib.md5(cover_url.encode(encoding='UTF-8')).hexdigest()
        host_path = 'D:/audio'
        timeArray = time.localtime(int(time.time()))
        dt = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        createtimes = dt.split(' ')[0].replace('-', '')
        path_im = host_path + '/%s/%s.jpg' % (createtimes, vid_im)

        if not os.path.exists(host_path + '/%s/' % (createtimes)):
            os.makedirs(host_path + '/%s/' % (createtimes))

        urllib.request.urlretrieve(cover_url, path_im)

        ##传的图片路径
        local_img = '/audio/%s/%s.jpg' % (createtimes, vid_im)

        item = {}
        item['id'] = id_
        item['link'] = url_info
        item['title'] = title
        item['label'] = label
        item['author'] = author
        item['play_count'] = play_count

        item['times'] = times
        item['cover_url'] = cover_url
        item['datasss'] = datasss
        item['local_img'] = local_img
        item['introduction'] = introduction
        item['commentCount'] = commentCount
        item['data'] = datasss

        video_url = 'https://www.ximalaya.com/revision/play/v1/audio?id={}&ptype=1'.format(trackId)
        yield scrapy.Request(video_url, callback=self.parse_down, dont_filter=True,
                             meta={'item': item, 'catagory': catagory})

    ##下载音频
    def parse_down(self, response):
        item = response.meta['item']
        catagory = response.meta['catagory']
        down_json = json.loads(response.text)
        if down_json.get('ret') == 200:
            url_down = down_json['data']['src']
            Header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 QQBrowser/10.4.3469.400'
            }
            # res = requests.get(url_down, headers=Header, timeout=30)
            vid = hashlib.md5(url_down.encode(encoding='UTF-8')).hexdigest()
            host_path = 'D:/audio'
            timeArray = time.localtime(int(time.time()))
            dt = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            createtimes = dt.split(' ')[0].replace('-', '')
            path = host_path + '/%s/%s.m4a' % (createtimes, vid)

            if not os.path.exists(host_path + '/%s/' % (createtimes)):
                os.makedirs(host_path + '/%s/' % (createtimes))

            urllib.request.urlretrieve(url_down, path)
            local_path = '/audio/%s/%s.m4a' % (createtimes, vid)
        else:
            local_path = ''

        addtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = 0
        item['local_path'] = local_path
        item['addtime'] = addtime
        item['status'] = status
        print(1111111111111111111111111)
        datasss = item['data']

        ###需要将新的cover_url 添加到参数中去
        postbody = [{
            "imgPath": item['local_img'],
            "description": item['introduction'],
            "isDown": 1,  # 1 表示可以下载

            "audioId": item['id'] + str(int(time.time())),
            "taskId": datasss['taskId'],
            "level": int(datasss['level']),
            "ruleId": datasss['ruleId'],
            "taskType": datasss['taskType'],
            "url": item['link'],
            "filePath": item['local_path'],
            "title": item['title'],
            "source": datasss['source'],
            "column": catagory,  ## 栏目 datasss['column']
            "label": item['label'],
            "author": item['author'],
            "playCount": item['play_count'],
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
        r = requests.post(url='http://172.18.31.156:5012/microserver-businessManagement/task/api/python/insert',
                          data=json.dumps(postbody), headers={'Content-Type': 'application/json'})

        print(r.status_code)
        print(item)

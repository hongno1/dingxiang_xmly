import scrapy
from scrapy_redis.spiders import RedisSpider
import json

# from xmly.xmly.items import XmlyKeyInfo
import re
import os
import time
import urllib
import scrapy
import re
import datetime
import json
import requests
import hashlib

from redis import Redis

r_dis = Redis(host='localhost', port=6379)

class XmlyTotalKeywordSpider(RedisSpider):
    name = 'xmly_total_keyword'
    redis_key = 'xmly_keyword:urls'

    def make_requests_from_url(self, url):
        try:
            data = url
            data_url = json.loads(data)
            album_url = 'https://www.ximalaya.com' + data_url['album_url']

            return scrapy.Request(album_url,callback=self.parse,dont_filter=True, meta={'item': album_url})
        except Exception as e:
            print(e)

    ###链接的数据   https://www.ximalaya.com/toutiao/19177108/

    def parse(self, response):
        item = XmlyKeyInfo()
        url_ = response.url

        datasss = response.meta.get('item')
        item['data'] = datasss
        ##专辑链接
        item['url_zj'] = url_
        ##专辑名
        book_name = "".join(response.xpath('//h1[@class="title vA_"]/text()').extract())
        item['book_name'] = book_name

        book_id = "".join(re.findall('www.ximalaya.com/\w+/(\w+)', url_))
        item['book_id'] = book_id
        ##评分
        score = "".join(response.xpath('//span[@class="d-ib v-m vA_"]/text()').extract()).replace('分', '')
        if score == '':
            score = 0.0
        else:
            score = float(score)
        item['score'] = score
        ##label
        label = response.xpath('//div[@class="xui-tag tag QE_"]//span[@class="xui-tag-text"]//a//text()').extract()
        label = ",".join(label)
        item['label'] = label
        ##简介
        introduction = " ".join(response.xpath('//article[@class="intro ge_"]//p//text()').extract())
        item['introduction'] = introduction

        ##总播放量
        play_sum = "".join(response.xpath('//span[@class="count vA_"]/text()').extract())
        if play_sum == '':
            play_sum = 0
        elif '万' in play_sum:
            num = float(play_sum.replace('万', ''))
            play_sum = int(num * 10000)

        elif '亿' in play_sum:
            num = float(play_sum.replace('亿', ''))
            play_sum = int(num * 100000000)
        else:
            play_sum = int(play_sum)

        item['play_sum'] = play_sum

        detail_page = response.xpath('//ul[@class="pagination-page WJ_"]/li[last()-1]/a/span/text()').extract()
        if len(detail_page) >= 1:
            detail_page = detail_page[0]
        else:
            detail_page = 1

        for page in range(1, int(detail_page) + 1):
            url_track = 'https://www.ximalaya.com/revision/album/v1/getTracksList?albumId={}&pageNum={}'.format(book_id,
                                                                                                                str(
                                                                                                                    page))
            yield scrapy.Request(url_track, callback=self.parse_info, dont_filter=True, meta={'item': item})

    def parse_info(self, response):
        item = response.meta.get('item')

        data = json.loads(response.text)
        if data.get('ret') == 200:
            for track in data['data']['tracks']:
                title = track.get('title')
                trackId = track.get('trackId')
                url_d = 'https://www.ximalaya.com' + track.get('url')
                url_d = url_d.replace('m.ximalaya', 'ximalaya')
                url = track.get('url')
                id_ = url.replace('/', '')
                id_time = id_ + str(int(time.time()))
                playCount = track.get('playCount')
                tag = track.get('tag')

                item['title'] = title
                item['trackId'] = trackId
                item['id'] = id_time
                item['link'] = url_d
                ##播放数
                item['play_count'] = playCount

                url_dd = 'https://www.ximalaya.com/revision/track/trackPageInfo?trackId={}'.format(trackId)

                yield scrapy.Request(url_dd, callback=self.parse_detail, dont_filter=True,
                                     meta={'item': item, 'tag': tag, 'trackId': trackId})

        ###详情页面的解析 链接类似 https://www.ximalaya.com/youshengshu/3144814/337147690
        ###接口解析  https://www.ximalaya.com/revision/track/trackPageInfo?trackId=337147690

    def parse_detail(self, response):
        item = response.meta['item']
        tag = response.meta.get('tag')
        trackId = response.meta.get('trackId')

        ### 1.出版时间  times   2.##出版类别 catagory 3. cat_name 4. commentCount 5.fans 6. author  7.source 8.trackId 9.cover_url
        datas = json.loads(response.text)
        if datas.get('ret') == 200:
            data = datas.get('data')
            albumInfo = data.get('albumInfo')
            category = data.get('category')
            trackInfo = data.get('trackInfo')
            userInfo = data.get('userInfo')

            times_ = trackInfo['lastUpdate']
            times = datetime.datetime.strptime(times_, '%Y-%m-%d %H:%M:%S')
            ##类别分类 int类型
            catagory = category.get('categoryId')

            ##类别标题
            cat_name = category.get('categoryTitle')

            commentCount = trackInfo.get('commentCount')
            fans = userInfo.get('fansCount')
            author = userInfo.get('nickname')
            source = '喜马拉雅'
            cover_url = 'https:' + trackInfo.get('coverPath')

            item['times'] = times
            item['catagory'] = catagory
            item['cat_name'] = cat_name

            item['commentCount'] = commentCount
            item['fans'] = fans
            item['author'] = author
            item['source'] = source
            item['cover_url'] = cover_url

            ##存评论的redis的值
            # xmly_comments_list = []
            # xmly_comments = dict()
            # xmly_comments['commentCount'] = commentCount
            # xmly_comments['trackId'] = trackId
            # xmly_comments['id'] = item['id']
            # xmly_comments_list.append(xmly_comments)
            #
            # r_dis.lpush('x_comment:start_urls', json.dumps(xmly_comments_list[0]))



            ###下载封面图片
            host_path = 'D:/audio'
            timeArray = time.localtime(int(time.time()))
            dt = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            createtimes = dt.split(' ')[0].replace('-', '')
            name_xmly_img = 'xmly_image'

            if not os.path.exists(host_path + '/%s/%s/%s' % (createtimes, name_xmly_img, item['catagory'])):
                os.makedirs(host_path + '/%s/%s/%s' % (createtimes, name_xmly_img, item['catagory']))

            ##存储的路径
            link_name = "".join(re.findall("www.ximalaya.com/(.*)", item['link'])).replace('/', '_')

            path_img = host_path + '/%s/%s/%s/%s.jpg' % (createtimes, name_xmly_img, item['catagory'], link_name)
            try:
                urllib.request.urlretrieve(cover_url, path_img)
                img_path = '/audio/%s/%s/%s/%s.jpg' % (createtimes, name_xmly_img, item['catagory'], link_name)
                item['img_path'] = img_path
            except:
                item['img_path'] = ''
            ##判断此音频是否为付费音频 0为可下载的
            if tag == 0:
                video_url = 'https://www.ximalaya.com/revision/play/v1/audio?id={}&ptype=1'.format(trackId)
                yield scrapy.Request(video_url, callback=self.parse_down, dont_filter=True,
                                     meta={'item': item, 'trackId': trackId})

            else:
                addtime_temp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                addtime = datetime.datetime.strptime(addtime_temp, '%Y-%m-%d %H:%M:%S')
                item['local_path'] = ''
                item['isDown'] = 0
                item['addtime'] = addtime
                item['status'] = 0
                print(222222222222222222)
                print(item)
                datasss = item['data']
                postbody = [{
                    "imgPath": item['local_img'],
                    "description": item['introduction'],
                    "isDown": 0,

                    "audioId": item['id'] + str(int(time.time())),
                    "taskId": datasss['taskId'],
                    "level": int(datasss['level']),
                    "ruleId": datasss['ruleId'],
                    "taskType": datasss['taskType'],
                    "url": item['link'],
                    "filePath": item['local_path'],
                    "title": item['title'],
                    "source": "喜马拉雅",
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
                print(postbody)

                # 传输数据
                r = requests.post(
                    url='http://192.168.31.156:5012/microserver-businessManagement/task/api/python/insert',
                    data=json.dumps(postbody), headers={'Content-Type': 'application/json'})
                print(r.status_code)
                yield item

    def parse_down(self, response):

        item = response.meta['item']

        video_link = item['link']
        link_name = "".join(re.findall("www.ximalaya.com/(.*)", video_link)).replace('/', '_')
        ##详细音频id
        trackId = response.meta.get('trackId')
        down_json = json.loads(response.text)
        if down_json.get('ret') == 200:
            url_down = down_json['data']['src']
            ##存储路径
            # vid = hashlib.md5(url_down.encode(encoding='UTF-8')).hexdigest()
            ##指定路径
            host_path = 'D:/audio'
            timeArray = time.localtime(int(time.time()))
            dt = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            createtimes = dt.split(' ')[0].replace('-', '')
            name_xmly = 'xmly'

            if not os.path.exists(host_path + '/%s/%s/%s' % (createtimes, name_xmly, item['catagory'])):
                os.makedirs(host_path + '/%s/%s/%s' % (createtimes, name_xmly, item['catagory']))

            ##存储的路径

            path = host_path + '/%s/%s/%s/%s.m4a' % (createtimes, name_xmly, item['catagory'], link_name)
            urllib.request.urlretrieve(url_down, path)
            local_path = '/audio/%s/%s/%s/%s.m4a' % (createtimes, name_xmly, item['catagory'], link_name)
        else:
            url_down = ''

        addtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = 0
        item['local_path'] = local_path
        item['isDown'] = 0
        item['addtime'] = addtime
        item['status'] = status
        print(1111111111111111111111111)
        datasss = item['data']
        postbody = [{
            "imgPath": item['local_img'],  ##图片路径
            "description": item['introduction'],  ##摘要
            "isDown": 1,

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

        r_dis.lpush('xmly_comment:start_urls', json.dumps(postbody[0]))
        print(postbody)
        # r = requests.post(url='http://172.18.155.31:5012/microserver-businessManagement/task/api/python/insert',data=json.dumps(postbody), headers={'Content-Type': 'application/json'})
        r = requests.post(url='http://192.168.31.156:5012/microserver-businessManagement/task/api/python/insert',
                          data=json.dumps(postbody), headers={'Content-Type': 'application/json'})

        print(r.status_code)
        yield item


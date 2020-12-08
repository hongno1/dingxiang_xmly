import scrapy
from scrapy_redis.spiders import RedisSpider
import re
import json
from ..items import XmlyComments
import requests
import datetime
import time

class XmlyCommentSpider(RedisSpider):
    name = 'xmly_comment'
    # allowed_domains = ['ximalaya.com']
    # start_urls = ['http://ximalaya.com/']
    redis_key = 'xmly_comment:start_urls'

    def make_requests_from_url(self, url):
        url_ = json.loads(url)
        audioId = url_.get('audioId')

        level = url_.get('level')
        ###url格式  https://www.ximalaya.com/youshengshu/240506/2015326
        curl = url_.get('url')

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
        }

        meta = {
            'audioId': audioId,
            'curl': curl,
            'level': level
        }

        return scrapy.Request(curl, headers=headers, callback=self.parse, dont_filter=True,meta=meta)


    def parse(self, response):
        ##详情页的url进行正则
        trackId = "".join(re.findall('www.ximalaya.com/\w+/\w+/(\w+)', response.url))
        next_page = response.xpath('//nav[@class="pagination WJ_"]/ul/li[last()-1]/a/span/text()').extract()
        if len(next_page) == 0:
            next_page = 1
        else:
            next_page = int(next_page[0])
        for page in range(1, next_page + 1):
            url_comment = 'https://www.ximalaya.com/revision/comment/queryComments?trackId={}&page={}&pageSize=20'.format(
                trackId, page)

            yield scrapy.Request(url_comment, callback=self.parse_content, dont_filter=True, meta=response.meta)


    def parse_content(self,response):
        audioId = response.meta['audioId']
        level = response.meta['level']
        data = json.loads(response.text)
        if data.get('ret') == 200:
            comments = data.get('data').get('comments')
            for comment in comments:
                item = XmlyComments()
                topic_id = comment.get('id')
                commentTime = comment.get('commentTime')
                # commentTime_ = commentTime[:-3]
                # time_local = time.localtime(int(commentTime_))
                # comment_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

                likeCount = comment.get('likes')
                neturl = comment.get('link')
                nickname = comment.get('nickname')
                replycount = comment.get('replyCount')
                userid = comment.get('uid')
                content = comment.get('content')
                add_time_temp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                add_time = datetime.datetime.strptime(add_time_temp, '%Y-%m-%d %H:%M:%S')
                status = 0
                source = '喜马拉雅'

                item['topic_id'] = topic_id
                item['commentTime'] = commentTime
                item['likeCount'] = likeCount
                item['neturl'] = neturl
                item['nickname'] = nickname
                item['replycount'] = replycount
                item['userid'] = userid
                item['content'] = content
                item['addtime'] = add_time
                item['status'] = status
                item['source'] = source

                postbody_comment = [{
                    "audioId": audioId,
                    "level": level,
                    "commentTime": item['commentTime'],
                    "userName": item['nickname'],
                    "content": item['content'],
                    "source": item['source'],
                }]
                print(postbody_comment)
                r = requests.post(url='http://192.168.31.156:5012/microserver-businessManagement/task/api/python/comment/insert',
                                  data=json.dumps(postbody_comment), headers={'Content-Type': 'application/json'})
                print(r.status_code)
                # exit()
                yield item
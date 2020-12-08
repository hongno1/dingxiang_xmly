# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
class XmlyPipeline(object):
    def process_item(self, item, spider):
        return item

class XmlyMongoPipeline(object):
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_url=crawler.settings.get('MONGO_URL'),
                   mongo_db=crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        if item.collection == 'xmlyvideo':
            self.db[item.collection].insert(dict(item))

        elif item.collection == 'xmlyinfo':
            # self.db[item.collection].insert(dict(item))
            self.db[item.collection].update(
                {'id':item.get('id')},
                {'$set':
                     {
                         'label':item['label'],
                         'book_id': item['book_id'],
                         'book_name': item['book_name'],
                         'introduction': item['introduction'],
                         'link': item['link'],
                         'score': item['score'],
                         'play_count': item['play_count'],
                         'play_sum': item['play_sum'],
                         'times': item['times'],
                         'title': item['title'],
                         'catagory': item['catagory'],
                         'local_path': item['local_path'],
                         'isDown': item['isDown'],
                         'addtime': item['addtime'],
                         'status': item['status'],
                         'commentCount': item['commentCount'],
                         'author' : item['author'],
                         'local_img': item['local_img']
                     }},True)

        ##新增加的专项的关键词的存入
        elif item.collection == 'xmlykeyinfo':
            self.db[item.collection].insert(dict(item))

        elif item.collection == 'xmlyinfo_dj':
            self.db[item.collection].update(
                {'id': item.get('id')},
                {'$set':
                    {
                        'link': item['link'],
                        'title': item['title'],
                        'label': item['label'],
                        'author': item['author'],
                        'play_count': item['play_count'],
                        'times': item['times'],
                        'cover_url': item['cover_url'],
                        'local_img': item['local_img'],
                        'local_path': item['local_path'],
                        'introduction': item['introduction'],
                        'addtime': item['addtime'],
                        'status': item['status'],
                        'commentCount': item['commentCount']
                    }}, True)

        elif item.collection == 'xmlycate':
            self.db[item.collection].update({'cate_url':item.get('cate_url')},{'$set':{'cate_url':item['cate_url']}},True)

        elif item.collection == 'xmlybook':
            self.db[item.collection].update({'book_url': item.get('book_url')},
                                            {'$set': {'book_url': item['book_url'],'status':item['status']}}, True)

        elif item.collection == 'xmlyupdate':
            self.db[item.collection].update({'update_url':item.get('update_url')},{'$set':{'update_url':item['update_url']}},True)

        elif item.collection == 'xmly_comments':
            self.db[item.collection].update({'topic_id':item.get('topic_id')},{
                '$set':{
                    'commentTime':item['commentTime'],
                    'likeCount': item['likeCount'],
                    'neturl': item['neturl'],
                    'nickname': item['nickname'],
                    'replycount': item['replycount'],
                    'userid': item['userid'],
                    'content': item['content'],
                    'addtime': item['addtime'],
                    'status': item['status'],
                    'source': item['source']
                }
            },True)

        # elif item.collection == 'xmlytotal':
        #     # self.db[item.collection].insert(dict(item))
        #     self.db[item.collection].update(
        #         {'id':item.get('id')},
        #         {'$set':
        #              {
        #                  'label':item['label'],
        #                  'book_id': item['book_id'],
        #                  'book_name': item['book_name'],
        #                  'introduction': item['introduction'],
        #                  'link': item['link'],
        #                  'score': item['score'],
        #                  'play_count': item['play_count'],
        #                  'play_sum': item['play_sum'],
        #                  'times': item['times'],
        #                  'title': item['title'],
        #                  'catagory': item['catagory'],
        #                  'local_path': item['local_path'],
        #                  'isDown': item['isDown'],
        #                  'addtime': item['addtime'],
        #                  'status': item['status']
        #              }},True)
        return item

    def close_spider(self, spider):
        self.client.close()



import time
from elasticsearch7 import Elasticsearch
# 写入到es中,需要在settings中启用这个类 ExchangeratespiderESPipeline
# 需要安装pip install elasticsearch-dsl==5.1.0 注意与es版本需要对应
class SinafinancespiderESPipeline(object):

    def __init__(self):
        # self.ES = ["http://elastic:0p-0p-0p-@172.18.155.50:9200"]

        self.ES = ["192.168.31.146:9202"]
        # 创建es客户端
        self.es = Elasticsearch(
          self.ES,
          # 启动前嗅探es集群服务器
          sniff_on_start=True,
          # es集群服务器结点连接异常时是否刷新es结点信息
          sniff_on_connection_fail=True,
          # 每60秒刷新节点信息
          sniffer_timeout=80
        )

    def process_item(self, item, spider):
        if item.collection == 'xmlyinfo':
            spider.logger.info("-----enter into insert ESXmlyInfo")
            doc = {
                "from_url": item["link"],
                "title": item["title"],
                "play_count": item["play_count"],
                "audio_time": item["duration"],

                "comment_count": item["commentCount"],
                "analyze_summary": item["introduction"],
                "author": item["author"],
                "add_time": item["addtime"],
                "create_time": item["addtime"],
                "release_time": item['times'],
                "id": item["id"]+str(int(time.time())),
                # "column": item['cat_name'],
                "source": "喜马拉雅",
                # "cover_url": item['cover_url'],
                "img_path": item['img_path'],
                "file_path": item['local_path'],
                "url_zj": item['url_zj'],
                "book_name": item['book_name'],
                "catagory": item['catagory'],
                "times": item['times'],
                # "trackId": item['trackId']
            }

        ##新增加的xmlykeyinfo的写入
        elif item.collection == 'xmlykeyinfo':
            spider.logger.info("-----enter into insert ESXmlyInfo")
            doc = {
                "from_url": item["link"],
                "title": item["title"],
                "play_count": item["play_count"],
                "comment_count": item["commentCount"],
                "analyze_summary": item["introduction"],
                "author": item["author"],
                "add_time": item["addtime"],
                "create_time": item["addtime"],
                "release_time": item['times'],
                "id": item["id"] + str(int(time.time())),
                "column": item['cat_name'],
                "source": "喜马拉雅",
                "cover_url": item['cover_url'],
                "img_path": item['img_path'],
                "file_path": item['local_path'],
                "url_zj": item['url_zj'],
                "book_name": item['book_name'],
                "catagory": item['catagory'],
                "times": item['times'],
                # "trackId": item['trackId']
            }

        # self.es.index(index="bus_analysis_result", doc_type="sinafinance", body=doc, id=item["id"])
        self.es.index(index="bus_analysis_result",  body=doc, id=item["id"]+str(int(time.time())))
        return item
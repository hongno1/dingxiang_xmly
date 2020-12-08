from redis import Redis
import re
import pymongo
import time


class Redis_cate():
    def __init__(self):
        self.redis = Redis(host='localhost',port=6379)
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client['xmly']

    def add_url(self):
        collection = self.db['xmlycate']
        urls = collection.find({})
        for url in urls:
            url = url['cate_url']
            self.redis.lpush('xmly_cate:start_urls',url)


if __name__ == '__main__':
    rc = Redis_cate()
    rc.add_url()
    print('catch...')
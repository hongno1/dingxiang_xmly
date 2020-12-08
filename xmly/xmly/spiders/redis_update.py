### 增量爬虫的url存入到redis中
from redis import Redis
import re
import pymongo
import time


class Redis_update():
    def __init__(self):
        self.redis = Redis(host='localhost',port=6379)
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client['xmly']

    def add_url(self):
        collection = self.db['xmlyupdate']
        urls = collection.find({})
        for url in urls:
            url = url['update_url']
            self.redis.lpush('xmly_update:start_urls',url)

if __name__ == '__main__':
    ru = Redis_update()
    ru.add_url()
    print('update...')
from redis import Redis
import time
import pymongo

class Redis_book():
    def __init__(self):
        self.redis = Redis(host='localhost', port=6379)
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client['xmly']

    def add_url(self):
        collection = self.db['xmlybook']
        urls = collection.find({})
        for url in urls:
            url = url['book_url']
            self.redis.lpush('xmly_book::start_urls',url)


if __name__ == '__main__':
    book = Redis_book()
    book.add_url()
    print('book add...')
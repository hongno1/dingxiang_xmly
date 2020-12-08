# -*- coding: utf-8 -*-

# Scrapy settings for xmly project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'xmly'

SPIDER_MODULES = ['xmly.spiders']
NEWSPIDER_MODULE = 'xmly.spiders'

# MONGO_URL = 'mongodb://admin:admin@172.18.155.12:27018/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=false'
# MONGO_DB = 'admin'

MONGO_URL = 'localhost'
MONGO_DB = 'admin'

# REDIS_URL='redis://root:admin@NBwhy0504@10.0.1.43:6338'
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379


SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'xmly (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False
DOWNLOAD_TIMEOUT = 20
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

##自动限速
AUTOTHROTTLE_ENABLED = True

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,apsplication/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#   'cookie': '_xmLog=xm_kf3ds0sxodpwbd; s&e=7f7893fe5b686e7c888edaca4e28b6da; x_xmly_traffic=utm_source%253A%2526utm_medium%253A%2526utm_campaign%253A%2526utm_content%253A%2526utm_term%253A%2526utm_from%253A; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1600139563,1600246326,1600307617; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1600310910; s&a=A%01T[WT%11%06O%0DU[T%06@%04BSW%06%0A%02%1C%02N%0EY[%08Y%1F%02V_CRBWMOKQ_SBTAS',
#   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
#   # 'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'xmly.middlewares.XmlySpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html

DOWNLOADER_MIDDLEWARES = {
   # 'xmly.middlewares.XmlyDownloaderMiddleware': 543,
    'xmly.middlewares.RandomUserAgentMiddlware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None
}


# RANDOMIZE_DOWNLOAD_DELAY=True

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'scrapy.pipelines.files.FilesPipeline': 1,
   # 'xmly.pipelines.XmlyPipeline': 300,
   # 'xmly.pipelines.XmlyMongoPipeline':301,
   'xmly.pipelines.SinafinancespiderESPipeline': 302,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

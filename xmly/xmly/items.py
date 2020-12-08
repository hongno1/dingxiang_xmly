# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XmlyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    collection = 'xmlyvideo'
    image = scrapy.Field()
    name = scrapy.Field()
    href = scrapy.Field()
    count = scrapy.Field()
    company = scrapy.Field()
    company_href = scrapy.Field()

    ###detail中的内容
    detail_id = scrapy.Field()
    track_id = scrapy.Field()
    detail_title = scrapy.Field()
    detail_count = scrapy.Field()
    detail_href = scrapy.Field()
    detail_year = scrapy.Field()

class XmlyInfo(scrapy.Item):
    ##定向的存储表
    collection = 'xmlyinfo'
    id = scrapy.Field()  ##音频标识id  string
    label = scrapy.Field()  ##音频标签 string
    book_id = scrapy.Field()  ##专辑id  Int
    book_name = scrapy.Field()  ##音频专辑id名称 string
    introduction = scrapy.Field()  ##音频专辑简介 string
    link = scrapy.Field()  ##音频原网页链接 string
    score = scrapy.Field()  ##音频分数 float
    play_count = scrapy.Field()  ##音频播放量  int
    play_sum = scrapy.Field()  ##音频专辑总播放量  int
    times = scrapy.Field()  ##音频发布时间  datetime
    title = scrapy.Field()  ##音频标题  string
    catagory = scrapy.Field()  ##音频类别  string
    local_path = scrapy.Field() ##音频本地存储地址  string
    isDown = scrapy.Field()  ##音频是否下载 0表示下载  1表示未下载
    addtime = scrapy.Field()  ##数据入库时间  datetime
    status = scrapy.Field()  ##入ES库的状态（0表示未入  1表示正在入 2表示已入）
    data = scrapy.Field()
    author = scrapy.Field()

    cover_url = scrapy.Field()
    commentCount = scrapy.Field()  ##评论数
    local_img = scrapy.Field()  ##图片地址
    duration = scrapy.Field()  #时长


###新增加的专向的关键词爬取
class XmlyKeyInfo(scrapy.Item):
    collection = 'xmlykeyinfo'
    id = scrapy.Field()  ##音频标识id  string
    label = scrapy.Field()  ##音频标签 string
    book_id = scrapy.Field()  ##专辑id  Int
    book_name = scrapy.Field()  ##音频专辑id名称 string
    introduction = scrapy.Field()  ##音频专辑简介 string
    link = scrapy.Field()  ##音频原网页链接 string
    score = scrapy.Field()  ##音频分数 float
    play_count = scrapy.Field()  ##音频播放量  int
    play_sum = scrapy.Field()  ##音频专辑总播放量  int
    times = scrapy.Field()  ##音频发布时间  datetime
    title = scrapy.Field()  ##音频标题  string
    catagory = scrapy.Field()  ##音频类别
    commentCount = scrapy.Field()  ##音频的评论数
    fans = scrapy.Field()  ##粉丝数
    local_path = scrapy.Field()  ##音频本地存储地址  string
    isDown = scrapy.Field()  ##音频是否下载 0表示下载  1表示未下载
    addtime = scrapy.Field()  ##数据入库时间  datetime
    status = scrapy.Field()  ##入ES库的状态（0表示未入  1表示正在入 2表示已入）
    cat_name = scrapy.Field()
    author = scrapy.Field()
    source = scrapy.Field()
    trackId = scrapy.Field()  ##音频id
    cover_url = scrapy.Field()  ##封面链接
    img_path = scrapy.Field()
    url_zj = scrapy.Field()  ###专辑的链接

    data = scrapy.Field()  ##传的参数


class XmlyDanji(scrapy.Item):
    ##单集存储表
    collection = 'xmlyinfo_dj'
    id = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()
    label = scrapy.Field()
    author = scrapy.Field()
    play_count = scrapy.Field()
    times = scrapy.Field()
    cover_url = scrapy.Field()
    local_img = scrapy.Field()
    local_path = scrapy.Field()
    introduction = scrapy.Field()
    addtime = scrapy.Field()
    status = scrapy.Field()
    commentCount = scrapy.Field()


##音频评论表
class XmlyComments(scrapy.Item):
    collection = 'xmly_comments'
    topic_id = scrapy.Field()
    commentTime = scrapy.Field()
    likeCount = scrapy.Field()
    neturl = scrapy.Field()
    nickname = scrapy.Field()
    replycount = scrapy.Field()
    userid = scrapy.Field()
    content = scrapy.Field()
    addtime = scrapy.Field()
    status = scrapy.Field()

    source = scrapy.Field()


    # title = scrapy.Field()
    # userid = scrapy.Field()
    # times = scrapy.Field()
    # link = scrapy.Field()
    # read_count = scrapy.Field()
    # book_name = scrapy.Field()
    # biaoqian = scrapy.Field()
    # pingfen = scrapy.Field()
    # shuji_count = scrapy.Field()
    # jianjie = scrapy.Field()

class XmlyCate(scrapy.Item):
    collection = 'xmlycate'
    cate_url = scrapy.Field()


class XmlyBook(scrapy.Item):
    collection = 'xmlybook'
    book_url = scrapy.Field()
    status = scrapy.Field()


class XmlyUpdate(scrapy.Item):
    collection = 'xmlyupdate'
    update_url = scrapy.Field()

# class XmlyTotal(scrapy.Item):
#     collection = 'xmlytotal'
#     id = scrapy.Field()  ##音频标识id  string
#     label = scrapy.Field()  ##音频标签 string
#     book_id = scrapy.Field()  ##专辑id  Int
#     book_name = scrapy.Field()  ##音频专辑id名称 string
#     introduction = scrapy.Field()  ##音频专辑简介 string
#     link = scrapy.Field()  ##音频原网页链接 string
#     score = scrapy.Field()  ##音频分数 float
#     play_count = scrapy.Field()  ##音频播放量  int
#     play_sum = scrapy.Field()  ##音频专辑总播放量  int
#     times = scrapy.Field()  ##音频发布时间  datetime
#     title = scrapy.Field()  ##音频标题  string
#     catagory = scrapy.Field()  ##音频类别  string
#     local_path = scrapy.Field() ##音频本地存储地址  string
#     isDown = scrapy.Field()  ##音频是否下载 0表示下载  1表示未下载
#     addtime = scrapy.Field()  ##数据入库时间  datetime
#     status = scrapy.Field()  ##入ES库的状态（0表示未入  1表示正在入 2表示已入）

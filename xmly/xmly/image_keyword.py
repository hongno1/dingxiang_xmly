# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import datetime
from flask import Flask, request, jsonify
from selenium import webdriver
import hashlib
import time
from scrapy.utils.python import to_bytes
from flask_cors import CORS
import json
import redis

app = Flask(__name__)
CORS(app, resources=r'/*')
CORS(app, supports_credentials=True)
# app.debug = True
# con = pymysql.connect(host ='10.0.1.35',user='root',password='159Super753Jian',db="crawl",port=6033,charset='utf8')
# con.autocommit(True)

# @app.route('/add/img/', methods=['get'])
# def add_content():
#     start = datetime.datetime.now()
#     if not request.args:  # 检测是否有数据
#         return ('fail')
#     img_url = request.args.get("link")
#     print(img_url)
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#     driver.get(img_url)
#     uu = hashlib.sha1(to_bytes(img_url)).hexdigest()
#     timeArray = time.localtime(int(time.time()))
#     dt = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
#     createtimes = dt.split(' ')[0]
#     # print createtimes
#     driver.get_screenshot_as_file(r"E:\img\full2\%s\%s.png" % (createtimes,uu))
#     path_img = "http://lsgcloud.com/full2/%s/%s.png" % (createtimes,uu)
#     #入库
#
#     driver.quit()
#     # driver.close()
#     return path_img
#     # 返回JSON数据。

@app.route('/add/xmlykeyword/', methods=['post'])
def add_xmlykeyword():
    start = datetime.datetime.now()
    if not request.data:  # 检测是否有数据
        return ('fail')
    appData = request.data
    app_json = json.loads(appData)
    # print (app_json)
    print(app_json["title"])
    print(app_json["source"])
    print(app_json["taskId"])
    print(app_json["taskType"])
    print(app_json["type"])
    print(app_json["url"])
    print(app_json["level"])
    print(app_json["ruleId"])
    print(app_json["range"])

    print(app_json["keyword"])
    # executor.submit(do_add_content, appData)
    # gevent.spawn(do_add_content(appData))
    end = datetime.datetime.now()
    # print 'content' + '|' + '{cost}'.format(cost=end - start)
    # 连接池
    # pool = redis.ConnectionPool(host="10.0.1.43", port=6338, password="admin@NBwhy0504", max_connections=1024)
    # conn = redis.Redis(connection_pool=pool)
    # conn.set("xmly:taskrw",app_json)
    r = redis.Redis(host='localhost', port=6379)
    r.lpush("xmly:taskkeyword", appData)
    return 'success'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=False)


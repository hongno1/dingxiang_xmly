# !/usr/bin/env python3
# -*- coding:utf-8 -*-

import datetime
from flask import Flask, request, jsonify
import json
app = Flask(__name__)
app.debug =False
@app.route('/add/xmly/', methods=['post'])
def add_xmly():
    start = datetime.datetime.now()
    if not request.data:  # 检测是否有数据
        return ('fail')
    appData = request.data
    app_json = json.loads(appData)
    print (app_json)
    print (app_json["title"])
    print (app_json["source"])
    print (app_json["column"])
    print (app_json["taskId"])
    print (app_json["taskType"])
    print (app_json["type"])
    print(app_json["url"])
    print(app_json["level"])
    print(app_json["ruleId"])
    print(app_json["range"])
    end = datetime.datetime.now()
    return 'success'
if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0',port=5008)

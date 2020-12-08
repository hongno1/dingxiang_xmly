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

r = redis.Redis(host='10.0.1.43', port=6338, password='admin@NBwhy0504')
r.lpush("xmly_book::start_urls'",'https://www.ximalaya.com/gerenchengzhang/24785128/')
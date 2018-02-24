# -*- coding: utf-8 -*-
"""
Created on 2018年2月9日
@author: Leo
"""
# 第三方库
import pymongo
from scrapy.conf import settings

# 项目内置库
from LaGou_Scrapy.logger.LoggerHandler import Logger

# 日志中心
logger = Logger(logger='pipelines.py').get_logger()


class LagouScrapyPipeline(object):
    def __init__(self):
        # Host地址
        self._host = settings["MONGODB_HOST"]
        # 端口号
        self._port = settings["MONGODB_PORT"]
        # 数据库名字
        self._db_name = settings["MONGODB_DB_NAME"]
        # 集合名
        self._collection_name = settings["MONGODB_COLLECTION"]
        # 数据库连接
        self.client = pymongo.MongoClient(host=self._host, port=self._port)
        # 判断是否有用户名密码(用户名和密码都不为空的情况下)
        if settings['MONGODB_USER'] != "" and settings['MONGODB_PASS'] != "":
            self.client.admin.authenticate(settings['MONGODB_USER'], settings['MONGODB_PASS'])
        # 指定数据库
        self._db = self.client[self._db_name]
        # 指定集合名
        self.collection = self._db[self._collection_name]

    def process_item(self, item, spider):
        if spider.name == "LaGou":
            try:
                self.collection.insert(item)
                return item
            except Exception as err:
                logger.error(err)

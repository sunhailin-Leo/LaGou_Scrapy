# -*- coding: UTF-8 -*-
"""
Created on 2018年2月9日
@author: Leo
"""
# Python内置库
import re
import time
import hashlib


def filter_html_tag(content: str) -> str:
    """
    过滤文字中的HTML标签
    :param content:
    :return:
    """
    pattern = re.compile(r'<[^>]+>', re.S)
    return pattern.sub('', content)


def get_value(data) -> str:
    """
    :param data: 数据
    :return: 拆分列表后的数据
    """
    data = [d.replace("\xa0", "") for d in data]
    info = ''.join(data)
    return info


def time_to_timestamp(time_str: str, time_format_model='%Y-%m-%d %H:%M:%S'):
    """
    年月日时分秒转时间戳
    :param time_str: 年月日时分秒
    :param time_format_model: 时间格式模版
    :return: 时间戳
    """
    return time.mktime(time.strptime(time_str, time_format_model)) * 1000


def string_to_md5(string: str):
    """
    字符串转MD5串
    :param string: 字符串
    :return: MD5串
    """
    return hashlib.md5(string.encode("utf-8")).hexdigest()

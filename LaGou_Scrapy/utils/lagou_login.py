# -*- coding:utf-8 -*-
"""
Created on 2018年2月9日
@author: Leo
"""
import re
import requests

# 项目内部库
from LaGou_Scrapy.utils.util import *
from LaGou_Scrapy.logger.LoggerHandler import Logger

# 日志中心
logger = Logger(logger='lagou_login.py').get_logger()


# 请求对象
session = requests.session()

# 请求头信息
HEADERS = {
    'Referer': 'https://passport.lagou.com/login/login.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0',
}


def _get_password(pass_wd: str) -> str:
    """
    这里对密码进行了md5双重加密 veennike 这个值是在main.html_aio_f95e644.js文件找到的
    """
    pass_wd = string_to_md5(string=pass_wd)
    pass_wd = 'veenike' + pass_wd + 'veenike'
    pass_wd = string_to_md5(string=pass_wd)
    return pass_wd


def _get_token() -> tuple:
    forge_token = ""
    forge_code = ""
    login_page = 'https://passport.lagou.com/login/login.html'
    data = session.get(login_page, headers=HEADERS)
    match_obj = re.match(r'.*X_Anti_Forge_Token = \'(.*?)\';.*X_Anti_Forge_Code = \'(\d+?)\'', data.text, re.DOTALL)
    if match_obj:
        forge_token = match_obj.group(1)
        forge_code = match_obj.group(2)
    return forge_token, forge_code


def login(user: str, pass_wd: str):
    x__anti__forge__token, x__anti__forge__code = _get_token()
    login_headers = HEADERS.copy()
    login_headers.update(
        {
            'X-Requested-With': 'XMLHttpRequest',
            'X-Anit-Forge-Token': x__anti__forge__token,
            'X-Anit-Forge-Code': x__anti__forge__code
        }
    )

    post_data = {
        'isValidate': 'true',
        'username': user,
        'password': _get_password(pass_wd),
        'request_form_verifyCode': '',
        'submit': '',
    }
    response = session.post('https://passport.lagou.com/login/login.json', data=post_data, headers=login_headers)
    logger.info(response.text)


def get_cookies():
    return requests.utils.dict_from_cookiejar(session.cookies)

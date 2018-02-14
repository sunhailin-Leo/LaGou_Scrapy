# -*- coding: UTF-8 -*-
"""
Created on 2018年2月8日
@author: Leo
@file: lagou_spider.py
"""

# Python内置库
import json
from collections import OrderedDict

# 第三方库
import scrapy
from scrapy.conf import settings
from scrapy.exceptions import CloseSpider

# 项目内部库
from LaGou_Scrapy.utils.lagou_login import *
from LaGou_Scrapy.utils.util import *
from LaGou_Scrapy.logger.LoggerHandler import Logger
from LaGou_Scrapy.utils.cookies import *
from LaGou_Scrapy.items import LagouScrapyItem

# 日志中心
logger = Logger(logger='lagou_spider.py').get_logger()


class Lagou(scrapy.Spider):

    name = "LaGou"

    def __init__(self, search_name, *args):
        # 拉勾网登录账号密码
        self._username = settings['USERNAME']
        self._password = settings['PASSWORD']

        # login_cookies
        self.login_cookies = None

        # 爬取字段 set到REFERER_NAME中
        self._search_name = search_name
        settings.set("REFERER_NAME", self._search_name)

        # 页数设个起始值
        self.page_no = settings["START_PAGE_NUM"]

        # 请求json的url
        self._url = 'https://www.lagou.com/jobs/positionAjax.json?px=new&kd={}&pn={}&'

        super().__init__(*args)

    def start_requests(self):
        # 登陆
        login(user=self._username, pass_wd=self._password)
        self.login_cookies = get_cookies()
        logger.info(self.login_cookies)

        url = self._url.format(self._search_name, self.page_no)
        yield scrapy.Request(url=url,
                             method="GET",
                             callback=self.parse)

    def parse(self, response):
        json_data = response.text
        logger.debug(json_data)
        if '<html>' not in json_data:
            data = json.loads(json_data, object_pairs_hook=OrderedDict)
            # logger.debug(data)
            if data['success'] is True:
                # Json里面的页码
                self.page_no = data['content']['pageNo']
                while self.page_no != 0:
                    # 解析
                    result = data['content']['positionResult']['result']
                    for item in result:
                        lagou_data = LagouScrapyItem()
                        # try:
                        # MongoDB ID
                        lagou_data['_id'] = string_to_md5(string=str(
                            item['companyId']) + str(item['positionId']))
                        lagou_data['from_website'] = "拉勾"
                        # 薪资(最低最高)
                        try:
                            salary = item.get('salary').split('-')
                            lagou_data['min_salary'] = salary[0]
                            lagou_data['max_salary'] = salary[1]
                        except IndexError:
                            salary = item.get('salary').replace('以上')
                            lagou_data['min_salary'] = salary
                            lagou_data['max_salary'] = "不限"
                        # 工作地址
                        try:
                            lagou_data['location'] = item['city'] + \
                                item['district']
                        except TypeError:
                            lagou_data['location'] = item['city']
                        # 发布时间
                        lagou_data['publish_date'] = int(
                            time_to_timestamp(time_str=item['createTime']))
                        # 职位类型
                        lagou_data['work_type'] = item['jobNature']
                        # 工作年限
                        lagou_data['work_experience'] = item['workYear']
                        # 教育水平
                        lagou_data['limit_degree'] = item['education']
                        # 招聘人数
                        lagou_data['people_count'] = 0
                        # 职位名称
                        lagou_data['work_name'] = item['positionName']
                        # 工作职责
                        lagou_data['work_duty'] = ""
                        # 工作需求
                        lagou_data['work_need'] = ""
                        # 公司名称
                        lagou_data['business_name'] = item['companyFullName']
                        # 公司状态
                        lagou_data['business_type'] = item['financeStage']
                        # 公司人数规模
                        lagou_data['business_count'] = item['companySize']
                        # 公司行业类别
                        lagou_data['business_industry'] = item['industryField']
                        # 公司页面url
                        company_url = 'https://www.lagou.com/gongsi/%s.html' % item['companyId']
                        # 招聘信息页面url
                        job_url = 'https://www.lagou.com/jobs/%s.html' % item['positionId']

                        # 职位页面
                        lagou_data['work_info_url'] = job_url

                        yield scrapy.Request(url=job_url,
                                             method="GET",
                                             cookies=ALL_COOKIES,
                                             callback=self.parse_job_info,
                                             meta={"lagou_data": lagou_data,
                                                   "company_url": company_url},
                                             dont_filter=False)
                        # except TypeError as err:
                        #     logger.error(err)
                        # 翻页
                        url = self._url.format(self._search_name, self.page_no + 1)
                        yield scrapy.Request(url=url,
                                             method="GET",
                                             callback=self.parse)
                else:
                    raise CloseSpider(reason="End of Page num!")

    def parse_job_info(self, response):
        """
        解析职位信息
        :param response:
        :return:
        """
        # Item
        lagou_data = response.meta['lagou_data']
        # 企业URL
        company_url = response.meta['company_url']
        # 招聘信息
        info = response.xpath("//dd[@class='job_bt']//p/text()").extract()
        if len(info) != 0:
            lagou_data['work_content'] = get_value(info)
        else:
            info = response.xpath(
                "//dd[@class='job_bt']//p/span/text()").extract()
            lagou_data['work_content'] = get_value(info)

        yield scrapy.Request(url=company_url,
                             method="GET",
                             cookies=COMPANY_COOKIES,
                             callback=self.parse_company_info,
                             meta={"lagou_data": lagou_data},
                             dont_filter=True)

    @staticmethod
    def parse_company_info(response):
        """
        解析企业信息
        :param response:
        :return:
        """
        # Item
        lagou_data = response.meta['lagou_data']
        # 获取页面上的json, 并解析
        business_json = json.loads(response.xpath(
            'string(//*[@id="companyInfoData"])').extract()[0])

        # 公司地址(判断)
        try:
            address_list = business_json['addressList'][0]
            business_location = \
                address_list['province'] + address_list['city'] + address_list['district']
        except KeyError:
            try:
                address_list = business_json['addressList'][1]
                business_location = \
                    address_list['province'] + address_list['city'] + address_list['district']
            except (IndexError, KeyError):
                business_location = ""
        # 公司地址
        lagou_data['business_location'] = business_location

        # 公司网站主页
        lagou_data['business_website'] = business_json['coreInfo']['companyUrl']

        # 公司介绍
        try:
            business_info = business_json['introduction']['companyProfile']
            business_info = filter_html_tag(
                content=business_info).replace(
                "\n",
                "").replace(
                "&nbsp;",
                "")
        except KeyError:
            business_info = ""

        # 公司介绍信息
        lagou_data['business_info'] = business_info

        yield lagou_data

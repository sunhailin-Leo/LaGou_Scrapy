# -*- coding: utf-8 -*-
"""
Created on 2018年2月9日
@author: Leo
"""

import scrapy


class LagouScrapyItem(scrapy.Item):
    _id = scrapy.Field()
    from_website = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    location = scrapy.Field()
    publish_date = scrapy.Field()
    work_type = scrapy.Field()
    work_experience = scrapy.Field()
    limit_degree = scrapy.Field()
    people_count = scrapy.Field()
    work_name = scrapy.Field()
    work_duty = scrapy.Field()
    work_need = scrapy.Field()
    work_content = scrapy.Field()
    work_info_url = scrapy.Field()
    business_name = scrapy.Field()
    business_type = scrapy.Field()
    business_count = scrapy.Field()
    business_website = scrapy.Field()
    business_industry = scrapy.Field()
    business_location = scrapy.Field()
    business_info = scrapy.Field()

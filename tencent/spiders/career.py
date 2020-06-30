# -*- coding: utf-8 -*-
import json
import scrapy
from tencent.items import Offer

class CareerSpider(scrapy.Spider):
    name = 'career'
    allowed_domains = ['career.tencent.com']
    start_urls = ['https://careers.tencent.com/tencentcareer/api/post/Query?countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex=1&pageSize=10&language=zh-cn&area=cn']
    detail_url = "https://careers.tencent.com/tencentcareer/api/post/ByPostId?postId={}&language=zh-cn"
    
    def parse(self, response):
        for post in json.loads(response.text)['Data']['Posts']:
            item = Offer()
            item['url'] = self.detail_url.format(post['PostId'])
            item['category'] = post['CategoryName']
            
            yield scrapy.Request(item['url'], meta={'item': item}, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        item = response.meta['item']
        resp = json.loads(response.text)
        item['name'] = resp['Data']['RecruitPostName']
        item['responsibility'] = resp['Data']['Responsibility']
        yield item

# -*- coding: utf-8 -*-
import scrapy
from netbian.items import NetbianItem

class NetbianCrawlerSpider(scrapy.Spider):
    name = "netbian_crawler"
    allowed_domains = ["netbian.com"]
    start_urls = (
        'http://www.netbian.com/',
    )

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)


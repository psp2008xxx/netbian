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
        # for link in response.xpath('//*[@id="header"]/div[1]/ul/li'):
        #     self.logger.info('link attribute is %s', link.xpath('div/a[1]/@href').extract())
        for link in response.xpath('//div[@class="nav cate"]/a'):
            self.logger.info('link attribute is %s', link.xpath('@href').extract())



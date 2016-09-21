# -*- coding: utf-8 -*-
import scrapy
from netbian.items import NetbianItem


class NetbianCrawlerSpider(scrapy.Spider):
    name = "netbian_crawler"
    allowed_domains = ["netbian.com"]
    start_urls = ['http://www.netbian.com/']
    base_url = 'http://www.netbian.com'

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        for sub_link in response.xpath('//li[@class="more"]/div'):
            for link in sub_link.xpath('a'):
                item = NetbianItem()
                item['title_name'] = link.xpath('@title').extract() or link.xpath('text()').extract()
                item['link_address'] = self._link_post_process(link.xpath('@href').extract()[0])
                yield item

    def _link_post_process(self, link):
        if link.startswith('/'):
            link = self.base_url + link
        return link
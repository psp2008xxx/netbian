# -*- coding: utf-8 -*-
import scrapy
from netbian.items import NetbianItem


# hdr = {
# 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#     'Accept-Encoding': 'none',
#     'Accept-Language': 'en-US,en;q=0.8',
#     'Connection': 'keep-alive'}


class NetbianCrawlerSpider(scrapy.Spider):
    name = "netbian"
    allowed_domains = ["netbian.com"]
    start_urls = ['http://www.netbian.com/']
    base_url = 'http://www.netbian.com'

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        for sub_link in response.xpath('//li[@class="more"]/div/a/@href').extract():
            sub_link_address = self._link_post_process(sub_link)
            yield scrapy.Request(sub_link_address, callback=self.parse_image)

    def parse_image(self, response):
        item = NetbianItem()
        item['image_urls'] = response.xpath('//*/@data-src').extract()
        yield item

        for next_link in response.xpath('//div[@class="page"]/a[not(contains(@class,"prev"))]/@href').extract():
            next_link_address = self._link_post_process(next_link)
            yield scrapy.Request(next_link_address, callback=self.parse_image)

    def _link_post_process(self, link):
        if link.startswith('/'):
            link = self.base_url + link
        return link

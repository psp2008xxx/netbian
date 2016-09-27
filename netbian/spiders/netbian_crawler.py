# -*- coding: utf-8 -*-
import scrapy
from netbian.items import NetbianItem


hdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}


class NetbianCrawlerSpider(scrapy.Spider):
    name = "netbian_crawler"
    allowed_domains = ["netbian.com"]
    start_urls = ['http://www.netbian.com/']
    base_url = 'http://www.netbian.com'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=hdr, callback=self.parse)

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        for sub_link in response.xpath('//li[@class="more"]/div'):
            for link in sub_link.xpath('a'):
                item = NetbianItem()
                # item['title_name'] = link.xpath('@title').extract() or link.xpath('text()').extract()
                item['link_address'] = self._link_post_process(link.xpath('@href').extract()[0])
                yield item

    def parse_image(self, response):
        for link in response.xpath('//a'):
            item = NetbianItem()
            item['image_urls'] = link.xpath('img/@src').re(r'.*jpg$')
            yield item

    def _link_post_process(self, link):
        if link.startswith('/'):
            link = self.base_url + link
        return link

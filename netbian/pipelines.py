# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
from scrapy import log
from scrapy.exceptions import DropItem
from scrapy import signals
from scrapy.exporters import JsonLinesItemExporter
from scrapy.pipelines.images import ImagesPipeline




class Netbian_Mysql_Pipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d

    def _do_upinsert(self, conn, item, spider):
        guid = self._get_guid(item)
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        conn.execute("""SELECT EXISTS(
            SELECT 1 FROM website WHERE guid = %s)""", (guid, ))
        ret = conn.fetchone()[0]
        if ret:
            conn.execute("""
           UPDATE website SET title_name=%s, link_address=%s, updated=%s WHERE guid=%s
            """, (item['title_name'], item['link_address'], now, guid))
            spider.log("Item updated in db: %s %r" % (guid, item))
        else:
            conn.execute("""
            INSERT INTO website (guid, title_name, link_address, updated)
                VALUES(%s, %s, %s, %s)"""
                         , (guid, item['title_name'], item['link_address'], now))
            spider.log("Item stored in db: %s %r" % (guid, item))

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        log.err(failure)

    def _get_guid(self, item):
        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
        return md5(item['link_address']).hexdigest()


class Netbian_Json_Pipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('%s_information.jsonl' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = JsonLinesItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class Netbian_Duplicates_Pipeline(object):
    def __init__(self):
        self.link_set = set()

    def process_item(self, item, spider):
        if item['link_address'] in self.link_set:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.link_set.add(item['link_address'])
            return item


class Myimage_Crwaler_Pipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['images'] = image_paths
        return item

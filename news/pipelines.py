# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter


class NewsPipeline(object):

    def open_spider(self, spider):
        self.file_clean = open('{}_clean.csv'.format(spider.name), 'wb')
        self.file_raw = open('{}_raw.csv'.format(spider.name), 'wb')

        self.exporter_clean = CsvItemExporter(self.file_clean)
        self.exporter_raw = CsvItemExporter(self.file_raw)

        self.exporter_clean.start_exporting()
        self.exporter_raw.start_exporting()

    def close_spider(self, spider):
        self.file_clean.close()
        self.file_raw.close()

        self.exporter_clean.finish_exporting()
        self.exporter_raw.finish_exporting()

    def process_item(self, item, spider):
        self.exporter_clean.export_item(item['clean'])
        self.exporter_raw.export_item(item['raw'])
        return item

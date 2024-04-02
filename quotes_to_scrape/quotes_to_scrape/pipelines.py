# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class MultiJSONPipeline:
    def __init__(self):
        self.authors_file = open('authors.json', 'w', encoding='utf-8')
        self.quotes_file = open('quotes.json', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.authors_file.close()
        self.quotes_file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        if 'fullname' in item:
            self.authors_file.write(line)
        elif 'quote' in item:
            self.quotes_file.write(line)
        return item

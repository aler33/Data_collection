# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.book220720

    def process_item(self, item, spider):
        item['base_price'] = self.process_base_price(item['base_price'])
        item['sale_price'] = self.process_sale_price(item['sale_price'])
        item['buy_price'] = self.process_buy_price(item['buy_price'], item['sale_price'])
        item['rating'] = self.process_rating(item['rating'])
        item['name'] = self.process_name(item['name'])
        item['_id'] = self.process_id(item['url'])
        # print(item)

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        # print(item)
        return item

    def process_base_price(self, base_price):
        if not base_price:
            return base_price
        return int(base_price)

    def process_sale_price(self, sale_price):
        if not sale_price:
            return sale_price
        return int(sale_price)

    def process_buy_price(self, buy_price, sale_price):
        if not buy_price:
            buy_price = sale_price
        return int(buy_price)

    def process_rating(self, rating):
        return round(float(rating), 2)

    def process_name(self, name):
        if ':' in name:
            re_name = (re.split(r':', name))
            name = re_name[1]
            if name[0] == ' ':
                name = name[1:]
        return name

    def process_id(self, url):
        return hash(url)


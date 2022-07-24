# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def process_old_price(old_price):
    if not old_price:
        return old_price
    try:
        return (int(old_price.replace(' ', '')))
    except:
        pass


def process_price(price):
    if not price:
        return price
    try:
        return int(price.replace(' ', ''))
    except:
        pass


def process_id(_id):
    _id = hash(_id)
    return _id


class JobparserItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    old_price = scrapy.Field(input_processor=MapCompose(process_old_price), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(process_price), output_processor=TakeFirst())
    photos = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field(input_processor=MapCompose(process_id), output_processor=TakeFirst())



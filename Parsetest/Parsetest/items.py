import scrapy
from w3lib.html import remove_tags
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose


def remove_currency(value):
    return value.replace('\xa0', '').strip()

class RozItem(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(remove_tags), output_process=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_tags, remove_currency), output_process=TakeFirst())


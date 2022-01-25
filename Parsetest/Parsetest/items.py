import scrapy


class RozItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    # img = scrapy.Field()

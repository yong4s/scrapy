import scrapy
from Parsetest.items import RozItem
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.http.request import Request

class RozetkascrSpider(scrapy.Spider):
    name = 'rozetkascr'
    # # allowed_domains = ['rozetka.com.ua']
    start_urls = ['https://rozetka.com.ua/']





    def parse(self, response):
        for link in response.css('div.menu-wrapper.menu-wrapper_state_static.ng-star-inserted ul li a::attr(href)').extract():
            yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        for link1 in response.css('a.tile-cats__heading.tile-cats__heading_type_center.ng-star-inserted::attr(href)').extract():
            yield response.follow(link1, callback=self.parse_products)

    def parse_products(self, response):
        item = RozItem()
        for products in response.css('li.catalog-grid__cell.catalog-grid__cell_type_slim.ng-star-inserted'):
            item['name'] = products.css('span.goods-tile__title::text').get()
            item['price'] = products.css('p.ng-star-inserted span.goods-tile__price-value::text').get().replace('\xa0', '')
            yield item

        next_page = response.css('a.button.button--gray.button--medium.pagination__direction.pagination__direction--forward.ng-star-inserted').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_products)





import scrapy
from Parsetest.items import RozItem
from scrapy.loader import ItemLoader


class RozetkascrSpider(scrapy.Spider):
    name = 'rozetkascr'
    start_urls = ['https://rozetka.com.ua/']


    def parse(self, response):
        for link in response.css('div.menu-wrapper.menu-wrapper_state_static.ng-star-inserted ul li a::attr(href)').extract():
            yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        for link in response.css('a.tile-cats__heading.tile-cats__heading_type_center.ng-star-inserted::attr(href)').extract():
            yield response.follow(link, callback=self.parse_products)

    def parse_products(self, response):
        for products in response.css('li.catalog-grid__cell.catalog-grid__cell_type_slim.ng-star-inserted'):
            l = ItemLoader(item = RozItem(), selector=products)

            l.add_css('name', 'span.goods-tile__title')
            l.add_css('price', 'span.goods-tile__price-value')

            yield l.load_item()

        next_page = response.css('a.button.button--gray.button--medium.pagination__direction.pagination__direction--forward.ng-star-inserted').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_products)



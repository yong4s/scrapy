import scrapy
from Parsetest.items import RozItem

class RozetkascrSpider(scrapy.Spider):
    name = 'rozetkascr'
    # allowed_domains = ['rozetka.com.ua']
    start_urls = ['https://rozetka.com.ua/notebooks/c80004/']

    def parse(self, response):
        item = RozItem()
        for products in response.css('li.catalog-grid__cell.catalog-grid__cell_type_slim.ng-star-inserted'):
            item['name'] = products.css('span.goods-tile__title::text').get()
            item['price'] = products.css('p.ng-star-inserted span.goods-tile__price-value::text').get().replace('\xa0', '')
            yield item

        next_page = response.css('a.button.button--gray.button--medium.pagination__direction.pagination__direction--forward.ng-star-inserted').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

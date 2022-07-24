import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/best/']

    def parse(self, response):
        next_page = response.xpath("//div[@class='pagination-next']/a/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@class='product-title-link']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        author = response.xpath("//div[@class='authors']/a/text()").get()
        buy_price = response.xpath("//span[@class='buying-price-val']/span/text()").get()
        base_price = response.xpath("//div[@class='buying-priceold-val']/span/text()").get()
        sale_price = response.xpath("//div[@class='buying-pricenew-val']/span/text()").get()
        rating = response.xpath("//div[@id='rate']/text()").get()
        url = response.url
        yield JobparserItem(name=name, author=author, url=url, base_price=base_price, sale_price=sale_price, rating=rating, buy_price=buy_price)

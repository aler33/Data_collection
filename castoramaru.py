import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from scrapy.loader import ItemLoader


class CastoramaruSpider(scrapy.Spider):
    name = 'castoramaru'
    allowed_domains = ['castorama.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.castorama.ru/catalogsearch/result/?q={kwargs.get("search")}/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='next i-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@class='product-card__img-link']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=JobparserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('old_price', "//div[@class='add-to-cart__price js-fixed-panel-trigger']//div[@class='old-price']//span/text()")
        loader.add_xpath('price', "//div[@class='add-to-cart__price js-fixed-panel-trigger']//div[@class='current-price']//span/text()")
        loader.add_xpath('photos', "//li//img[@role='presentation']/@src | //li//img[@class='top-slide__img swiper-lazy']/@data-src")
        loader.add_value('url', response.url)
        loader.add_value('_id', response.url)
        yield loader.load_item()




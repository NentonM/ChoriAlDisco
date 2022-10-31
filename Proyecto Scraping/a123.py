import scrapy


class A123Spider(scrapy.Spider):
    name = '123'
    allowed_domains = ['123.com']
    start_urls = ['http://123.com/']

    def parse(self, response):
        pass

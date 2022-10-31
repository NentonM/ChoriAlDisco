
import scrapy
import json

class SoResponseItem(scrapy.Item):
        name = scrapy.Field()
        condition = scrapy.Field()
        price = scrapy.Field()
        rarity = scrapy.Field()

class LoginspiderSpider(scrapy.Spider):
    name = 'LoginSpider'
    allowed_domains = ['www.starcitygames.com']
    url = 'http://www.starcitygames.com/'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        url = response.urljoin('buylist/search?search-type=category&id=5061')
        yield scrapy.Request(url=url, callback=self.parse_data)

    def parse_data(self, response):
        jsonreponse = json.loads(response.body)
        for result in jsonreponse['results']:
            for index in range(len(result)):
                items = SoResponseItem()
                items['name'] = result[index]['name']
                items['condition'] = result[index]['condition']
                items['price'] = result[index]['price']
                items['rarity'] = result[index]['rarity']
                yield items
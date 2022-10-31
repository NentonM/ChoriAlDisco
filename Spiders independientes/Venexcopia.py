from pickle import TRUE
import time
import scrapy

from multiprocessing.connection import wait
from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

class VenexItem(Item):
    producto = Field()
    precio = Field()
    PN = Field()
    EAN = Field()

class VenexCrawler(CrawlSpider):
    name = 'VenexCrawler'
    allowed_domains = ['venex.com.ar']
    start_urls = [
        'https://www.venex.com.ar/componentes-de-pc/memorias-ram?limit=96',
        'https://www.venex.com.ar/componentes-de-pc/memorias-ram/notebook?limit=96',
        'https://www.venex.com.ar/componentes-de-pc/microprocesadores?limit=96',
        'https://www.venex.com.ar/componentes-de-pc/motherboards?limit=96',
        'https://www.venex.com.ar/componentes-de-pc/placas-de-video?limit=96',
        'https://www.venex.com.ar/componentes-de-pc/combos-de-actualizacion?limit=96',
        'https://www.venex.com.ar/computadoras-y-servidores?limit=96',
        'https://www.venex.com.ar/notebooks?limit=96',
    ]
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }

    rules = (
        Rule(
            LinkExtractor(
                allow=[r'.*html'],
                ),
            callback="parse_items"
        ),
    )
    
    def parse_items(self, response):
        item = ItemLoader(VenexItem(), response)
        item.add_xpath('producto', 'normalize-space(//h1[contains(@class,"tituloProducto hidden-xs")]/text())')
        item.add_xpath('precio', 'normalize-space(//div[contains(@class,"textPrecio text-green")]/text())')
        item.add_xpath('PN', '//div[contains(@class,"sub-title-product hidden-xs")]/p/text()')
        yield item.load_item()
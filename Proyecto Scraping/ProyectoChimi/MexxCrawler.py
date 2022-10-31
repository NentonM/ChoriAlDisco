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

class MexxItem(Item):
    producto = Field()
    precio = Field()
    PN = Field()
    EAN = Field()

class MexxCrawler(CrawlSpider):
    name = 'MexxCrawler'
    allowed_domains = ['mexx.com.ar']
    start_urls = [
        'https://www.mexx.com.ar/productos-rubro/notebooks/?all=1&pagina=1',
        'https://www.mexx.com.ar/productos-rubro/pcs-all-in-one-/?all=1',
        'https://www.mexx.com.ar/productos-rubro/pcs-mini-/?all=1',
        'https://www.mexx.com.ar/productos-rubro/motherboards/?all=1',
        'https://www.mexx.com.ar/productos-rubro/procesadores/?all=1',
        'https://www.mexx.com.ar/productos-rubro/memorias-ram/?all=1',
        'https://www.mexx.com.ar/productos-rubro/almacenamiento/?all=1',
        'https://www.mexx.com.ar/productos-rubro/placas-de-video/?all=1',
        'https://www.mexx.com.ar/productos-rubro/fuentes-de-poder/?all=1',
        'https://www.mexx.com.ar/productos-rubro/gabinetes/?all=1',
        'https://www.mexx.com.ar/productos-rubro/refrigeracion-pc/?all=1',
        'https://www.mexx.com.ar/productos-rubro/teclados,-mouses-y-pads/?all=1',
        'https://www.mexx.com.ar/productos-rubro/auriculares-y-microfonos-/?all=1',
        'https://www.mexx.com.ar/productos-rubro/camaras-web-e-ip/?all=1',
        'https://www.mexx.com.ar/productos-rubro/monitores/?all=1',
        'https://www.mexx.com.ar/productos-rubro/impresoras-y-plotters/?all=1',
        'https://www.mexx.com.ar/productos-rubro/escaneres-/?all=1',
        'https://www.mexx.com.ar/productos-rubro/conectividad-y-redes/?all=1',
        'https://www.mexx.com.ar/productos-rubro/ups-y-estabilizadores/?all=1',
        'https://www.mexx.com.ar/productos-rubro/sillas-y-escritorios-gamers-/?all=1',
        'https://www.mexx.com.ar/productos-rubro/consolas,-volantes-y-gamepads/?all=1',
        'https://www.mexx.com.ar/productos-rubro/parlantes-/?all=1',
        'https://www.mexx.com.ar/productos-rubro/proyectores-/?all=1',
        'https://www.mexx.com.ar/productos-rubro/software/?all=1',
        'https://www.mexx.com.ar/productos-rubro/tablets/?all=1',
        'https://www.mexx.com.ar/productos-rubro/tabletas-graficas/?all=1',
        'https://www.mexx.com.ar/productos-rubro/camaras-gopro/?all=1',
        'https://www.mexx.com.ar/productos-rubro/cables/?all=1',
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
        item = ItemLoader(MexxItem(), response)
        item.add_xpath('producto', '//h1[contains(@class,"title")]/text()')
        item.add_xpath('precio', '//h2/b[2]/text()')
        item.add_xpath('PN', '//p[contains(b,"P/N")]/text()')
        item.add_xpath('PN', '//p[contains(b,"PN")]/text()')
        item.add_xpath('EAN', '//p[contains(b,"EAN")]/text()')
        yield item.load_item()
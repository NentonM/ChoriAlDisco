### Este es el spider de Mexx. Se usa procedimiento para paginas estaticas.
import scrapy

from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

### Los modulos que importe aca son los que se van a utilizar para casos de paginas estaticas.

### Genero una Clase para los items que se generan mediante la araña. Cada item seria una Fila de datos, y cada uno de los campos que le doy al item es una Columna
### Los datos vitales son el producto y el precio. Despues el PN y el EAN es para ver si sirve para otro tipo de comparaciones mas especificas como si fuera un ID 
class MexxItem(Item):
    producto = Field()
    precio = Field()
    PN = Field()
    EAN = Field()

### Aca defino la clase del spider. Le puse Crawler por que si honestamente, pero la idea es que sea un formato tipo "Local"Crawler o algun otro termino de comuún conocimiento.
### Ya que esto me permite importar el spider en un script que me corra varios spider de manera secuencial
class MexxCrawler(CrawlSpider):
    name = 'MexxCrawler'
    allowed_domains = ['mexx.com.ar']# Esto es para que el spider no se "escape" de la web que queremos scrapear. Esto es por si detecta algun link que redirija a otro sitio.
    ### Aca abajo le doy todos los links del interior de la pagina en donde puede sacar la informacion que necesitamos
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
        'DOWNLOAD_DELAY': 1, # Este delay es para que el script no chupe la informacion de golpe y generemos un ataque a un sitio. (Eso o que nos bloqueen)
    }
    # Hay que añadirle proxys para evitar quilombos. Por el momento no sabria de donde conseguir alguno y como implementarlo aca.
    FEEDS = {
        'data.csv': {'format': 'csv', 'overwrite': True}
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

#Add_xpath basicamente funciona asi:
#    item.add_xpath('Campo', 'Ruta XPath')
#
#normalize-space lo uso para que me saque caracteres random que a veces suele extraer (Porque algunas cosas de las paginas estan hechas asi nomas)
#/text() es solo para que me retorne el texto que hay dentro del elemento que le especificamos con la ruta XPath.
#contains(@class,) me selecciona los elementos que tengan cierta clase css.

#Notese que este codigo puede ser bastante rustico o le falta pulir mucho. Eso es porque lo estoy haciendo como sale y apenas estoy empezando a programar jajaja
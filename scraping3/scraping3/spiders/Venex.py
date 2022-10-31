### Este es el spider de Venex. Venex no tiene una pagina dinamica asi que lo que utilizo es un proceso normal para obtener los elementos deseados mediante XPath
import scrapy

from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from ..items import ProductoItem as items

### Los modulos que importe aca son los que se van a utilizar para casos de paginas estaticas.


### Aca defino la clase del spider. Le puse Crawler por que si honestamente, pero la idea es que sea un formato tipo "Local"Crawler o algun otro termino de comuún conocimiento.
### Ya que esto me permite importar el spider en un script que me corra varios spider de manera secuencial
class VenexCrawler(CrawlSpider):
    name = 'VenexCrawler'
    allowed_domains = ['venex.com.ar'] # Esto es para que el spider no se "escape" de la web que queremos scrapear. Esto es por si detecta algun link que redirija a otro sitio.
    ### Aca abajo le doy todos los links del interior de la pagina en donde puede sacar la informacion que necesitamos
    start_urls = [
        'https://www.venex.com.ar/componentes-de-pc/discos-duros-mecanicos?limit=96',
        'https://www.venex.com.ar/componentes-de-pc/discos-solidos-ssd?limit=96',
        'https://www.venex.com.ar/componentes-de-pc/memorias-ram?limit=96',
        'https://www.venex.com.ar/componentes-de-pc/memorias-ram/notebook?limit=96',
        'https://www.venex.com.ar/componentes-de-pc/microprocesadores?limit=96',
        'https://www.venex.com.ar/componentes-de-pc/motherboards?limit=96',
        'https://www.venex.com.ar/componentes-de-pc/grabadoras-de-dvd?limit=96',
        'https://www.venex.com.ar/componentes-de-pc/placas-de-video?limit=96',
        'https://www.venex.com.ar/componentes-de-pc/gabinetes?limit=96',
        'https://www.venex.com.ar/componentes-de-pc/placas-de-sonido?limit=96',
        'https://www.venex.com.ar/componentes-de-pc/fuentes?limit=96',
        'https://www.venex.com.ar/componentes-de-pc/pastas-termicas?limit=96',
        'https://www.venex.com.ar/componentes-de-pc/placas-de-red?limit=96',
        'https://www.venex.com.ar/componentes-de-pc/refrigeracion?limit=96',
        'https://www.venex.com.ar/componentes-de-pc/combos-de-actualizacion?limit=96',
        'https://www.venex.com.ar/computadoras-y-servidores?limit=96',
        'https://www.venex.com.ar/notebooks?limit=96',
        'https://www.venex.com.ar/perifericos/teclados?limit=96',
        'https://www.venex.com.ar/perifericos/gaming-kit?limit=96',
        'https://www.venex.com.ar/perifericos/teclados---mouse?limit=96',
        'https://www.venex.com.ar/perifericos/mousepads?limit=96',
        'https://www.venex.com.ar/perifericos/mouse?limit=96',
        'https://www.venex.com.ar/perifericos/auriculares?limit=96',
        'https://www.venex.com.ar/perifericos/parlantes?limit=96',
        'https://www.venex.com.ar/perifericos/joystick-y-volantes?limit=96',
        'https://www.venex.com.ar/perifericos/webcams?limit=96',
        'https://www.venex.com.ar/perifericos/punteros-laser-y-presentadores?limit=96',
        'https://www.venex.com.ar/perifericos/lectores-codigo-de-barras?limit=96',
        'https://www.venex.com.ar/perifericos/microfonos?limit=96',
        'https://www.venex.com.ar/monitores?limit=96',
        'https://www.venex.com.ar/proyectores-y-pantallas?limit=96',
        'https://www.venex.com.ar/almacenamiento-portatil?limit=96',
        'https://www.venex.com.ar/hogar/herramientas?limit=96',
        'https://www.venex.com.ar/hogar/televisores?limit=96',
        'https://www.venex.com.ar/hogar/aires-acondicionados?limit=96',
        'https://www.venex.com.ar/hogar/audio?limit=96',
        'https://www.venex.com.ar/hogar/aspiradoras?limit=96',
        'https://www.venex.com.ar/hogar/calefaccion?limit=96',
        'https://www.venex.com.ar/hogar/cuidado-personal?limit=96',
        'https://www.venex.com.ar/hogar/iluminacion?limit=96',
        'https://www.venex.com.ar/hogar/maquinas-de-coser?limit=96',
        'https://www.venex.com.ar/hogar/hornos-y-microondas?limit=96',
        'https://www.venex.com.ar/hogar/electrodomesticos?limit=96',
        'https://www.venex.com.ar/hogar/juguetes?limit=96',
        'https://www.venex.com.ar/hogar/tv-box---smart?limit=96',
        'https://www.venex.com.ar/impresion-y-scanners?limit=96',
        'https://www.venex.com.ar/impresion-3d?limit=96',
        'https://www.venex.com.ar/conectividad-y-redes?limit=96',
        'https://www.venex.com.ar/tabletas-digitalizadoras?limit=96',
        'https://www.venex.com.ar/tablets?limit=96',
        'https://www.venex.com.ar/celulares-y-telefonia?limit=96',
        'https://www.venex.com.ar/seguridad?limit=96',
        'https://www.venex.com.ar/accesorios?limit=96',
        'https://www.venex.com.ar/soportes?limit=96',
        'https://www.venex.com.ar/sillas-y-butacas?limit=96',
        'https://www.venex.com.ar/estabilizadores-ups-y-zapatillas?limit=96',
    ]
    # Lo recomendable es poner links en donde tenga acceso a la mayor cantidad de productos posibles.
    custom_settings = {
        'DOWNLOAD_DELAY': 1, # Este delay es para que el script no chupe la informacion de golpe y generemos un ataque a un sitio. (Eso o que nos bloqueen)
    }
    # Hay que añadirle proxys para evitar quilombos. Por el momento no sabria de donde conseguir alguno y como implementarlo aca.

    rules = (
        Rule(
            LinkExtractor(
                allow=[r'.*html'], #Esta regla, le dice al LinkExtractor que recorra todos los links que terminen en .html (Se pueden utilizar expresiones regulares o RegEx)
                ),
            callback="parse_items" #El callback lo que hace es ejectuar una funcion despues de que entra a un link. 
        ),
    )
    
    # Esta seria la funcion principal para obtener los datos. Se activa mediante el callback del LinkExtractor.
    def parse_items(self, response):
        item = ItemLoader(items(), response) #Invocamos al item para tener en donde alojar la informacion que se extrae.
        item.add_xpath('producto', 'normalize-space(//h1[contains(@class,"tituloProducto hidden-xs")]/text())') #En producto,
        item.add_xpath('precio', 'normalize-space(//div[contains(@class,"textPrecio text-green")]/text())')
        item.add_xpath('pnEan', '//div[contains(@class,"sub-title-product hidden-xs")]/p/text()')
        yield item.load_item()

#Add_xpath basicamente funciona asi:
#    item.add_xpath('Campo', 'Ruta XPath')
#
#normalize-space lo uso para que me saque caracteres random que a veces suele extraer (Porque algunas cosas de las paginas estan hechas asi nomas)
#/text() es solo para que me retorne el texto que hay dentro del elemento que le especificamos con la ruta XPath.
#contains(@class,) me selecciona los elementos que tengan cierta clase css.

#Notese que este codigo puede ser bastante rustico o le falta pulir mucho. Eso es porque lo estoy haciendo como sale y apenas estoy empezando a programar jajaja
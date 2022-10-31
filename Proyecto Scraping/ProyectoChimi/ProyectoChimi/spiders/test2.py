# Este es el spider de CG. Es una pagina dinamica... asi que es un dolor de huevos inmenso.
import scrapy
import json
from scrapy import responsetypes

# Toda la informacion esta en un .json dentro del sitio. La idea es rastrearlo y despues obtener cierta informacion de este para poder hacerle consultas y obtener la informacion que necesitamos de el.
# De esta forma, logramos con Scrapy poder extraer informacion de paginas dinamicas.

class CGSpider(scrapy.Spider):
    name = 'CGSpider'
    allowed_domains = ['compragamer.com']
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    start_urls = ['https://compragamer.com/']
    headers = {
        "accept" : "application/json, text/plain, */*",
        "accept-encoding" : "gzip, deflate, br",
        "accept-language" : "es-AR,es-419;q=0.9,es;q=0.8",
        "origin" : "https://compragamer.com",
        "referer" : "https://compragamer.com/",
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-site": "?1",
    } #Estos son headers que se consiguen del .json y nos sirven para que se pueda ejecutar la consulta. Como funciona? Jaja nose bro disculpa

    custom_settings = {
        'DOWNLOAD_DELAY': 1, #El delay necesario. 
    }

    FEEDS = {
        'data.csv': {'format': 'csv', 'overwrite': True} 
    }

    def parse(self, response):
        yield scrapy.Request(
            url = 'https://serviciosweb.compragamer.com/net_micro_web2/productos/lista', 
            callback=self.parse_json, 
            headers= self.headers #Aparte del Callback, invocamos los headers.
            )

    def parse_json(self, response):
        data = response.json() # Newer version of Scrapy come with shortcut to get JSON data

        for i,producto in enumerate(data):
            id_producto = producto["id_producto"] #Esto es un elemento en comun de todas las listas. Itera sobre estos para entrar a cada una de estas listas y despues de esta retorna la informacion que le especificamos abajo
            yield scrapy.Request(
                f"https://serviciosweb.compragamer.com/net_micro_web2/productos/lista?ids={id_producto}",#Entra a una lista con cierto id y ejecuta la consulta
                callback=self.parse_school,
                headers=self.headers,
                dont_filter=True # Ni idea para que funciona.
            )

    def parse_school(self, response):
        data = response.json() # Newer version of Scrapy come with shortcut to get JSON data
        yield {
            "nombre": data[0]["nombre"],
            "precioEspecial": data[0]["precioEspecial"],
            "codigo_principal": data[0]["codigo_principal"],
            "vendible": data[0]["vendible"],
            "stock": data[0]["stock"],
            "id_producto": data[0]["id_producto"],
        }
# Ok esto de arriba no lo entendi del todo, siendo honesto. Lo que si se, es que lo que nosotros extraemos son dict. Para que no tire TypeError le pongo [0] que al parecer me convierte el dato en dict (la base original es en list)
# Cada uno de los campos extrae un dato en particular dentro de las listas 
# Me falta entender bien este codigo. Solo se que funciona, pero no se porque y tampoco bien el codigo
# Se ajusta segun como este registrada la informacion en el .json y listo, supongo.
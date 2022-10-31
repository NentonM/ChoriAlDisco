import scrapy
import json


class Test2Spider(scrapy.Spider):
    name = 'test2'
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
    }

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }

    def parse(self, response):
        yield scrapy.Request(
            url = 'https://serviciosweb.compragamer.com/net_micro_web2/productos/lista', 
            callback=self.parse_json, 
            headers= self.headers
            )

    def parse_json(self, response):
        raw_json = response.body
        data = json.loads(raw_json) # Newer version of Scrapy come with shortcut to get JSON data

        for i,school in enumerate(data):
            school_code = school["id_producto"]
            yield scrapy.Request(
                f"https://serviciosweb.compragamer.com/net_micro_web2/productos/lista?ids={school_code}",
                callback=self.parse_school,
                headers=self.headers,
                dont_filter=True # Many schools have the same code, same page, but listed more than once
            )

    def parse_school(self, response):
        data = json.loads(response.body) # Newer version of Scrapy come with shortcut to get JSON data
        yield {
            "nombre": data[0]["nombre"],
            "precioEspecial": data[0]["precioEspecial"],
            "codigo_principal": data[0]["codigo_principal"],
            "vendible": data[0]["vendible"],
            "stock": data[0]["stock"],
            "id_producto": data[0]["id_producto"],
        }
        
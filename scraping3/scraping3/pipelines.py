# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class scraping3Pipeline(object):
    
    # Se utiliza el metodo init para inicializar la base de datos y
    # para crear la conexion con esta y sus tablas
    def __init__(self):

        # Se crea la conexion con la DB
        self.create_conn()

        # se invoca al metodo para crear tablas
        self.create_table()
    
    # se crea un metodo de conexion para crear una DB
    # o se usa una base de datos para alojar los datos recolectados
    def create_conn(self):

        # Conectar a la base de datos
        self.conn = sqlite3.connect("spider.db")

        # referencia al cursor de conexion (?)
        self.curr = self.conn.cursor()
    
    #Creat metodo para crear tabla que use comandos SQL para crear la tabla en la DB
    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXIST firsttable""")
        self.curr.execute("""create table firsttable(
                        producto text           
                        )""")

    # guardar los items en la DB
    def process_item(self, item, spider):
        self.putitemsintable(item)
        return item
    
    def putitemsintable(self, item):

        # extraer item y añadirlo a la base de datos utilizando comandos SQL.
        self.curr.execute("""insert into firsttable values(?)""", (
            item['producto'][0],
        ))
        self.conn.commit() #cerrando conexion

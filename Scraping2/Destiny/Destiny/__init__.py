import scrapy
import twisted
from Destiny import spiders

from spiders.Venex import VenexCrawler
from spiders.Mexx import MexxCrawler
from spiders.CompraGamer import CompraGamerSpider
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(VenexCrawler)
    yield runner.crawl(MexxCrawler)
    yield runner.crawl(CompraGamerSpider)
    reactor.stop()

crawl()
reactor.run()
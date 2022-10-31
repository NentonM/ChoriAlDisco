import scrapy
import twisted
from MexxCrawler import MexxCrawler
from Venex import VenexCrawler
from test2 import Test2Spider

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(VenexCrawler)
    yield runner.crawl(MexxCrawler)
    yield runner.crawl(Test2Spider)
    reactor.stop()

crawl()
reactor.run()
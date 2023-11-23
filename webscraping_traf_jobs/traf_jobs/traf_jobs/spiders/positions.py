import scrapy


class PositionsSpider(scrapy.Spider):
    name = "positions"
    allowed_domains = ["traf.com"]
    start_urls = ["https://traf.com"]

    def parse(self, response):
        pass

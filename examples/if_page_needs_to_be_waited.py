# myspider.py
import scrapy
from scrapy_splash import SplashRequest

class MySpider(scrapy.Spider):
    name = 'myspider'

    def start_requests(self):
        url = 'https://example.com'
        yield SplashRequest(url, self.parse, args={'wait': 2})

    def parse(self, response):
        # Extract the data from the rendered page
        data = response.xpath('//div[@class="my-data"]/text()').get()
        yield {'data': data}
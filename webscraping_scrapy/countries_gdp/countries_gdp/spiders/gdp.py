import scrapy


class GdpSpider(scrapy.Spider):
    name = "gdp"
    allowed_domains = ["wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"]

    def parse(self, response):
        # print each row of tr table in wikipedia, using css selector function
        for row in response.css("table.wikitable tr"):
            print(row)

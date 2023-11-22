import scrapy
from countries_gdp.items import CountriesGdpItem
from scrapy.loader import ItemLoader

class GdpSpider(scrapy.Spider):
    name = "gdp"
    allowed_domains = ["wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"]

    def parse(self, response):

        # print each row of tr table in wikipedia, using css selector function
        for country in response.css("table.wikitable.sortable tbody tr:not([class])"):
            # using item loader
            item = ItemLoader(item=CountriesGdpItem(), selector=country)
            item.add_css("country_name", "td:nth-child(1) a::text")
            item.add_css("region", "td:nth-child(2) a::text")
            item.add_css("gdp", "td:nth-child(3) ::text")
            item.add_css("year", "td:nth-child(4) ::text")

            yield item.load_item()
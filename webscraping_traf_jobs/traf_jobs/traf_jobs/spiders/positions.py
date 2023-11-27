import scrapy


class PositionsSpider(scrapy.Spider):
    name = "positions"
    allowed_domains = ["traf.com"]
    start_urls = ["https://trafigura.wd3.myworkdayjobs.com/TrafiguraCareerSite"]

    def parse(self, response):
        for job in response.css('section#results div[role="list"] div[role="listitem"]'):
            yield {
                'title': job.css('div[role="heading"]::text').get(),
                'location': job.css('div[role="note"]::text').get(),
                'link': job.css('a::attr(href)').get()
            }

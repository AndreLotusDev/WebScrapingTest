import scrapy
from scrapy.http import FormRequest
from scrapy.selector import Selector

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['https://quotes.toscrape.com/search.aspx']

    def parse(self, response):
        # Extract ViewState and EventValidation
        viewstate = response.css('input[name="__VIEWSTATE"]::attr(value)').extract_first()
        eventvalidation = response.css('input[name="__EVENTVALIDATION"]::attr(value)').extract_first()

        # Form submission data
        formdata = {
            '__EVENTTARGET': 'ctl00$MainContent$author',
            '__VIEWSTATE': viewstate,
            '__EVENTVALIDATION': eventvalidation,
            'ctl00$MainContent$author': '1',  # Author ID, change as needed
            'ctl00$MainContent$search': 'Search',
        }

        # Submit the form
        yield FormRequest(
            url=response.url,
            formdata=formdata,
            callback=self.parse_quotes,
        )

    def parse_quotes(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            yield {
                'text': quote.css('.text::text').get(),
                'author': quote.css('.author::text').get(),
                'tags': quote.css('.tags .tag::text').getall(),
            }

        # Check if there is a next page and follow it
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse_quotes)
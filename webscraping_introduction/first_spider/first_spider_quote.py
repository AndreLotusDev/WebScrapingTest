import scrapy

class FirstSpiderQuote(scrapy.Spider):
    name = "first_spider_quote"

    custom_settings = {
        ##SET ENCONDING AS UTF 8
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        quote_blocks = response.css('div.quote')
        for quote_block in quote_blocks:
            link_about = quote_block.css('span a::attr(href)').get()
            yield response.follow(link_about, dont_filter=True, callback=self.parse_about, cb_kwargs=
            {
                'text': quote_block.css('span.text::text').get(),
                'author': quote_block.css('small.author::text').get(),
                'tags': quote_block.css('div.tags a.tag::text').getall(),
            })

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_about(self, response, **kwargs):
        yield {
            'text': kwargs['text'],
            'author': kwargs['author'],
            'tags': kwargs['tags'],
            'born_date': response.css('span.author-born-date::text').get(),
            'born_location': response.css('span.author-born-location::text').get(),
            'description': response.css('div.author-description::text').get(),
        }

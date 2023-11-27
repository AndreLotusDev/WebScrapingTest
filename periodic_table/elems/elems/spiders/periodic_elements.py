from typing import Iterable

import scrapy
from scrapy import Request


class PeriodicElementsSpider(scrapy.Spider):
    name = "periodic_elements"
    allowed_domains = ["nih.gov"]

    def start_requests(self) -> Iterable[Request]:
        yield scrapy.Request(
            'https://pubchem.ncbi.nlm.nih.gov/ptable',
            meta=dict(
                playwright=True
            )
        )

    def parse(self, response):
        pass

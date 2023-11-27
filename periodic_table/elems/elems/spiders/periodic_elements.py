from typing import Iterable

import scrapy
from scrapy import Request
from elems.items import PeriodicElementItem
from scrapy.loader import ItemLoader


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
        print(response.body)
        for element in response.css('div.ptable div.element'):
            i = ItemLoader(item=PeriodicElementItem(), selector=element)

            i.add_css('symbol', '[data-tooltip="Symbol"]')
            i.add_css('name', '[data-tooltip="Name"]')
            i.add_css('atomic_number', '[data-tooltip="Atomic Number"]')
            i.add_css('atomic_mass', '[data-tooltip*="Atomic Mass, u"]')
            i.add_css('chemical_group', '[data-tooltip="Chemical Group Block"]')

            yield i.load_item()

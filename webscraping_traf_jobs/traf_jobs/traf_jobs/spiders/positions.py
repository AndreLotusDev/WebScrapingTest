from typing import Iterable

import scrapy
from scrapy import Request


class PositionsSpider(scrapy.Spider):
    name = "positions"
    allowed_domains = ["traf.com"]
    start_urls = ["https://trafigura.wd3.myworkdayjobs.com/TrafiguraCareerSite"]

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0],
            meta={
                'playwright': True,
                'playwright_include_page': True,
                'playwright_page_methods': [
                    ('wait_for_timeout', '5000'),
                ]
            }
        )

    def parse(self, response):
        job_results_section = response.css('section[data-automation-id="jobResults"]')
        print(response.body)
        print(job_results_section)

        jobs_list = job_results_section.xpath('.//ul[@aria-label="Page 1 of 5"]')
        print(jobs_list)

        for job in jobs_list.xpath('./li'):
            yield {
                'title': job.xpath('.//a[@data-automation-id="jobTitle"]/text()').get(),
                'location': self.extract_with_label(job, 'locations'),
                'posted': self.extract_with_label(job, 'posted on'),
            }

            def extract_with_label(self, job, label):
                return job.xpath(f'.//dt[normalize-space(text())="{label}"]/following-sibling::dd[1]/text()').get()


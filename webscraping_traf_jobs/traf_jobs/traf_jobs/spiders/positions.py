from typing import Iterable
import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
from scrapy_playwright.page import PageMethod


class PositionsSpider(scrapy.Spider):
    name = "positions"
    allowed_domains = ["trafigura.wd3.myworkdayjobs.com"]
    start_urls = ["https://trafigura.wd3.myworkdayjobs.com/TrafiguraCareerSite"]

    def start_requests(self) -> Iterable[Request]:
        yield scrapy.Request(
            self.start_urls[0],
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod("wait_for_load_state", state="networkidle"),
                    PageMethod("wait_for_selector", "ul[role='list']"),
                    PageMethod("wait_for_timeout", timeout=3 * 1000),
                    PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                    PageMethod("wait_for_selector", ".css-1xuojeq"),

                ]
            )
        )

    async def parse(self, response: HtmlResponse):
        page = response.meta["playwright_page"]

        while True:
            await page.wait_for_load_state(state="networkidle")
            await page.wait_for_selector("ul[role='list']")
            content = await page.content()
            selector = Selector(text=content)

            for job in selector.css("ul[role='list'] li"):
                item = {
                    "title": job.css("div div div h3 a[data-automation-id='jobTitle']::text").get()
                }
                yield item

            next_page_available = await page.evaluate(
                "() => Boolean(document.querySelector('svg.wd-icon-chevron-right-small.wd-icon:not([disabled])'))"
            )

            if next_page_available:
                await page.click("button[aria-label='Next']")  # assuming 'Next' is the aria-label for the next page button
                await page.wait_for_event("response")
            else:
                break

        await page.close()
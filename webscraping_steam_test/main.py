from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser

URL_STEAM = 'https://store.steampowered.com/specials'

if __name__ == '__main__':
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL_STEAM)

        page.wait_for_load_state('networkidle')
        page.wait_for_load_state('load')

        #scroll to the bottom of the page
        page.evaluate('() => window.scrollTo(0, document.body.scrollHeight)')
        page.wait_for_load_state('domcontentloaded')

        page.wait_for_selector('[class^="salepreviewwidgets_StoreSaleWidgetContainer"]')

        # page.screenshot(path='steam.png', full_page=True)
        html = page.inner_html('body')
        tree = HTMLParser(html)

        divs = tree.css('[class^="salepreviewwidgets_StoreSaleWidgetContainer"]')

        for d in divs:
            title = d.css_first('[class^="salepreviewwidgets_StoreSaleWidgetTitle"]').text()
            thumbnail = d.css_first('img[class^="salepreviewwidgets_CapsuleImage"]').attributes['src']
            tags = d.css('[class^="salepreviewwidgets_StoreSaleWidgetTags"] > a')
            tags_only_text = [t.text() for t in tags]

            print(title)
            print(thumbnail)
            print(tags_only_text)

            attrs = {
                'title': title,
                'thumbnail': thumbnail,
                'tags': tags_only_text
            }

        browser.close()
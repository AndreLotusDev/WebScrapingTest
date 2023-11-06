from playwright.sync_api import sync_playwright

# '[class^="salepreviewwidgets_StoreSaleWidgetContainer"]'

def extract_full_body_html(steam_url, wait_for=None):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(steam_url)

        page.wait_for_load_state('networkidle')
        page.wait_for_load_state('load')

        # scroll to the bottom of the page
        page.evaluate('() => window.scrollTo(0, document.body.scrollHeight)')
        page.wait_for_load_state('domcontentloaded')

        if(wait_for):
            page.wait_for_selector(wait_for)

        # page.screenshot(path='steam.png', full_page=True)
        html = page.inner_html('body')
        return html
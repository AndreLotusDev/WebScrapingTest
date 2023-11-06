from playwright.sync_api import sync_playwright

URL_STEAM = 'https://store.steampowered.com/search/?specials'

if __name__ == '__main__':
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL_STEAM)

        page.screenshot(path='steam.png', full_page=True)
        browser.close()



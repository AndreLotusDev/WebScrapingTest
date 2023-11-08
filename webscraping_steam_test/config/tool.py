import json

_config = {
    "url": 'https://store.steampowered.com/specials',
    "container":
    {
            "name": "store_sales_divs",
            "selector": 'div[class*="salepreviewwidgets_StoreSaleWidgetContainer"]',
            "match": "all",
            "type": "node"
    },
    "item": [
        {
            "name": "title",
            "selector": '[class^="salepreviewwidgets_StoreSaleWidgetTitle"]',
            "match": "first",
            "type": "text"
        },
        {
            "name": "thumbnail",
            "selector": 'img[class*="CapsuleImage"]',
            "match": "first",
            "type": "node"
        },
        {
            "name": "tags",
            "selector": '[class^="salepreviewwidgets_StoreSaleWidgetTags"] > a',
            "match": "all",
            "type": "text"
        },
        {
            "name": "release_date",
            "selector": '[class*="salepreviewwidgets_WidgetReleaseDateAndPlatformCtn"] > div[class*="StoreSaleWidgetRelease"]',
            "match": "first",
            "type": "text"
        },
        {
            "name": "reviewed_by",
            "selector": '[class*="ReviewScoreCount"]',
            "match": "first",
            "type": "text"
        },
        {
            "name": "review_score",
            "selector": '[class*="ReviewScoreValue"] > div',
            "match": "first",
            "type": "text"
        },
        {
            "name": "sale_price",
            "selector": '[class*="salepreviewwidgets_StoreSalePriceBox"]',
            "match": "first",
            "type": "text"
        },
        {
            "name": "normal_price",
            "selector": '[class*="salepreviewwidgets_StoreOriginalPrice"]',
            "match": "first",
            "type": "text"
        },
        {
            "name": "price_currency",
            "selector": 'div[class*="StoreSalePriceBox"]',
            "match": "first",
            "type": "text"
        }
    ]
}

def get_config(load_from_file=False):
    if(load_from_file):
        with open('config.json', 'r') as f:
            return json.load(f)
    else:
        return _config


def generate_config():
    with open('config.json', 'w') as f:
        json.dump(_config, f, indent=4)

# run as main
if __name__ == '__main__':
    generate_config()
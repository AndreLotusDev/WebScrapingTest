from selectolax.parser import HTMLParser
from utils.extract import  extract_full_body_html
from utils.parser import parse_raw_attributes
from config.tool import get_config
from utils.process import format_and_transform

if __name__ == '__main__':

    config = get_config()

    html = extract_full_body_html(
        config.get('url'),
        wait_for=config.get('container').get('selector')
    )

    tree = HTMLParser(html)

    divs = tree.css(config.get('container').get('selector'))

    for d in divs:
        attrs = parse_raw_attributes(d, config.get('item'))
        attrs = format_and_transform(attrs)

        print(attrs)

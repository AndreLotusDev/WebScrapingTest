from scrapy.http import HtmlResponse
from chompjs import ChompJS

def parse_product_page(response: HtmlResponse):
    # Create a ChompJS instance
    chomp = ChompJS(response.body)

    # Execute the JavaScript code to load the product information
    rich_product_data = chomp.evaluate('window.productData')

    # Extract the product details from the rich_product_data object
    product_title = rich_product_data['title']
    product_price = rich_product_data['price']
    product_description = rich_product_data['description']

    # Do something with the extracted product details
    print(product_title, product_price, product_description)
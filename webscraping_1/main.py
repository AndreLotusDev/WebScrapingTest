import requests
from bs4 import BeautifulSoup
from requests import Response
import sys
from product import Product
import re

OK_STATUS_CODE = 200

url = 'https://webscraper.io/test-sites/e-commerce/allinone/phones/touch'

result: Response = requests.get(url)

if(result.status_code != OK_STATUS_CODE):
    sys.exit("Something went wrong")

soup = BeautifulSoup(result.text, 'html.parser')
##find div with clas container test-site
product_container = soup.find('div', {'class': 'container test-site'})
row_with_products = product_container.find('div', {'class': 'row'})

products = row_with_products.find_all('div', {'class': 'col-md-4 col-xl-4 col-lg-4'})

list_products = []

for product in products:
    product_name = product.find('a', {'class': 'title'}).text
    product_price = product.find('h4', {'class': 'float-end price card-title pull-right'}).text
    product_description = product.find('p', {'class': 'description card-text'}).text
    print(f'Product name: {product_name}')
    print(f'Product price: {product_price}')
    print(f'Product description: {product_description}')

    number_string = re.sub(r'[^0-9.]', '', product_price)
    price_only_numbers = float(number_string)

    product_to_add = Product(product_name, price_only_numbers, product_description)
    list_products.append(product_to_add)

print('\n')
print(len(list_products))

##get maximum price
max_price = 0
for product in list_products:
    if product.price > max_price:
        max_price = product.price

print(f'Max price: {max_price}')
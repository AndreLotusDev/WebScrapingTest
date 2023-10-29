import requests
from bs4 import BeautifulSoup

URL_BASE = 'https://www.marketwatch.com/investing/stock/aapl'

page_requested = requests.get(URL_BASE)

soup = BeautifulSoup(page_requested.text, 'html.parser')
#print(soup)

# Get the price
price = soup.find('bg-quote', {'class': 'value'}).text
#print(price)

# Get closing price stock
closing_price = soup.find('td', {'class': 'table__cell u-semi'}).text
#print(closing_price)

# Get the 52 week range(lower, upper)
range_52_week = soup.find('mw-rangebar', {'class': 'element element--range range--yearly'})
#print(range_52_week)

lower_range = range_52_week.findAll('span', {'class': 'primary'})[0].text
print(lower_range)

upper_range = range_52_week.findAll('span', {'class': 'primary'})[1].text
print(upper_range)

# analyst rating
analyst_rating = soup.find('li', {'class': 'analyst__option active'}).text
print(analyst_rating)
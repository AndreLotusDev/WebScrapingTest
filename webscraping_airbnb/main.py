import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import datetime
import re
import spacy
from price_parser import Price

nlp = spacy.load("pt_core_news_sm")

# this code works in 10 - 29 - 2013
def generate_text(text_to_generate):
    actual_only_date_datetime = datetime.datetime.now()
    #replace : to _ in date
    actual_only_date_datetime = str(actual_only_date_datetime).replace(':', '_')
    actual_dir = os.getcwd()
    file_path = actual_dir + '/soup_' + actual_only_date_datetime + '.html'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(text_to_generate))
def filter_func(tag):
    #try catch
    try:
        if tag.name != 'div':
            return False
        if not tag.has_attr('aria-labelledby'):
            return False
        if not tag['aria-labelledby'].startswith('title_'):
            return False

        return True
    except:
        return False

URL_BASE = 'https://www.airbnb.com.br'
URL_BASE_FOR_SEARCH = 'https://www.airbnb.com.br/s/Matinhos-~-PR/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-11-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Matinhos%20-%20PR&place_id=ChIJ8SCG7y3u25QRVTkDb8dp8OE&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click'

page = requests.get(URL_BASE_FOR_SEARCH)
soup = BeautifulSoup(page.text, 'html.parser')

#get by aria-label="Paginação de resultados de busca"
pagination = soup.find('nav', attrs={'aria-label': 'Paginação de resultados de busca'})

#get first a inside pagination
first_a = pagination.find('a')
href_value = first_a['href']

#get divs with usefull info
grid = soup.findAll(filter_func)

for card in grid:

    link_to_new_page = card.find('a')
    link_to_new_page_href = link_to_new_page['href']
    pure_image = card.find('img')['src']
    children_div = ''

    first_div = card.find('div')
    ZERO_VALUE = 0
    actual_value = 0
    for child in first_div.children:
        if actual_value == 1:
            actual_value = ZERO_VALUE
            children_div = child
        actual_value += 1

    title = children_div.find_all('div')[0].text
    description = children_div.find_all('div')[1].text
    beds = children_div.find_all('div')[2].text
    date = children_div.find_all('div')[3].text

    pricing = children_div.find_all('div')[4].find('span').find('div').text
    numbers = re.findall(r'(\d+\.\d+|\d+)', pricing)
    result_pricing = Price.fromstring(pricing)
    currency = result_pricing.currency
    rating = 0
    num_ratings = 0

    for each_line_of_desc in children_div.children:
        if each_line_of_desc.name == 'span':
            text = "4,98 (45)"
            pattern = r'(\d+,?\d*) \((\d+)\)'

            match = re.search(pattern, text)
            rating = match.group(1)
            num_ratings = match.group(2)

    #WIP
    # doc = nlp(pricing)
    # print(doc.ents)
    # for ent in doc.ents:
    #     if ent.label_ == "MONEY":
    #         currency = ent.text

next_page = URL_BASE + href_value


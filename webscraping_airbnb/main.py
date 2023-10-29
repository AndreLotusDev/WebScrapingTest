import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import datetime
import spacy
from grid_extraction_logic import GridExtractionLogic
from random import uniform
import time

nlp = spacy.load("pt_core_news_sm")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# this code works in 10 - 29 - 2013
def generate_text(text_to_generate):
    actual_only_date_datetime = datetime.datetime.now()
    #replace : to _ in date
    actual_only_date_datetime = str(actual_only_date_datetime).replace(':', '_').replace('-', "_")
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

pagination = soup.find('nav', attrs={'aria-label': 'Paginação de resultados de busca'})

next_button = pagination.find('a', attrs={'aria-label': 'Próximo'})
href_value = next_button['href']
requests_made = 0

all_grids = []

while href_value != None or href_value != '' :
    sleep_duration = uniform(1, 2)
    time.sleep(sleep_duration)
    print('requests made' + str(requests_made))
    page = requests.get(URL_BASE + href_value)
    soup = BeautifulSoup(page.text, 'html.parser')

    pagination = soup.find('nav', attrs={'aria-label': 'Paginação de resultados de busca'})

    next_button = pagination.find('a', {'aria-label': 'Próximo'})
    if(next_button == None):
        break

    href_value = next_button['href']
    print(href_value)
    requests_made += 1

    temp_grid = soup.findAll(filter_func)
    all_grids.append(temp_grid)

do_one_time = False
qtd = 0

data_array = []

for _temp_grid in all_grids:
    GridExtractionLogic.Run(_temp_grid, do_one_time, qtd, data_array, URL_BASE, headers)

df_to_export = pd.DataFrame(data_array)

actual_directory = os.getcwd()
actual_only_date_datetime = datetime.datetime.now()
actual_only_date_datetime = str(actual_only_date_datetime).replace(':', '_').replace('-', "_")
with pd.ExcelWriter(actual_directory + "\\" + actual_only_date_datetime + ".xlsx", engine='openpyxl') as writer:
    df_to_export.to_excel(writer, sheet_name='main', index=False)



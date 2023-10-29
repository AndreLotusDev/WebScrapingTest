import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

WORLD_METER_URL = 'https://www.worldometers.info/world-population/'

page = requests.get(WORLD_METER_URL)

soup = BeautifulSoup(page.content, 'html.parser')

#find table

table = soup.find('table', class_ = 'table table-striped table-bordered table-hover table-condensed table-list')

all_th = table.find_all('th')

header = [th.text for th in all_th]

#create data frame with headers
df = pd.DataFrame(columns = header)

#find all rows
all_tr = table.find_all('tr')[1:]

for tr in all_tr:
    td = tr.find_all('td')
    row = [tr.text for tr in td]
    length = len(df)
    df.loc[length] = row

current_directory = os.getcwd()
df.to_csv(current_directory + "\\" + "world_population.csv")
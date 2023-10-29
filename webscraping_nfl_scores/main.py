import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

NFL_2019 = 'https://www.nfl.com/standings/league/2019/reg'

page = requests.get(NFL_2019)
soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find('table', {'summary':'Standings - Detailed View'})

headers = []

for i in table.find_all('th'):
    title = i.text.strip()
    headers.append(title)

df = pd.DataFrame(columns = headers)

for j in table.find_all('tr')[1:]:
    first_td = j.find_all('td')[0].find('div', class_ = 'd3-o-club-fullname').text.strip()
    data = j.find_all('td')[1:]
    row_data = [td.text.strip() for td in data]
    row_data.insert(0, first_td)
    length = len(df)
    df.loc[length] = row_data

actual_directory = os.getcwd()

# Write to Excel
with pd.ExcelWriter(actual_directory + "\\" + "NFL_2019.xlsx", engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='main', index=False)
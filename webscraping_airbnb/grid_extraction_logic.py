from price_parser import Price
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import re
import requests
from bs4 import BeautifulSoup

class GridExtractionLogic:
    @staticmethod
    def Run(grid, do_one_time, qtd, data_array, URL_BASE, headers):
        for card in grid:

            if do_one_time and qtd == 1:
                break

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

            new_url = URL_BASE + link_to_new_page_href
            # Parse the URL into its components
            parsed_url = urlparse(new_url)

            # Extract the query parameters as a dictionary
            query_params = parse_qs(parsed_url.query)

            # Create a new dictionary containing only the source_impression_id parameter
            new_query_params = {
                "source_impression_id": query_params["source_impression_id"][0]
            }

            # Construct the new URL
            new_url = urlunparse(
                (
                    parsed_url.scheme,
                    parsed_url.netloc,
                    parsed_url.path,
                    parsed_url.params,
                    urlencode(new_query_params),
                    parsed_url.fragment
                )
            )

            # new_page = requests.get(new_url, headers=headers)
            # new_soup = BeautifulSoup(new_page.text, 'html.parser')

            # retrieve_address = new_soup.find('div', attrs={'data-section-id': 'TITLE_DEFAULT'})
            # print(retrieve_address.children.find('div').children.find('section').children.find_all('div')[1].text)
            # print(retrieve_address.findChild('div').findChild('section').findChildren('div')[1].text)
            # generate_text(retrieve_address)

            obj = {
                "title": title,
                "description": description,
                "beds": beds,
                "date": date,
                "pricing": pricing,
                "currency": currency,
                "rating": rating,
                "num_ratings": num_ratings,
                "pure_image": pure_image,
                "new_url": new_url
            }

            data_array.append(obj)

            qtd += 1

            # generate df to export a posteriori in excel

            # WIP
            # doc = nlp(pricing)
            # print(doc.ents)
            # for ent in doc.ents:
            #     if ent.label_ == "MONEY":
            #         currency = ent.text
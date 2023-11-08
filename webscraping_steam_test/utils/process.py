import re
from datetime import datetime
from pandas.core.frame import DataFrame as df
import pandas as pd
import openpyxl

from selectolax.parser import Node

def get_attrs_from_node(node: Node, attr: str):
    if node:
        return node.attributes.get(attr)

    return None

def get_first_n(input_list: list, n: int):
    if input_list:
        value_to_return = input_list[:n]
        return value_to_return

    return None

def reformat_date(date: str, old_format: str, new_format: str):
    if date:
        return datetime.strptime(date, old_format).strftime(new_format)

    return None

def format_number_using_regex(input: str, regex: str):
    if input and input != "N/A":
        numbers_string = re.findall(regex, input)
        return int(numbers_string[0].replace(",", ""))

    return input

def currency_pattern_at_begging(input: str):
    currency_pattern = r"^[^\d]*"

    if input:
        currency_symbol = re.findall(currency_pattern, input)[0]
        remaining_string = input[len(currency_symbol):]
        return currency_symbol

    return None

def get_number_withouth_currency(input: str):
    currency_pattern = r"^[^\d]*"

    if input:
        currency_symbol = re.findall(currency_pattern, input)[0]
        remaining_string = input[len(currency_symbol):]
        return float(remaining_string.replace(",", "."))

    return None

def format_and_transform(attrs: dict):
    transforms = {
        "thumbnail": lambda n: get_attrs_from_node(n, "src"),
        "tags": lambda input_list: get_first_n(input_list, 5),
        "release_date": lambda date: reformat_date(date, "%b %d, %Y", "%Y-%m-%d"),
        "reviewed_by": lambda input: format_number_using_regex(input, r"[0-9,]+"),
        "price_currency": lambda input: currency_pattern_at_begging(input),
        "sale_price": lambda input: get_number_withouth_currency(input),
        "normal_price": lambda input: get_number_withouth_currency(input),
    }

    for k, v in transforms.items():
        if k in attrs:
            attrs[k] = v(attrs[k])


    return attrs


def save_to_file(filename="extract", data: list[dict] = None):
    if data is None:
        raise ValueError("The function expects data to be provided as a list of dictionaries")

    df = pd.DataFrame(data)
    filename = f"{datetime.now().strftime('%Y_%m_%d')}_{filename}.xlsx"

    writer = pd.ExcelWriter(filename)
    df.to_excel(writer)
    writer.close()

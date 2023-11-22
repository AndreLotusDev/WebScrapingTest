import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags

def remove_commas(value):
    return value.replace(",", "")

def replace_gdp(value):
    return value.replace("-", "0")

def try_float(value):
    try:
        return float(value)
    except ValueError:
        return None

def try_int(value):
    try:
        return int(value)
    except ValueError:
        return None

def extract_year(value):
    return value[-4:]

class CountriesGdpItem(scrapy.Item):
    country_name = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.split),
        output_processor=TakeFirst()
    )
    region = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.split),
        output_processor=TakeFirst()
    )
    gdp = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.split, replace_gdp, remove_commas, try_float),
        output_processor=TakeFirst()
    )
    year = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.split,extract_year, try_int),
        output_processor=TakeFirst()
    )
    pass

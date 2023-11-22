from scrapy.exceptions import DropItem

class CountriesGdpPipeline:
    def process_item(self, item, spider):
        if not isinstance(item["gdp", float]):
            raise DropItem("Missing gdp in %s" % item)

        return item
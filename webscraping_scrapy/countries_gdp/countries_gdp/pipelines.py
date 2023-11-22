from scrapy.exceptions import DropItem
import sqlite3

class CountriesGdpPipeline:
    def process_item(self, item, spider):
        print(item)
        if not isinstance(item["gdp"], float):
            raise DropItem("Missing gdp in %s" % item)

        return item


class SaveToDatabasePipeline:
    def __init__(self):
        self.con = sqlite3.connect("countries_gdp.db")
        self.cur = self.con.cursor()

    def open_spider(self, spider):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS countries_gdp (
            country_name TEXT PRIMARY KEY,
            region TEXT,
            gdp REAL,
            year INTEGER)
        """)
        self.con.commit()

    def process_item(self, item, spider):
        print(item)
        self.cur.execute(
            """INSERT INTO countries_gdp (country_name, region, gdp, year) VALUES(?, ?, ?, ?)""",
(
                item["country_name"],
                item["region"],
                item["gdp"],
                item["year"]
            )
        )
        self.con.commit()
        return item

    def close_spider(self, spider):
        self.con.close()

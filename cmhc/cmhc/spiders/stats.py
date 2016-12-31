import scrapy
import os
import yaml


def province_codes():
    with open(os.path.join(os.path.dirname(__file__), '..', 'provinces.yml'), 'r') as f:
        data = yaml.load(f)
        return data.values()


class StatsSpider(scrapy.Spider):
    name = "stats"
    allowed_domains = ["www03.cmhc-schl.gc.ca"]
    start_urls = ["https://www03.cmhc-schl.gc.ca/hmip-pimh/en/Navigation/MetsByProvince/" + str(code) for code in province_codes()]

    def parse(self, response):
        pass

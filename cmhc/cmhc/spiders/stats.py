import scrapy
import os
import yaml
from urllib import parse
from bs4 import BeautifulSoup
import json
import logging


def province_codes():
    with open(os.path.join(os.path.dirname(__file__), '..', 'provinces.yml'), 'r') as f:
        data = yaml.load(f)
    return data


class StatsSpider(scrapy.Spider):
    name = "stats"
    allowed_domains = ["www03.cmhc-schl.gc.ca"]
    METS_REQUEST_URL = "https://www03.cmhc-schl.gc.ca/hmip-pimh/en/Navigation/MetsByProvince/"
    DATA_URL = "https://www03.cmhc-schl.gc.ca/hmip-pimh/en/TableMapChart/TableMatchingCriteria"
    EMBEDDED_DATA_URL = "https://www03.cmhc-schl.gc.ca/hmip-pimh/en/TableMapChart/RenderTable"

    HEADERS = {
        'Accept': 'text/html, */*; q=0.01',
        'Origin': 'https://www03.cmhc-schl.gc.ca',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8',
    }

    def __init__(self, *args, **kwargs):
        logger = logging.getLogger('scrapy.core.scraper')
        logger.setLevel(logging.WARNING)
        super().__init__(*args, **kwargs)

    def initial_request(self, province, code):
        return scrapy.Request(
            self.METS_REQUEST_URL + str(code),
            callback=self.mets_for_province,
            headers=self.HEADERS,
            meta={'province': province, 'province_code': code}
        )

    def start_requests(self):
        for (province, code) in province_codes().items():
            yield self.initial_request(province, code)

    @staticmethod
    def parse_met_data(body):
        page = BeautifulSoup(body, 'html.parser')
        cma = page.find_all('a', **{'data-type': 'MetropolitanMajorArea'})

        for node in cma:
            yield (node['data-id'], node.text)

    def vacancy_rate_request(self, met_id, met_name, meta):
        params = parse.urlencode({
            'GeographyType': 'MetropolitanMajorArea',
            'GeographyId': met_id,
            'CategoryLevel1': 'Primary Rental Market',
            'CategoryLevel2': 'Vacancy Rate (%)',
        })
        meta['data_type'] = 'Vacancy Rate (%)'
        meta['met_id'] = met_id
        meta['met_name']= met_name

        return scrapy.Request(
            self.DATA_URL + "?" + params,
            callback=self.vacancy_data_availability,
            headers=self.HEADERS,
            meta=meta,
        )

    def mets_for_province(self, response):
        data = self.parse_met_data(response.body)
        meta = {
            'province': response.meta['province'],
            'province_code': response.meta['province_code'],
        }

        for (met_id, name) in data:
            yield self.vacancy_rate_request(met_id, name, meta)

    @staticmethod
    def vacancy_rate_available_periods(body):
        page = BeautifulSoup(body, 'html.parser')
        time_periods = json.loads(page.find('input', id="serialized-model")['data-table-model'])
        for availability in time_periods['AvailableTimePeriods']:
            yield (availability['Year'], availability['Month'])

    def vacancy_data_availability(self, response):
        available_periods = self.vacancy_rate_available_periods(response.body)
        data = {
            'AppliedFilters[0].Key': 'dwelling_type_desc_en',
            'AppliedFilters[0].Value': 'Row / Apartment',
            'BreakdownGeographyTypeId': '7',
            'DataSource': '2',
            'DefaultDataField': 'vacancy_rate_pct',
            'DisplayAs': 'Table',
            'ForTimePeriod.Quarter': '',
            'ForTimePeriod.Season': '',
            'Frequency': '',
            'GeograghyName': response.meta['met_name'],
            'GeographyId': response.meta['met_id'],
            'GeographyTypeId': '3',
            'RowSortKey': '',
            'SearchCriteria': '',
            'Survey': 'Rms',
            'TableId': '2.1.1.6',
            'Ytd': 'false',
        }

        meta = {
            'province': response.meta['province'],
            'province_code': response.meta['province_code'],
            'met_id': response.meta['met_id'],
            'met_name': response.meta['met_name'],
            'data_type': response.meta['data_type'],
        }

        for (year, month) in available_periods:
            data['ForTimePeriod.Month'] = month
            data['ForTimePeriod.Year'] = year
            body = parse.urlencode(data)
            meta['year'] = year
            meta['month'] = month

            yield scrapy.Request(
                self.EMBEDDED_DATA_URL,
                body=body,
                headers=self.HEADERS,
                callback=self.parse_vacancy_data,
                meta=meta,
            )

    @staticmethod
    def extract_vacancy_data(body):
        page = BeautifulSoup(body, 'html.parser')
        table = page.find('table', **{'class': 'CawdDataTable'})
        head = table.find('thead')
        cols = {node['data-sort-key']: node.text for node in head.find_all('th')}

        main = table.find('tbody')
        rows = main.find_all('tr')
        for row in rows:
            data = {value: row.find('td', **{'data-field': key}).text for (key, value) in cols.items()}
            for key in data:
                data[key] = None if data[key] == '**' else data[key]

            data['name'] = row.find('th').text
            yield data

    def parse_vacancy_data(self, response):
        for item in self.extract_vacancy_data(response.body):
            item['province'] = response.meta['province']
            item['province_code'] = response.meta['province_code']
            item['data_type'] = response.meta['data_type']
            item['year'] = response.meta['year']
            item['month'] = response.meta['month']
            yield item

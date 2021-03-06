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

    DEFAULT_REQUEST_CONTENT = {
        'BreakdownGeographyTypeId': '7',
        'DataSource': '2',
        'DisplayAs': 'Table',
        'ForTimePeriod.Quarter': '',
        'ForTimePeriod.Season': '',
        'Frequency': '',
        'GeographyTypeId': '3',
        'RowSortKey': '',
        'SearchCriteria': '',
        'Survey': 'Rms',
        'Ytd': 'false',
    }

    DATA_TYPES = {
        'vacancy_rate': {
            'CategoryLevel1': 'Primary Rental Market',
            'CategoryLevel2': 'Vacancy Rate (%)',
            'dimension_name': 'dwelling_type',
            'dimension_key': 'dwelling_type_desc_en',
            'dimension_value': {'Row', 'Apartment', 'Row / Apartment'},
            'DefaultDataField': 'vacancy_rate_pct',
            'TableId': '2.1.1.6',
        },
        'availability_rate': {
            'CategoryLevel1': 'Primary Rental Market',
            'CategoryLevel2': 'Availability Rate (%)',
            'dimension_name': 'dwelling_type',
            'dimension_key': 'dwelling_type_desc_en',
            'dimension_value': {'Row', 'Apartment', 'Row / Apartment'},
            'DefaultDataField': 'availability_rate_pct',
            'TableId': '2.1.6.6',
        },
        'average_rent': {
            'CategoryLevel1': 'Primary Rental Market',
            'CategoryLevel2': 'Average Rent ($)',
            'dimension_name': 'dwelling_type',
            'dimension_key': 'dwelling_type_desc_en',
            'dimension_value': {'Row', 'Apartment', 'Row / Apartment'},
            'DefaultDataField': 'average_rent_amt',
            'TableId': '2.1.11.6',
        },
        'median_rent': {
            'CategoryLevel1': 'Primary Rental Market',
            'CategoryLevel2': 'Median Rent ($)',
            'dimension_name': 'dwelling_type',
            'dimension_key': 'dwelling_type_desc_en',
            'dimension_value': {'Row', 'Apartment', 'Row / Apartment'},
            'DefaultDataField': 'rent_median_amt',
            'TableId': '2.1.21.6',
        },
        'rental_universe': {
            'CategoryLevel1': 'Primary Rental Market',
            'CategoryLevel2': 'Rental Universe',
            'dimension_name': 'dwelling_type',
            'dimension_key': 'dwelling_type_desc_en',
            'dimension_value': {'Row', 'Apartment', 'Row / Apartment'},
            'DefaultDataField': 'universe_unit_cnt',
            'TableId': '2.1.26.6',
        },
        'completions': {
            'CategoryLevel1': 'New Housing Construction',
            'CategoryLevel2': 'Completions',
            'dimension_name': 'intended_markets',
            'dimension_key': 'dimension-18',
            'dimension_value': {'Homeowner', 'Rental', 'Condo', 'Co-op', 'All'},
            'DefaultDataField': 'measure-11',
            'TableId': '1.1.2.11',
        },
        'starts': {
            'CategoryLevel1': 'New Housing Construction',
            'CategoryLevel2': 'Starts (Actual)',
            'dimension_name': 'intended_markets',
            'dimension_key': 'dimension-18',
            'dimension_value': {'Homeowner', 'Rental', 'Condo', 'Co-op', 'All'},
            'DefaultDataField': 'measure-12',
            'TableId': '1.1.1.11',
        },
        'under_construction_inventory': {
            'CategoryLevel1': 'New Housing Construction',
            'CategoryLevel2': 'Under Construction Inventory',
            'dimension_name': 'intended_markets',
            'dimension_key': 'dimension-18',
            'dimension_value': {'Homeowner', 'Rental', 'Condo', 'Co-op', 'All'},
            'DefaultDataField': 'measure-14',
            'TableId': '1.1.3.11',
        },
        'average_length_of_construction': {
            'CategoryLevel1': 'New Housing Construction',
            'CategoryLevel2': 'Length of Construction (in months)',
            'dimension_name': 'intended_markets',
            'dimension_key': 'dimension-18',
            'dimension_value': {'Homeowner', 'Rental', 'Condo', 'Co-op', 'All'},
            'DefaultDataField': 'measure-17',
            'TableId': '1.1.7.9',
        },
        'absorbed_units': {
            'CategoryLevel1': 'New Housing Construction',
            'CategoryLevel2': 'Absorbed Units (Homeowner & Condo)',
            'dimension_name': 'intended_markets',
            'dimension_key': 'dimension-18',
            'dimension_value': {'Homeowner', 'Condo', 'All'},
            'DefaultDataField': 'measure-20',
            'TableId': '1.1.5.9',
        },
        'percent_absorbed_units_at_completion': {
            'CategoryLevel1': 'New Housing Construction',
            'CategoryLevel2': '% of Absorbed Units at Completion (Homeowner & Condo)',
            'dimension_name': 'intended_markets',
            'dimension_key': 'dimension-18',
            'dimension_values': {'Homeowner', 'Condo'},
            'DefaultDataField': 'measure-16',
            'TableId': '1.1.6.9',
        },
        'completed_unabsorbed_units_inventory': {
            'CategoryLevel1': 'New Housing Construction',
            'CategoryLevel2': 'Inventory of Completed and Unabsorbed Units (Homeowner & Condo)',
            'dimension_name': 'intended_markets',
            'dimension_key': 'dimension-id',
            'dimension_values': {'Homeowner', 'Condo'},
            'DefaultDataField': 'measure-15',
            'TableId': '1.1.4.9',
        },
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

    def data_availability_request(self, met_id, met_name, data_type, meta):
        params = parse.urlencode({
            'GeographyType': 'MetropolitanMajorArea',
            'GeographyId': met_id,
            'CategoryLevel1': self.DATA_TYPES[data_type]['CategoryLevel1'],
            'CategoryLevel2': self.DATA_TYPES[data_type]['CategoryLevel2'],
        })
        meta['data_type'] = data_type
        meta['met_id'] = met_id
        meta['met_name']= met_name
        meta['dont_retry'] = True

        return scrapy.Request(
            self.DATA_URL + "?" + params,
            callback=self.data_availability,
            errback=self.data_availability_error,
            headers=self.HEADERS,
            meta=meta,
        )

    def mets_for_province(self, response):
        data = self.parse_met_data(response.body)

        for (met_id, name) in data:
            for data_type in self.DATA_TYPES:
                meta = {
                    'province': response.meta['province'],
                    'province_code': response.meta['province_code'],
                }
                yield self.data_availability_request(met_id, name, data_type, meta)

    @staticmethod
    def available_periods(body):
        page = BeautifulSoup(body, 'html.parser')
        time_periods = json.loads(page.find('input', id="serialized-model")['data-table-model'])
        for availability in time_periods['AvailableTimePeriods']:
            yield (availability['Year'], availability['Month'])

    def data_availability_error(self, failure):
        meta = failure.request.meta
        self.logger.debug("Data unavailable for province_code: {}, met_id: {}, data_type: {}".format(meta['province_code'], meta['met_id'], meta['data_type']))

    def data_availability(self, response):
        available_periods = self.available_periods(response.body)
        data_type = response.meta['data_type']
        data_fields = self.DATA_TYPES[data_type]

        data = self.DEFAULT_REQUEST_CONTENT.copy()
        data['AppliedFilters[0].Key'] = data_fields['dimension_key']
        data['DefaultDataField'] = data_fields['DefaultDataField']
        data['TableId'] = data_fields['TableId']
        data['GeograghyName'] = response.meta['met_name']
        data['GeographyId'] = response.meta['met_id']

        meta = {
            'province': response.meta['province'],
            'province_code': response.meta['province_code'],
            'met_id': response.meta['met_id'],
            'met_name': response.meta['met_name'],
            'data_type': data_type,
            'dimension_name': data_fields['dimension_name'],
            'dimension_key': data_fields['dimension_key'],
        }

        for (year, month) in available_periods:
            for dim_value in data_fields['dimension_value']:
                data['AppliedFilters[0].Value'] = dim_value
                data['ForTimePeriod.Month'] = month
                data['ForTimePeriod.Year'] = year
                body = parse.urlencode(data)
                meta['year'] = year
                meta['month'] = month
                meta['dimension_value'] = dim_value

                yield scrapy.Request(
                    self.EMBEDDED_DATA_URL,
                    body=body,
                    headers=self.HEADERS,
                    callback=self.parse_data,
                    meta=meta,
                )

    @staticmethod
    def extract_data(body):
        page = BeautifulSoup(body, 'html.parser')
        table = page.find('table', **{'class': 'CawdDataTable'})
        if table:
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

    def parse_data(self, response):
        for item in self.extract_data(response.body):
            item['province'] = response.meta['province']
            item['province_code'] = response.meta['province_code']
            item['met_id'] = response.meta['met_id']
            item['met_name'] = response.meta['met_name']
            item['data_type'] = response.meta['data_type']
            item['year'] = response.meta['year']
            item['month'] = response.meta['month']
            item['dimension_name'] = response.meta['dimension_name']
            item['dimension_value'] = response.meta['dimension_value']
            yield item

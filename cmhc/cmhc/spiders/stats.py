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
    mets_request_url = "https://www03.cmhc-schl.gc.ca/hmip-pimh/en/Navigation/MetsByProvince/"
    survey_zone_request_url = "https://www03.cmhc-schl.gc.ca/hmip-pimh/en/Navigation/SurveyZonesAndCSDsByMet/"
    data_url = "https://www03.cmhc-schl.gc.ca/hmip-pimh/en/TableMapChart/TableMatchingCriteria"
    embedded_data_url = "https://www03.cmhc-schl.gc.ca/hmip-pimh/en/TableMapChart/RenderTable"

    def __init__(self, *args, **kwargs):
        logger = logging.getLogger('scrapy.core.scraper')
        logger.setLevel(logging.WARNING)
        super().__init__(*args, **kwargs)

    def form_request(self, province, code):
        return scrapy.Request(
            self.mets_request_url + str(code),
            callback=self.mets_for_province,
            meta={'province': province, 'province_code': code}
        )

    def start_requests(self):
        return [self.form_request(province, code)
                    for province, code in province_codes().items()]

    @staticmethod
    def parse_met_data(body):
        page = BeautifulSoup(body, 'html.parser')
        cma = page.find_all('a', **{'data-type': 'MetropolitanMajorArea'})

        for node in cma:
            yield (node['data-id'], node.text)

    def survey_zone_request(self, survey_id, name, meta):
        meta['survey_zone_id'] = survey_id
        meta['survey_zone_name'] = name
        return scrapy.Request(
            self.survey_zone_request_url + str(survey_id),
            callback=self.survey_zones_for_met,
            meta=meta
        )

    def mets_for_province(self, response):
        data = self.parse_met_data(response.body)
        meta = {
            'province': response.meta['province'],
            'province_code': response.meta['province_code'],
        }

        return [self.survey_zone_request(survey_id, name, meta) for (survey_id, name) in data]

    @staticmethod
    def parse_survey_zone_data(body):
        page = BeautifulSoup(body, 'html.parser')
        surveys = page.find_all('a', **{'data-type': 'SurveyZone'})
        for node in surveys:
            yield (node['data-id'], node.text)

    def vacancy_rate_request(self, survey_id, meta):
        params = parse.urlencode({
            'GeographyType': 'SurveyZone',
            'GeographyId': survey_id,
            'CategoryLevel1': 'Primary Rental Market',
            'CategoryLevel2': 'Vacancy Rate (%)',
            'ColumnField': 2,
            'RowField': 23,
        })
        meta['data_type'] = 'Vacancy Rate (%)'

        return scrapy.FormRequest(
            self.data_url + "?" + params,
            callback=self.vacancy_data_for_survey_zone,
            meta=meta,
        )

    def survey_zones_for_met(self, response):
        data = self.parse_survey_zone_data(response.body)
        meta = {
            'province': response.meta['province'],
            'province_code': response.meta['province_code'],
            'survey_zone_id': response.meta['survey_zone_id'],
            'survey_zone_name': response.meta['survey_zone_name'],
        }

        return [self.vacancy_rate_request(survey_id, meta) for (survey_id, name) in data]

    @staticmethod
    def vacancy_rate_available_periods(body):
        page = BeautifulSoup(body, 'html.parser')
        time_periods = json.loads(page.find('input', id="serialized-model")['data-table-model'])
        for availability in time_periods['AvailableTimePeriods']:
            yield (availability['Year'], availability['Month'])

    def vacancy_data_for_survey_zone(self, response):
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
            'GeograghyName': response.meta['survey_zone_name'],
            'GeographyId': response.meta['survey_zone_id'],
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
            'survey_zone_id': response.meta['survey_zone_id'],
            'survey_zone_name': response.meta['survey_zone_name'],
            'data_type': response.meta['data_type'],
        }

        headers = {
            'Accept': 'text/html, */*; q=0.01',
            'Origin': 'https://www03.cmhc-schl.gc.ca',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://www03.cmhc-schl.gc.ca/hmiportal/en/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8',
        }

        for (year, month) in available_periods:
            data['ForTimePeriod.Month'] = month
            data['ForTimePeriod.Year'] = year
            body = parse.urlencode(data)
            meta['year'] = year
            meta['month'] = month

            yield scrapy.Request(
                self.embedded_data_url,
                body=body,
                headers=headers,
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
            item['survey_zone_id'] = response.meta['survey_zone_id']
            item['survey_zone_name'] = response.meta['survey_zone_name']
            item['data_type'] = response.meta['data_type']
            item['year'] = response.meta['year']
            item['month'] = response.meta['month']
            yield item

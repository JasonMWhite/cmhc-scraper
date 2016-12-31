from cmhc.cmhc.spiders import stats
from tests.fixtures import mets_by_province, availability_data, detailed_data
from scrapy.http import Request, HtmlResponse


def test_provinces():
    codes = stats.province_codes()
    assert codes['Ontario'] == 35
    assert len(codes) == 13


def test_start_requests():
    spider = stats.StatsSpider()
    result = spider.start_requests()
    result = sorted(result, key=lambda req: req.url)
    assert len(result) == 13
    assert result[0].url == spider.METS_REQUEST_URL + '10'
    assert result[0].method == 'GET'
    assert result[0].meta['province'] == 'Newfoundland and Labrador'
    assert result[0].meta['province_code'] == 10
    assert result[0].callback == spider.mets_for_province


def test_parse_met_data(mets_by_province):
    result = sorted([x for x in stats.StatsSpider.parse_met_data(mets_by_province)])
    assert len(result) == 5
    assert result[0] == ('1640', "St. John's")


def test_mets_for_province_callback(mets_by_province):
    spider = stats.StatsSpider()
    url = spider.METS_REQUEST_URL + '10'
    req = Request(url=url,
                  callback=spider.mets_for_province,
                  meta={'province': 'Newfoundland and Labrador', 'province_code': 10})
    res = HtmlResponse(url=url, request=req, body=mets_by_province, encoding='utf-8')
    result = spider.mets_for_province(res)
    result = sorted(result, key=lambda req: req.url)

    assert len(result) == 5
    assert 'GeographyId=1640' in result[0].url
    assert result[0].method == 'GET'
    assert result[0].callback == spider.vacancy_data_availability
    assert result[0].meta == {
        'province': 'Newfoundland and Labrador',
        'province_code': 10,
        'met_id': '1640',
        'met_name': "St. John's",
        'data_type': 'Vacancy Rate (%)',
    }


def test_vacancy_data_availability_callback(availability_data):
    spider = stats.StatsSpider()
    url = spider.DATA_URL + '1640'
    meta = {
        'province': 'Newfoundland and Labrador',
        'province_code': 10,
        'met_id': '1640',
        'met_name': "St. John's",
        'data_type': 'Vacancy Rate (%)',
    }
    req = Request(url=url,
                  callback=spider.parse_vacancy_data,
                  meta=meta)
    res = HtmlResponse(url=url, request=req, body=availability_data, encoding='utf-8')
    result = spider.vacancy_data_availability(res)
    result = sorted(result, key=lambda req: (req.meta['year'], req.meta['month']))

    assert len(result) == 36
    assert result[0].url == spider.EMBEDDED_DATA_URL
    assert 'GeographyId=1640' in result[0].body.decode('utf-8')
    assert result[0].method == 'GET'
    assert result[0].callback == spider.parse_vacancy_data
    assert result[0].meta == {
        'province': 'Newfoundland and Labrador',
        'province_code': 10,
        'met_id': '1640',
        'met_name': "St. John's",
        'data_type': 'Vacancy Rate (%)',
        'year': 1990,
        'month': 10,
    }


def test_vacancy_rate_available_periods(availability_data):
    output = stats.StatsSpider.vacancy_rate_available_periods(availability_data)
    result = sorted([x for x in output])
    assert len(result) == 36
    assert result[0] == (1990, 10)


def test_parse_vacancy_data(detailed_data):
    spider = stats.StatsSpider()
    meta = {
        'province': 'Newfoundland and Labrador',
        'province_code': 10,
        'met_id': '1640',
        'met_name': "St. John's",
        'data_type': 'Vacancy Rate (%)',
        'year': 2016,
        'month': 10,
    }

    req = Request(url=spider.EMBEDDED_DATA_URL,
                  callback=spider.parse_vacancy_data,
                  meta=meta)
    res = HtmlResponse(url=spider.EMBEDDED_DATA_URL,
                       request=req,
                       body=detailed_data,
                       encoding='utf-8')
    result = spider.parse_vacancy_data(res)
    result = sorted(result, key=lambda r: r['name'])

    assert len(result) == 37
    assert result[2] == {
        'Bachelor': None,
        '1 Bedroom': '12.0',
        '2 Bedroom': '9.1',
        '3 Bedroom +': '16.7',
        'Total': '11.3',
        'name': '0003.01',
        'province': 'Newfoundland and Labrador',
        'province_code': 10,
        'data_type': 'Vacancy Rate (%)',
        'year': 2016,
        'month': 10
    }

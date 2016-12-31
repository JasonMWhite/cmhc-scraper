from cmhc.cmhc.spiders import stats
import pytest


def test_provinces():
    codes = stats.province_codes()
    assert codes['Ontario'] == 35
    assert len(codes) == 13


@pytest.fixture()
def met():
    return """
<div class="MetropolitanMajorAreaContainer">
    <div class="option-container">
        <a href="#" title="Select this geography" class="MetropolitanMajorArea option" data-type="MetropolitanMajorArea" data-id="7253" data-type-code="3">Estevan</a>
        <a href="#" title="Add this geography to my compare list" class="add-to-compare" data-id="7253" data-type="3" data-name="Estevan"><img src="/hmip-pimh/images/compare-icon-grey.png" alt="Add this geography to my compare list"/></a>
    </div>
    <div class="option-container">
        <a href="#" title="Select this geography" class="MetropolitanMajorArea option" data-type="MetropolitanMajorArea" data-id="7433" data-type-code="3">Lloydminster</a>
        <a href="#" title="Add this geography to my compare list" class="add-to-compare" data-id="7433" data-type="3" data-name="Lloydminster"><img src="/hmip-pimh/images/compare-icon-grey.png" alt="Add this geography to my compare list"/></a>
    </div>
</div>"""


def test_parse_met_data(met):
    result = sorted([x for x in stats.StatsSpider.parse_met_data(met)])

    expected = [
        ('7253', 'Estevan'),
        ('7433', 'Lloydminster'),
    ]
    assert result == expected


@pytest.fixture()
def survey():
    return """
<div class="SurveyZoneContainer">
    <div>
        <h3>Survey Zones</h3>
    </div>
    <div class="option-container">
        <a href="#" title="Select this geography" class="SurveyZone option" data-type="SurveyZone" data-id="126504" data-type-code="5">Alta Vista</a>
        <a href="#" title="Add this geography to my compare list" class="add-to-compare" data-id="126504" data-type="5" data-name="Alta Vista"><img src="/hmip-pimh/images/compare-icon-grey.png" alt="Add this geography to my compare list"/></a>
    </div>
    <div class="option-container">
        <a href="#" title="Select this geography" class="SurveyZone option" data-type="SurveyZone" data-id="126505" data-type-code="5">Carlington/Iris</a>
        <a href="#" title="Add this geography to my compare list" class="add-to-compare" data-id="126505" data-type="5" data-name="Carlington/Iris"><img src="/hmip-pimh/images/compare-icon-grey.png" alt="Add this geography to my compare list"/></a>
    </div>
</div>
<div class="CensusSubDivisionContainer">
    <div>
        <h3>Census Subdivisions</h3>
    </div>
    <div class="option-container">
        <a href="#" title="Select this geography" class="CensusSubDivision option" data-type="CensusSubDivision" data-id="3502036" data-type-code="4">Clarence-Rockland (CY)</a>
        <a href="#" title="Add this geography to my compare list" class="add-to-compare" data-id="3502036" data-type="4" data-name="Clarence-Rockland (CY)"><img src="/hmip-pimh/images/compare-icon-grey.png" alt="Add this geography to my compare list"/></a>
    </div>
</div>
"""


def test_parse_survey_data(survey):
    result = sorted([x for x in stats.StatsSpider.parse_survey_zone_data(survey)])

    expected = [
        ('126504', 'Alta Vista'),
        ('126505', 'Carlington/Iris'),
    ]
    assert result == expected

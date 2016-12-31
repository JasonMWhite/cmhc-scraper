import pytest
from cmhc.cmhc.spiders.stats import StatsSpider


@pytest.fixture()
def data():
    return """
<div class="data-widget">
<form action="/hmip-pimh/en/TableMapChart/RenderTable" data-ajax="true" data-ajax-mode="replace" data-ajax-update="#predefinedTable-data-area" id="PredefinedTableForm" method="post"></form>
<div class="table-section">
<form action="/hmip-pimh/en/CustomTable/Export" method="post">
<table class="CawdDataTable">
<thead>
<tr> <td data-sort-key="sgc_census_tract_cde" rowspan="1"> </td>
<th colspan="2" data-sort-key="cell-1" scope="col"><span>Bachelor</span></th>
<th colspan="2" data-sort-key="cell-3" scope="col"><span>1 Bedroom</span></th>
<th colspan="2" data-sort-key="cell-5" scope="col"><span>2 Bedroom</span></th>
<th colspan="2" data-sort-key="cell-7" scope="col"><span>3 Bedroom +</span></th>
<th colspan="2" data-sort-key="cell-9" scope="col"><span>Total</span></th>
</tr>
</thead>
<tfoot>
<tr> <th scope="row">Guelph</th>
<td class="">**</td>
<td class=""></td>
<td class="numericalData">0.7</td>
<td class="">a </td>
<td class="numericalData">0.9</td>
<td class="">a </td>
<td class="numericalData">1.2</td>
<td class="">a </td>
<td class="numericalData">0.9</td>
<td class="">a </td>
</tr>
</tfoot>
<tbody>
<tr> <th class="first-cell" data-field="sgc_census_tract_cde" data-value="0" scope="row">0001.02</th>
<td class="" data-field="cell-1" data-value="">**</td>
<td class="" data-field="cell-2" data-value="**"></td>
<td class="" data-field="cell-3" data-value="">**</td>
<td class="" data-field="cell-4" data-value="**"></td>
<td class="" data-field="cell-5" data-value="">**</td>
<td class="" data-field="cell-6" data-value="**"></td>
<td class="" data-field="cell-7" data-value="">**</td>
<td class="" data-field="cell-8" data-value="**"></td>
<td class="" data-field="cell-9" data-value="">**</td>
<td class="" data-field="cell-10" data-value="**"></td>
</tr><tr> <th class="first-cell" data-field="sgc_census_tract_cde" data-value="1" scope="row">0001.03</th>
<td class="" data-field="cell-1" data-value="">**</td>
<td class="" data-field="cell-2" data-value="**"></td>
<td class="numericalData" data-field="cell-3" data-value="0.7">0.7</td>
<td class="" data-field="cell-4" data-value="a ">a </td>
<td class="numericalData" data-field="cell-5" data-value="0.7">0.7</td>
<td class="" data-field="cell-6" data-value="a ">a </td>
<td class="numericalData" data-field="cell-7" data-value="0.3">0.3</td>
<td class="" data-field="cell-8" data-value="a ">a </td>
<td class="numericalData" data-field="cell-9" data-value="0.5">0.5</td>
<td class="" data-field="cell-10" data-value="a ">a </td>
</tr><tr> <th class="first-cell" data-field="sgc_census_tract_cde" data-value="2" scope="row">0001.06</th>
<td class="" data-field="cell-1" data-value="">**</td>
<td class="" data-field="cell-2" data-value=""></td>
<td class="" data-field="cell-3" data-value="">**</td>
<td class="" data-field="cell-4" data-value=""></td>
<td class="" data-field="cell-5" data-value="">**</td>
<td class="" data-field="cell-6" data-value="**"></td>
<td class="" data-field="cell-7" data-value="">**</td>
<td class="" data-field="cell-8" data-value="**"></td>
<td class="" data-field="cell-9" data-value="">**</td>
<td class="" data-field="cell-10" data-value="**"></td>
</tr><tr> <th class="first-cell" data-field="sgc_census_tract_cde" data-value="3" scope="row">0002.00</th>
<td class="" data-field="cell-1" data-value="">**</td>
<td class="" data-field="cell-2" data-value="**"></td>
<td class="" data-field="cell-3" data-value="">**</td>
<td class="" data-field="cell-4" data-value="**"></td>
<td class="" data-field="cell-5" data-value="">**</td>
<td class="" data-field="cell-6" data-value="**"></td>
<td class="" data-field="cell-7" data-value="">**</td>
<td class="" data-field="cell-8" data-value="**"></td>
<td class="" data-field="cell-9" data-value="">**</td>
<td class="" data-field="cell-10" data-value="**"></td>
</tr><tr> <th class="first-cell" data-field="sgc_census_tract_cde" data-value="4" scope="row">0003.00</th>
<td class="" data-field="cell-1" data-value="">**</td>
<td class="" data-field="cell-2" data-value="**"></td>
<td class="numericalData" data-field="cell-3" data-value="0.0">0.0</td>
<td class="" data-field="cell-4" data-value="d ">d </td>
<td class="" data-field="cell-5" data-value="">**</td>
<td class="" data-field="cell-6" data-value="**"></td>
<td class="" data-field="cell-7" data-value="">**</td>
<td class="" data-field="cell-8" data-value="**"></td>
<td class="" data-field="cell-9" data-value="">**</td>
<td class="" data-field="cell-10" data-value="**"></td>
</tr><tr> <th class="first-cell" data-field="sgc_census_tract_cde" data-value="5" scope="row">0004.01</th>
<td class="" data-field="cell-1" data-value="">**</td>
<td class="" data-field="cell-2" data-value=""></td>
<td class="" data-field="cell-3" data-value="">**</td>
<td class="" data-field="cell-4" data-value=""></td>
<td class="" data-field="cell-5" data-value="">**</td>
<td class="" data-field="cell-6" data-value="**"></td>
<td class="" data-field="cell-7" data-value="">**</td>
<td class="" data-field="cell-8" data-value="**"></td>
<td class="" data-field="cell-9" data-value="">**</td>
<td class="" data-field="cell-10" data-value="**"></td>
</tr><tr> <th class="first-cell" data-field="sgc_census_tract_cde" data-value="6" scope="row">0004.03</th>
<td class="" data-field="cell-1" data-value="">**</td>
<td class="" data-field="cell-2" data-value=""></td>
<td class="" data-field="cell-3" data-value="">**</td>
<td class="" data-field="cell-4" data-value="**"></td>
<td class="" data-field="cell-5" data-value="">**</td>
<td class="" data-field="cell-6" data-value="**"></td>
<td class="" data-field="cell-7" data-value="">**</td>
<td class="" data-field="cell-8" data-value="**"></td>
<td class="" data-field="cell-9" data-value="">**</td>
<td class="" data-field="cell-10" data-value="**"></td>
</tr><tr> <th class="first-cell" data-field="sgc_census_tract_cde" data-value="7" scope="row">0005.00</th>
<td class="" data-field="cell-1" data-value="">**</td>
<td class="" data-field="cell-2" data-value="**"></td>
<td class="numericalData" data-field="cell-3" data-value="0.0">0.0</td>
<td class="" data-field="cell-4" data-value="d ">d </td>
<td class="numericalData" data-field="cell-5" data-value="0.0">0.0</td>
<td class="" data-field="cell-6" data-value="d ">d </td>
<td class="" data-field="cell-7" data-value="">**</td>
<td class="" data-field="cell-8" data-value="**"></td>
<td class="numericalData" data-field="cell-9" data-value="0.0">0.0</td>
<td class="" data-field="cell-10" data-value="d ">d </td>
</tr><tr> <th class="first-cell" data-field="sgc_census_tract_cde" data-value="8" scope="row">0006.00</th>
<td class="" data-field="cell-1" data-value="">**</td>
<td class="" data-field="cell-2" data-value="**"></td>
<td class="" data-field="cell-3" data-value="">**</td>
<td class="" data-field="cell-4" data-value="**"></td>
<td class="numericalData" data-field="cell-5" data-value="1.1">1.1</td>
<td class="" data-field="cell-6" data-value="a ">a </td>
<td class="" data-field="cell-7" data-value="">**</td>
<td class="" data-field="cell-8" data-value="**"></td>
<td class="numericalData" data-field="cell-9" data-value="2.9">2.9</td>
<td class="" data-field="cell-10" data-value="c ">c </td>
</tr><tr> <th class="first-cell" data-field="sgc_census_tract_cde" data-value="9" scope="row">0007.00</th>
<td class="" data-field="cell-1" data-value="">**</td>
<td class="" data-field="cell-2" data-value="**"></td>
<td class="numericalData" data-field="cell-3" data-value="0.0">0.0</td>
<td class="" data-field="cell-4" data-value="d ">d </td>
<td class="numericalData" data-field="cell-5" data-value="0.0">0.0</td>
<td class="" data-field="cell-6" data-value="c ">c </td>
<td class="numericalData" data-field="cell-7" data-value="0.0">0.0</td>
<td class="" data-field="cell-8" data-value="d ">d </td>
<td class="numericalData" data-field="cell-9" data-value="0.0">0.0</td>
<td class="" data-field="cell-10" data-value="d ">d </td>
</tr><tr> <th class="first-cell" data-field="sgc_census_tract_cde" data-value="10" scope="row">0008.00</th>
<td class="" data-field="cell-1" data-value="">**</td>
<td class="" data-field="cell-2" data-value="**"></td>
<td class="numericalData" data-field="cell-3" data-value="0.6">0.6</td>
<td class="" data-field="cell-4" data-value="a ">a </td>
<td class="numericalData" data-field="cell-5" data-value="1.0">1.0</td>
<td class="" data-field="cell-6" data-value="a ">a </td>
<td class="" data-field="cell-7" data-value="">**</td>
<td class="" data-field="cell-8" data-value="**"></td>
<td class="numericalData" data-field="cell-9" data-value="0.8">0.8</td>
<td class="" data-field="cell-10" data-value="a ">a </td>
</tr><tr> <th class="first-cell" data-field="sgc_census_tract_cde" data-value="11" scope="row">0009.03</th>
<td class="" data-field="cell-1" data-value="">**</td>
<td class="" data-field="cell-2" data-value=""></td>
<td class="" data-field="cell-3" data-value="">**</td>
<td class="" data-field="cell-4" data-value=""></td>
<td class="" data-field="cell-5" data-value="">**</td>
<td class="" data-field="cell-6" data-value="**"></td>
<td class="" data-field="cell-7" data-value="">**</td>
<td class="" data-field="cell-8" data-value="**"></td>
<td class="" data-field="cell-9" data-value="">**</td>
<td class="" data-field="cell-10" data-value="**"></td>
</tr><tr> <th class="first-cell" data-field="sgc_census_tract_cde" data-value="12" scope="row">0009.04</th>
<td class="" data-field="cell-1" data-value="">**</td>
<td class="" data-field="cell-2" data-value="**"></td>
<td class="numericalData" data-field="cell-3" data-value="0.7">0.7</td>
<td class="" data-field="cell-4" data-value="a ">a </td>
<td class="" data-field="cell-5" data-value="">**</td>
<td class="" data-field="cell-6" data-value="**"></td>
<td class="" data-field="cell-7" data-value="">**</td>
<td class="" data-field="cell-8" data-value="**"></td>
<td class="numericalData" data-field="cell-9" data-value="0.2">0.2</td>
<td class="" data-field="cell-10" data-value="a ">a </td>
</tr><tr> <th class="first-cell" data-field="sgc_census_tract_cde" data-value="13" scope="row">0010.01</th>
<td class="" data-field="cell-1" data-value="">**</td>
<td class="" data-field="cell-2" data-value="**"></td>
<td class="numericalData" data-field="cell-3" data-value="0.5">0.5</td>
<td class="" data-field="cell-4" data-value="a ">a </td>
<td class="numericalData" data-field="cell-5" data-value="0.5">0.5</td>
<td class="" data-field="cell-6" data-value="a ">a </td>
<td class="" data-field="cell-7" data-value="">**</td>
<td class="" data-field="cell-8" data-value="**"></td>
<td class="numericalData" data-field="cell-9" data-value="0.5">0.5</td>
<td class="" data-field="cell-10" data-value="a ">a </td>
</tr><tr> <th class="first-cell" data-field="sgc_census_tract_cde" data-value="14" scope="row">0010.02</th>
<td class="" data-field="cell-1" data-value="">**</td>
<td class="" data-field="cell-2" data-value="**"></td>
<td class="numericalData" data-field="cell-3" data-value="0.0">0.0</td>
<td class="" data-field="cell-4" data-value="d ">d </td>
<td class="numericalData" data-field="cell-5" data-value="0.0">0.0</td>
<td class="" data-field="cell-6" data-value="d ">d </td>
<td class="" data-field="cell-7" data-value="">**</td>
<td class="" data-field="cell-8" data-value="**"></td>
<td class="numericalData" data-field="cell-9" data-value="0.0">0.0</td>
<td class="" data-field="cell-10" data-value="d ">d </td>
</tr><tr> <th class="first-cell" data-field="sgc_census_tract_cde" data-value="15" scope="row">0011.00</th>
<td class="" data-field="cell-1" data-value="">**</td>
<td class="" data-field="cell-2" data-value="**"></td>
<td class="numericalData" data-field="cell-3" data-value="0.0">0.0</td>
<td class="" data-field="cell-4" data-value="d ">d </td>
<td class="numericalData" data-field="cell-5" data-value="0.0">0.0</td>
<td class="" data-field="cell-6" data-value="d ">d </td>
<td class="numericalData" data-field="cell-7" data-value="0.0">0.0</td>
<td class="" data-field="cell-8" data-value="a ">a </td>
<td class="numericalData" data-field="cell-9" data-value="0.0">0.0</td>
<td class="" data-field="cell-10" data-value="d ">d </td>
</tr><tr> <th class="first-cell" data-field="sgc_census_tract_cde" data-value="16" scope="row">0012.00</th>
<td class="" data-field="cell-1" data-value="">**</td>
<td class="" data-field="cell-2" data-value="**"></td>
<td class="numericalData" data-field="cell-3" data-value="0.0">0.0</td>
<td class="" data-field="cell-4" data-value="d ">d </td>
<td class="numericalData" data-field="cell-5" data-value="1.1">1.1</td>
<td class="" data-field="cell-6" data-value="d ">d </td>
<td class="" data-field="cell-7" data-value="">**</td>
<td class="" data-field="cell-8" data-value="**"></td>
<td class="numericalData" data-field="cell-9" data-value="0.7">0.7</td>
<td class="" data-field="cell-10" data-value="b ">b </td>
</tr><tr> <th class="first-cell" data-field="sgc_census_tract_cde" data-value="17" scope="row">0013.01</th>
<td class="" data-field="cell-1" data-value="">**</td>
<td class="" data-field="cell-2" data-value="**"></td>
<td class="" data-field="cell-3" data-value="">**</td>
<td class="" data-field="cell-4" data-value="**"></td>
<td class="" data-field="cell-5" data-value="">**</td>
<td class="" data-field="cell-6" data-value="**"></td>
<td class="" data-field="cell-7" data-value="">**</td>
<td class="" data-field="cell-8" data-value="**"></td>
<td class="" data-field="cell-9" data-value="">**</td>
<td class="" data-field="cell-10" data-value="**"></td>
</tr><tr> <th class="first-cell" data-field="sgc_census_tract_cde" data-value="18" scope="row">0013.02</th>
<td class="" data-field="cell-1" data-value="">**</td>
<td class="" data-field="cell-2" data-value="**"></td>
<td class="numericalData" data-field="cell-3" data-value="0.0">0.0</td>
<td class="" data-field="cell-4" data-value="d ">d </td>
<td class="numericalData" data-field="cell-5" data-value="1.1">1.1</td>
<td class="" data-field="cell-6" data-value="d ">d </td>
<td class="" data-field="cell-7" data-value="">**</td>
<td class="" data-field="cell-8" data-value="**"></td>
<td class="numericalData" data-field="cell-9" data-value="1.5">1.5</td>
<td class="" data-field="cell-10" data-value="c ">c </td>
</tr><tr> <th class="first-cell" data-field="sgc_census_tract_cde" data-value="19" scope="row">0014.00</th>
<td class="" data-field="cell-1" data-value="">**</td>
<td class="" data-field="cell-2" data-value="**"></td>
<td class="" data-field="cell-3" data-value="">**</td>
<td class="" data-field="cell-4" data-value="**"></td>
<td class="" data-field="cell-5" data-value="">**</td>
<td class="" data-field="cell-6" data-value="**"></td>
<td class="" data-field="cell-7" data-value="">**</td>
<td class="" data-field="cell-8" data-value="**"></td>
<td class="" data-field="cell-9" data-value="">**</td>
<td class="" data-field="cell-10" data-value="**"></td>
</tr><tr> <th class="first-cell" data-field="sgc_census_tract_cde" data-value="20" scope="row">0015.00</th>
<td class="" data-field="cell-1" data-value="">**</td>
<td class="" data-field="cell-2" data-value="**"></td>
<td class="numericalData" data-field="cell-3" data-value="0.0">0.0</td>
<td class="" data-field="cell-4" data-value="d ">d </td>
<td class="numericalData" data-field="cell-5" data-value="0.0">0.0</td>
<td class="" data-field="cell-6" data-value="c ">c </td>
<td class="numericalData" data-field="cell-7" data-value="0.9">0.9</td>
<td class="" data-field="cell-8" data-value="a ">a </td>
<td class="numericalData" data-field="cell-9" data-value="0.2">0.2</td>
<td class="" data-field="cell-10" data-value="b ">b </td>
</tr><tr> <th class="first-cell" data-field="sgc_census_tract_cde" data-value="21" scope="row">0100.00</th>
<td class="" data-field="cell-1" data-value="">**</td>
<td class="" data-field="cell-2" data-value=""></td>
<td class="" data-field="cell-3" data-value="">**</td>
<td class="" data-field="cell-4" data-value="**"></td>
<td class="" data-field="cell-5" data-value="">**</td>
<td class="" data-field="cell-6" data-value="**"></td>
<td class="" data-field="cell-7" data-value="">**</td>
<td class="" data-field="cell-8" data-value="**"></td>
<td class="" data-field="cell-9" data-value="">**</td>
<td class="" data-field="cell-10" data-value="**"></td>
</tr>
</tbody>
</table>
    <input type="hidden" name="exportType" id="exportType" value="pdf" />
    <input type="hidden" name="title"  value="Vacancy Rates by Bedroom Type by Zone "/>
</form></div>
"""


def test_parse_vacancy_data(data):
    result = [x for x in StatsSpider.extract_data(data)]
    result = sorted(result, key=lambda d: d['name'])
    assert len(result) == 22
    assert result[0] == {
        'name': '0001.02',
        '1 Bedroom': None,
        '2 Bedroom': None,
        '3 Bedroom +': None,
        'Bachelor': None,
        'Total': None,
    }
    assert result[1] == {
        'name': '0001.03',
        '1 Bedroom': '0.7',
        '2 Bedroom': '0.7',
        '3 Bedroom +': '0.3',
        'Bachelor': None,
        'Total': '0.5',
    }

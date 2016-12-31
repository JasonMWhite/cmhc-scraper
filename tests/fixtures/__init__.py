import pytest
from os import path


def file_to_string(filename):
    with open(path.join(path.dirname(__file__), filename), 'r') as f:
        data = f.read()
    return data


@pytest.fixture()
def mets_by_province():
    return file_to_string('MetsByProvince.html')


@pytest.fixture()
def availability_data():
    return file_to_string('AvailabilityData.html')


@pytest.fixture()
def detailed_data():
    return file_to_string('DetailedData.html')

from cmhc.cmhc.spiders import stats


def test_provinces():
    codes = stats.province_codes()
    assert 35 in codes
    assert len(codes) == 13

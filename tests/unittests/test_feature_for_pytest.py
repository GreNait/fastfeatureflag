from fastfeatureflag.feature_flag import feature_flag


@feature_flag().pytest()
def test_deactive_for_pytest():
    assert False


@feature_flag("on").pytest()
def test_active_for_pytest():
    assert True

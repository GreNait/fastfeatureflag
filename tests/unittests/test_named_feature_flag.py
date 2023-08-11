import pytest

from flaggen.feature_flag import feature_flag


def stub_func(response=True, option=None) -> bool:
    if option:
        return option

    return response


def test_name_feature():
    test_function = feature_flag(active="off", name="test")
    test_function = test_function(stub_func)

    assert test_function.feature_name == "test"

    with pytest.raises(NotImplementedError):
        test_function()

    test_function.clean()


def test_name_feature_two_methods():
    test_function = feature_flag(active="off", name="test")
    test_function = test_function(stub_func)

    assert test_function.feature_name == "test"

    test_function_2 = feature_flag(name="test")
    test_function_2 = test_function_2(stub_func)

    assert test_function_2.feature_name == "test"

    with pytest.raises(NotImplementedError):
        test_function_2()

    test_function.clean()


def test_registere_features_deactive():
    test_function = feature_flag(active="off", name="test")
    test_function = test_function(stub_func)

    assert {"name": "test", "active": "off"} in test_function.registered_features
    assert test_function.feature_active == "off"

    test_function_2 = feature_flag(name="test")
    test_function_2 = test_function_2(stub_func)

    assert test_function_2.feature_active == "off"
    assert {"name": "test", "active": "off"} in test_function_2.registered_features
    assert len(test_function.registered_features) == 1

    test_function.clean()
    test_function_2.clean()


def test_registere_features_active():
    test_function = feature_flag(active="on", name="test")
    test_function = test_function(stub_func)

    assert {"name": "test", "active": "on"} in test_function.registered_features
    assert test_function.feature_active == "on"

    test_function_2 = feature_flag(name="test")
    test_function_2 = test_function_2(stub_func)

    assert test_function_2.feature_active == "on"
    assert {"name": "test", "active": "on"} in test_function_2.registered_features
    assert len(test_function.registered_features) == 1

    test_function.clean()
    test_function_2.clean()


def test_name_feature_two_methods_active():
    test_function = feature_flag(active="on", name="test")
    test_function = test_function(stub_func)

    test_function_2 = feature_flag(name="test")
    test_function_2 = test_function_2(stub_func)

    assert test_function()
    assert test_function_2()

    test_function.clean()
    test_function_2.clean()


def test_two_different_feature_names():
    test_function = feature_flag(active="on", name="test")
    test_function = test_function(stub_func)

    test_function_2 = feature_flag(name="test2")
    test_function_2 = test_function_2(stub_func)

    assert test_function.feature_name == "test"
    assert test_function.feature_active == "on"
    assert test_function_2.feature_name == "test2"
    assert test_function_2.feature_active == "off"
    assert len(test_function_2.registered_features) == 2

    test_function.clean()
    test_function_2.clean()

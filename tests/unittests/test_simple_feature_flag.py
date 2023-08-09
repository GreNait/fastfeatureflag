import pytest

from flaggen.feature_flag import feature_flag


def stub_func(response=True, option=None) -> bool:
    if option:
        return option

    return response


def test_call_with_off():
    with pytest.raises(NotImplementedError):
        test_function = feature_flag(active="off")
        test_function = test_function(stub_func)
        test_function()


def test_call_with_on():
    test_function = feature_flag(active="on")
    test_function = test_function(stub_func)
    assert test_function() is True


def test_call_empty():
    with pytest.raises(NotImplementedError):
        test_function = feature_flag()
        test_function = test_function(stub_func)
        test_function()


def test_call_with_wrong_keyword():
    with pytest.raises(KeyError):
        test_function = feature_flag(active="WrongKeyword")
        test_function = test_function(stub_func)
        test_function()


def test_call_with_option():
    option = "option_on"
    test_function = feature_flag(active="on", option=option)
    test_function = test_function(stub_func)
    assert test_function() == option


def test_as_decorator():
    @feature_flag(active="off")
    def stub_function_decorated():
        return True

    with pytest.raises(NotImplementedError):
        stub_function_decorated()


def test_call_with_response_but_deactivated_feature():
    response = "answer"
    test_function = feature_flag(active="off", response=response)
    test_function = test_function(stub_func)
    assert test_function() == response

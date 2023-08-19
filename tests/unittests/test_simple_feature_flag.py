import pytest

from flaggen.feature_flag import feature_flag


def test_call_with_off(decorated_stub):
    test_function = feature_flag(activation="off")
    test_function = test_function(decorated_stub)

    with pytest.raises(NotImplementedError):
        test_function()


def test_call_with_on(decorated_stub):
    test_function = feature_flag(activation="on")
    test_function = test_function(decorated_stub)
    assert test_function() is True


def test_call_empty(decorated_stub):
    test_function = feature_flag()
    test_function = test_function(decorated_stub)

    with pytest.raises(NotImplementedError):
        test_function()


def test_call_with_wrong_keyword(decorated_stub):
    test_function = feature_flag(activation="WrongKeyword")
    test_function = test_function(decorated_stub)

    with pytest.raises(KeyError):
        test_function()


def test_call_with_option(decorated_stub):
    option = "option_on"
    test_function = feature_flag(activation="on", option=option)
    test_function = test_function(decorated_stub)
    assert test_function() == option


def test_call_without_parameter():
    @feature_flag()
    def test_function():
        return True

    with pytest.raises(NotImplementedError):
        test_function()


def test_as_decorator(decorated_stub):
    @feature_flag(activation="off")
    def stub_function_decorated():
        return True

    with pytest.raises(NotImplementedError):
        stub_function_decorated()


def test_call_with_response_but_deactivated_feature(decorated_stub):
    response = "answer"
    test_function = feature_flag(activation="off", response=response)
    test_function = test_function(decorated_stub)
    assert test_function() == response


def test_feature_active(decorated_stub):
    test_function = feature_flag(activation="off")
    test_function = test_function(decorated_stub)
    assert test_function.feature_active == "off"

    test_function = feature_flag(activation="on")
    test_function = test_function(decorated_stub)
    assert test_function.feature_active == "on"

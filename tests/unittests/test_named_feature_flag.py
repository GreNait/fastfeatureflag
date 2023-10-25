from urllib import response

import pytest

from fastfeatureflag.feature_content import FeatureContent
from fastfeatureflag.feature_flag import feature_flag


def test_name_feature(decorated_stub):
    test_function = feature_flag(activation="off", name="test")
    test_function = test_function(decorated_stub)

    assert test_function.feature.name == "test"

    with pytest.raises(NotImplementedError):
        test_function()

    test_function.clean()


def test_name_feature_two_methods(decorated_stub):
    test_function = feature_flag(activation="off", name="test")
    test_function = test_function(decorated_stub)

    test_function_2 = feature_flag(name="test")
    test_function_2 = test_function_2(decorated_stub)

    assert test_function_2.feature.name == "test"

    with pytest.raises(NotImplementedError):
        test_function_2()

    test_function.clean()
    test_function_2.clean()


def test_registere_features_deactive(decorated_stub):
    test_function = feature_flag(activation="off", name="test")
    test_function = test_function(None)

    assert (
        FeatureContent(**{"name": "test", "activation": "off"})
        in test_function.registered_features
    )
    assert test_function.feature.activation == "off"

    test_function_2 = feature_flag(name="test")
    test_function_2 = test_function_2(None)

    assert test_function_2.feature.activation == "off"
    assert (
        FeatureContent(**{"name": "test", "activation": "off"})
        in test_function_2.registered_features
    )
    assert len(test_function.registered_features) == 1

    test_function.clean()
    test_function_2.clean()


def test_registere_features_active(decorated_stub):
    test_function = feature_flag(activation="on", name="test")
    test_function = test_function(None)

    assert (
        FeatureContent(**{"name": "test", "activation": "on"})
        in test_function.registered_features
    )
    assert test_function.feature.activation == "on"

    test_function_2 = feature_flag(name="test")
    test_function_2 = test_function_2(None)

    assert test_function_2.feature.activation == "on"
    assert (
        FeatureContent(**{"name": "test", "activation": "on"})
        in test_function_2.registered_features
    )
    assert len(test_function.registered_features) == 1

    test_function.clean()
    test_function_2.clean()


def test_name_feature_two_methods_active(decorated_stub):
    test_function = feature_flag(activation="on", name="test")
    test_function = test_function(decorated_stub)

    test_function_2 = feature_flag(name="test")
    test_function_2 = test_function_2(decorated_stub)

    assert test_function()
    assert test_function_2()

    test_function.clean()
    test_function_2.clean()


def test_two_different_feature_names(decorated_stub):
    test_function = feature_flag(activation="on", name="test")
    test_function = test_function(decorated_stub)

    test_function_2 = feature_flag(name="test2")
    test_function_2 = test_function_2(decorated_stub)

    assert test_function.feature.name == "test"
    assert test_function.feature.activation == "on"
    assert test_function_2.feature.name == "test2"
    assert test_function_2.feature.activation == "off"
    assert len(test_function_2.registered_features) == 2

    test_function.clean()
    test_function_2.clean()


def test_two_methods_one_feature_as_decorator():
    @feature_flag("off", name="test")
    def test_method_1():
        return True

    @feature_flag(name="test")
    def test_method_2():
        return True

    assert test_method_1.feature.activation == "off"
    assert test_method_2.feature.activation == "off"
    assert len(test_method_2.registered_features) == 1

    with pytest.raises(NotImplementedError):
        test_method_1()

    with pytest.raises(NotImplementedError):
        test_method_2()

    test_method_1.clean()
    test_method_2.clean()


def test_two_methods_one_feature_as_decorator_active():
    @feature_flag("on", name="test")
    def test_method_1():
        return True

    @feature_flag(name="test")
    def test_method_2():
        return True

    assert test_method_1.feature.activation == "on"
    assert test_method_2.feature.activation == "on"
    assert len(test_method_2.registered_features) == 1

    assert test_method_1()
    assert test_method_2()

    test_method_1.clean()
    test_method_2.clean()


def test_two_methods_two_feature_as_decorator():
    @feature_flag("off", name="test")
    def test_method_1():
        return True

    @feature_flag(name="test2")
    def test_method_2():
        return True

    assert test_method_1.feature.activation == "off"
    assert test_method_2.feature.activation == "off"
    assert len(test_method_2.registered_features) == 2

    with pytest.raises(NotImplementedError):
        test_method_1()

    with pytest.raises(NotImplementedError):
        test_method_2()

    test_method_1.clean()
    test_method_2.clean()


def test_two_methods_one_feature_single_response():
    @feature_flag("off", name="test", response="test_method_1")
    def test_method_1():
        return True

    @feature_flag(name="test")
    def test_method_2():
        return True

    assert test_method_1() == "test_method_1"

    with pytest.raises(NotImplementedError):
        test_method_2()

    test_method_1.clean()
    test_method_2.clean()


def test_two_methods_one_feature_both_response():
    @feature_flag("off", name="test", response="test_method_1")
    def test_method_1():
        return True

    @feature_flag(name="test", response="test_method_2")
    def test_method_2():
        return True

    assert test_method_1() == "test_method_1"
    assert test_method_2() == "test_method_2"

    test_method_1.clean()
    test_method_2.clean()


def test_update_feature():
    @feature_flag("off", name="test", response="test_method_1")
    def test_method_1():
        return True

    assert test_method_1() == "test_method_1"

    test_method_1.update(activation="off", name="test", response="re-configured")
    assert test_method_1() == "re-configured"

    test_method_1.clean()

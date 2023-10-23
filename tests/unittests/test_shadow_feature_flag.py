import pytest

from fastfeatureflag.config import TestConfig
from fastfeatureflag.errors import CannotRunShadowWithoutFunctionError
from fastfeatureflag.feature_flag import feature_flag


def original_method():
    return "original"


def alternative_method():
    return "alternative_method"


def alternative_method_with_arguments(argument_one: str):
    return f"alternative_method_{argument_one}"


def test_call_shadow():
    assert callable(feature_flag().shadow)


def test_shadow_run_method():
    test_function = feature_flag().shadow(run=alternative_method)
    test_function = test_function(original_method)

    assert test_function() == "alternative_method"


def test_shadow_run_method_with_arguments():
    test_function = feature_flag().shadow(
        alternative_method_with_arguments, "the_argument_one"
    )
    test_function = test_function(original_method)
    assert test_function() == "alternative_method_the_argument_one"

    test_function = feature_flag().shadow(
        run=alternative_method_with_arguments, argument_one="the_argument_one"
    )
    test_function = test_function(original_method)
    assert test_function() == "alternative_method_the_argument_one"


def test_shadow_run_empty_method():
    with pytest.raises(CannotRunShadowWithoutFunctionError):
        test_function = feature_flag().shadow(run=None)


def test_shadow_run_bad_method():
    test: int = 5  # not a function
    with pytest.raises(CannotRunShadowWithoutFunctionError):
        test_function = feature_flag().shadow(run=test)


def test_shadow_run_method_as_decorator():
    def alternative_method():
        return "alternative_method"

    @feature_flag().shadow(run=alternative_method)
    def original_method():
        return "original"

    assert original_method() == "alternative_method"


def test_shadow_run_method_by_string():
    test_function = feature_flag().shadow(
        run="tests.unittests.test_shadow_feature_flag.alternative_method"
    )
    test_function = test_function(original_method)

    assert test_function() == "alternative_method"


def test_shadow_run_bad_method_by_string():
    with pytest.raises(AttributeError):
        test_function = feature_flag().shadow(
            run="tests.unittests.test_shadow_feature_flag.not_existing_alternative_method"
        )

    test = "not a module"
    with pytest.raises(ValueError):
        test_function = feature_flag().shadow(run=test)


def test_shadow_run_deactivated():
    test_function = feature_flag("off").shadow(
        run="tests.unittests.test_shadow_feature_flag.alternative_method"
    )
    test_function = test_function(original_method)
    assert test_function() == "alternative_method"

    test_function = feature_flag("on").shadow(
        run="tests.unittests.test_shadow_feature_flag.alternative_method"
    )
    test_function = test_function(original_method)
    assert test_function() == "original"


def test_shadow_run_method_by_config_file():
    test_function = feature_flag(
        name="test_shadow_method", configuration=TestConfig().DEFAULT_CONFIG
    )
    test_function = test_function(original_method)
    assert test_function.configuration == TestConfig().DEFAULT_CONFIG
    assert test_function() == "shadow"

    test_function.clean()


def test_shadow_as_decorator():
    def shadow_method():
        return "replacement"

    @feature_flag().shadow(run=shadow_method)
    def original_method():
        return "original_method"

    assert original_method() == "replacement"


def test_shadow_as_decorator_deactivated():
    def shadow_method():
        return "replacement"

    @feature_flag("on").shadow(run=shadow_method)
    def original_method():
        return "original_method"

    assert original_method() == "original_method"


def test_shadow_as_decorator_with_configuration():
    @feature_flag(
        "off", name="test_shadow_method", configuration=TestConfig().DEFAULT_CONFIG
    )
    def original_method():
        return "original_method"

    assert original_method() == "shadow"

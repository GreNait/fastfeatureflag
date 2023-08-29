import os
import pathlib
import sys

import pytest
import toml
from behave import given, then, when
from behave.__main__ import main as behave_main

from fastfeatureflag.feature_flag import feature_flag

FEATURE_CONFIG_PATH = pathlib.Path.cwd() / "features" / "steps" / "feature_config.toml"


def method_a():
    return "method a"


def method_c():
    return "method c"


def method_b():
    return "method b"


# Background: Configuration file and methods


@given(
    "there is a configuration file containing feature flag 'feature_method_a', 'feature_method_b' and 'feature_method_c'"
)
def given_config_file(context):
    configuration = toml.load(FEATURE_CONFIG_PATH)
    assert "feature_method_a" in configuration
    assert "feature_method_b" in configuration
    assert "feature_method_c" in configuration
    context.configuration = configuration


@given("'feature_method_a' contains the activation 'on'")
def given_feature_method_a(context):
    assert context.configuration.get("feature_method_a").get("activation") == "on"


@given("'feature_method_b' contains the activation 'off'")
def given_feature_method_b(context):
    assert context.configuration.get("feature_method_b").get("activation") == "off"


@given("'feature_method_c' contains the activation 'FEATURE_METHOD_C'")
def given_feature_method_c(context):
    assert (
        context.configuration.get("feature_method_c").get("activation")
        == "FEATURE_METHOD_C"
    )


@given("there is a method_a which returns 'method a'")
def given_method_a(context):
    assert method_a() == "method a"


@given("there is a method_b which returns 'method b'")
def given_method_b(context):
    assert method_b() == "method b"


@given("there is a method_c which returns 'method c'")
def given_method_c(context):
    assert method_c() == "method c"


# Scenario: Load active feature by configuration


@when("method_a gets the flag feature_flag(name='feature_method_a')")
def when_method_a(context):
    decorated_method_a = feature_flag(
        name="feature_method_a", configuration=context.configuration
    )
    decorated_method_a = decorated_method_a(method_a)
    context.decorated_method_a = decorated_method_a


@then("when method_a is called it returns 'method a'")
def then_when_method_a(context):
    assert context.decorated_method_a() == "method a"


# Scenario: Load inactive feature by configuration


@when("method_b gets the flag feature_flag(name='feature_method_b')")
def when_method_b(context):
    decorated_method_b = feature_flag(
        name="feature_method_b", configuration=context.configuration
    )
    decorated_method_b = decorated_method_b(method_b)
    context.decorated_method_b = decorated_method_b


@then("when method_b is called it raises a NotImplementedError")
def then_when_method_b(context):
    with pytest.raises(NotImplementedError):
        context.decorated_method_b()


# Scenario: Overrule feature flag activation by configuration


@when("method_a gets the flag feature_flag('off', name='feature_method_a')")
def when_method_a_off(context):
    decorated_method_a = feature_flag(
        "off", name="feature_method_a", configuration=context.configuration
    )
    decorated_method_a = decorated_method_a(method_a)
    context.decorated_method_a = decorated_method_a


@then("when overruled method_a is called it returns 'method a'")
def then_when_method_a_overruled(context):
    assert context.decorated_method_a() == "method a"


# Scenario: Activate feature by environment variable


@when("the environment variable 'FEATURE_METHOD_C' contains 'on'")
def when_the_environment(context):
    os.environ["FEATURE_METHOD_C"] = "on"
    assert os.getenv("FEATURE_METHOD_C") == "on"


@then("when method_c gets the flag feature_flag(name='feature_method_c')")
def then_when_method_c(context):
    decorated_method_c = feature_flag(
        "off", name="feature_method_c", configuration=context.configuration
    )
    decorated_method_c = decorated_method_c(method_c)
    context.decorated_method_c = decorated_method_c


@then("when method_c is called it returns 'method c'")
def then_when_method_c_called(context):
    assert context.decorated_method_c() == "method c"


# Scenario: Inactive feature by environment variable


@when("the environment variable 'FEATURE_METHOD_C' contains 'off'")
def when_the_environment_off(context):
    os.environ["FEATURE_METHOD_C"] = "off"
    assert os.getenv("FEATURE_METHOD_C") == "off"


@then("when inactive method_c gets the flag feature_flag(name='feature_method_c')")
def then_when_method_c_deactivated(context):
    decorated_method_c = feature_flag(
        "off", name="feature_method_c", configuration=context.configuration
    )
    decorated_method_c = decorated_method_c(method_c)
    context.decorated_method_c = decorated_method_c


@then("when method_c is called it raises NotImplementedError")
def then_when_method_c_called_raise_exception(context):
    with pytest.raises(NotImplementedError):
        context.decorated_method_c()


if __name__ == "__main__":
    sys.exit(behave_main())

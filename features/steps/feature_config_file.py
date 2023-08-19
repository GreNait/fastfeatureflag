import pathlib
import sys

import pytest
import toml
from behave import given, then, when
from behave.__main__ import main as behave_main

from flaggen.feature_flag import feature_flag

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


@given("feature_method_a' contains the activation 'on'")
def given_feature_method_a(context):
    pass


@given("'feature_method_b' contains the activation 'off'")
def given_feature_method_b(context):
    pass


@given("'feature_method_c' contains the activation 'FEATURE_METHOD_C'")
def given_feature_method_c(context):
    pass


@given("there is a method_a which returns 'method a'")
def given_method_a(context):
    pass


@given("there is a method_b which returns 'method b'")
def given_method_b(context):
    pass


@given("there is a method_c which returns 'method c'")
def given_method_c(context):
    pass


# Scenario: Load active feature by configuration


@when("method_a gets the flag feature_flag(name='feature_method_a')")
def when_method_a(context):
    pass


@then("when method_a is called it returns 'method a'")
def then_when_method_a(context):
    pass


# Scenario: Load inactive feature by configuration


@when("method_b gets the flag feature_flag(name='feature_method_b')")
def when_method_b(context):
    pass


@then("when method_b is called it raises a NotImplementedError")
def then_when_method_b(context):
    pass


# Scenario: Overrule feature flag activation by configuration


@when("method_a gets the flag feature_flag('off', name='feature_method_a')")
def when_method_a_off(context):
    pass


@then("when overruled method_a is called it returns 'method a'")
def then_when_method_a_overruled(context):
    pass


# Scenario: Activate feature by environment variable


@when("the environment variable 'FEATURE_METHOD_C' contains 'on'")
def when_the_environment(context):
    pass


@then("when method_c gets the flag feature_flag(name='feature_method_c')")
def then_when_method_c(context):
    pass


@then("when method_c is called it returns 'method c'")
def then_when_method_c_called(context):
    pass


# Scenario: Inactive feature by environment variable


@when("the environment variable 'FEATURE_METHOD_C' contains 'off'")
def when_the_environment_off(context):
    pass


@then("when inactive method_c gets the flag feature_flag(name='feature_method_c')")
def then_when_method_c_deactivated(context):
    pass


@then("when method_c is called it raises NotImplementedError")
def then_when_method_c_called_raise_exception(context):
    pass


if __name__ == "__main__":
    sys.exit(behave_main())

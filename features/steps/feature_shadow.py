import sys

import pytest
from behave import given, then, when
from behave.__main__ import main as behave_main

from fastfeatureflag.feature_flag import feature_flag


class TestShadow:
    def method_old(self, ingoing: str):
        return ingoing

    def method_new(self, *args, **kwargs):
        raise Exception("new_method exception")


# Background: Class with several methods is available


@given("there is a class with a method_old and takes an string as an input")
def step_impl(context):
    test_class = TestShadow()
    assert callable(test_class.method_old)
    context.test_class = test_class


@given("that the method_old returns the input string when called")
def step_impl(context):
    assert context.test_class.method_old("test") == "test"


@given("in this class is a method_new with arbitrary arguments")
def step_impl(context):
    assert callable(context.test_class.method_new)


@given("that method_new raises a exception when directly called")
def step_impl(context):
    with pytest.raises(Exception):
        context.test_class.new_method()


# Scenario: Flagging the method_new as a shadow function


@when("method_new gets the flag feature_flag.shadow(run=method_old)")
def step_impl(context):
    decorated_method_new = feature_flag.shadow(run=context.method_old)
    decorated_method_new = decorated_method_new(context.method_new)
    context.decorated_method_new = decorated_method_new


@then("when method_new is called with an input string it returns the input string")
def step_impl(context):
    assert context.decorated_method_new("test") == "test"


if __name__ == "__main__":
    sys.exit(behave_main())

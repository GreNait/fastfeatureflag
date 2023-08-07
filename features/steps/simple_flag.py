import sys

import pytest
from behave import given, then, when
from behave.__main__ import main as behave_main

from pyflag.feature_flag import feature_flag


@given("There is a method called disable")
def step_given_method(context):
    def disable():
        pass

    context.disable_method = disable


@when("a feature flag feature.flag('off') is added")
def step_when_flag(context):
    test_function = feature_flag(active="off")
    test_function = test_function(context.disable_method)
    context.decorated_method = test_function


@then("if I try to call the method a 'NotImplementedError' exception is raised")
def step_then_return(context):
    with pytest.raises(NotImplementedError) as caught_exception:
        context.decorated_method()
    # assert caught_exception.typename == "NotImplementedError"


@when('a feature flag feature.flag("off", response="{response_in}") is added')
def step_feature_flag_with_response(context, response_in):
    test_function = feature_flag(active="off", response=response_in)
    test_function = test_function(context.disable_method)
    context.decorated_method = test_function


@then('if I call the method it returns "{response_out}"')
def step_feate_flag_response(context, response_out):
    assert context.decorated_method() == response_out


if __name__ == "__main__":
    sys.exit(behave_main())

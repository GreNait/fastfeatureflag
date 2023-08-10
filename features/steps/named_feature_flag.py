import sys

import pytest
from behave import given, then, when
from behave.__main__ import main as behave_main

from flaggen.feature_flag import feature_flag


def method_a():
    return "method a"


def method_b():
    return "method b"


# Background


@given("There is a method called method_a which returns 'method a'")
def given_method_a(context):
    assert method_a() == "method a"


@given("There is a method called method_b which returns 'method b'")
def given_method_b(context):
    assert method_b() == "method b"


# Scenario: Provide a name and deactivate feature


@when(
    "a feature flag contains a name and is added with feature.flag('off', name='not_working_feature') to method_a"
)
def when_name(context):
    decorated_method_a = feature_flag("off", name="not_working_feature")
    decorated_method_a = decorated_method_a(method_a())
    context.decorated_method_a = decorated_method_a


@then(
    "if a feature flag is added to method_b with feature.flag(name='not_working_feature')"
)
def then_flag_added(context):
    decorated_method_b = feature_flag(name="not_working_feature")
    decorated_method_b = decorated_method_b(method_b())
    context.decorated_method_b = decorated_method_b


@then("if method_b is called a 'NotImplementedError' exception is raised")
def then_exception_raised(context):
    with pytest.raises(NotImplementedError):
        context.decorated_method_b()


# Scenario: Activate a named feature


@given("that method_a has been flagged with feature.flag('on', name='be_activated')")
def given_method_a_flagged(context):
    decorated_method_a = feature_flag("on", name="be_activated")
    decorated_method_a = decorated_method_a(method_a())
    context.decorated_method_a = decorated_method_a


@given("that method_b has been flagged with feature.flag(name='be_activated')")
def given_method_b_flagged(context):
    decorated_method_b = feature_flag(name="be_activated")
    decorated_method_b = decorated_method_b(method_b())
    context.decorated_method_b = decorated_method_b


@when("method_a is called and returns 'method_a'")
def when_method_a_called(context):
    assert context.decorated_method_a() == "method a"


@then("method_b is called it returns 'method b'")
def then_method_b_called(context):
    assert context.decorated_method_b() == "method b"


# Scenario: Deactivated method with response only with method a


@given(
    "that method_a has been flagged with feature.flag('off', name='deactivated_with_response', response='I am method a')"
)
def given_method_a_flagged_with_response(context):
    decorated_method_a = feature_flag(
        "off", name="deactivated_with_response", response="I am method a"
    )

    decorated_method_a = decorated_method_a(method_a())
    context.decorated_method_a = decorated_method_a


@given("that method_b has been flagged with feature.flag(name='be_activated')")
def given_method_b_flagged_no_response(context):
    decorated_method_b = feature_flag(name="be_activated")
    decorated_method_b = decorated_method_b(method_b())
    context.decorated_method_b = decorated_method_b


@when("method_a is called and returns 'method_a'")
def when_method_a_called_with_response(context):
    assert context.decorated_method_a() == "I am method a"


@then("method_b is called it returns 'method b'")
def then_method_b_called_no_response(context):
    with pytest.raises(NotImplementedError):
        context.decorated_method_b()


# Scenario: Deactivated method with response with both methods


@given(
    "that method_a has been flagged with feature.flag('off', name='deactivated_with_response', response='I am method a')"
)
def given_method_a_flagged_both_response(context):
    decorated_method_a = feature_flag(
        "off", name="deactivated_with_response", response="I am method a"
    )

    decorated_method_a = decorated_method_a(method_a())
    context.decorated_method_a = decorated_method_a


@given(
    "that method_b has been flagged with feature.flag(name='deactivated_with_response', name='I am method b')"
)
def given_method_b_flagged_response(context):
    decorated_method_b = feature_flag(name="be_activated", response="I am method b")
    decorated_method_b = decorated_method_b(method_b())
    context.decorated_method_b = decorated_method_b


@when("method_a is called and returns 'method_a'")
def when_method_a_called_both_response(context):
    assert context.decorated_method_a() == "I am method a"


@then("method_b is called and returns 'I am method b'")
def then_method_b_called_with_response(context):
    assert context.decorated_method_a() == "I am method b"


if __name__ == "__main__":
    sys.exit(behave_main())

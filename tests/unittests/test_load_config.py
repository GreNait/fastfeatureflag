import os
import pathlib

import pytest
import toml

from fastfeatureflag.config import TestConfig
from fastfeatureflag.errors import WrongFeatureSchema
from fastfeatureflag.feature_content import FeatureContent
from fastfeatureflag.feature_flag import feature_flag


def test_load_config_by_dict(decorated_stub):
    test_function = feature_flag(
        name="test_feature_off", configuration=TestConfig().DEFAULT_CONFIG
    )
    test_function = test_function(decorated_stub)

    assert test_function.configuration == TestConfig().DEFAULT_CONFIG

    test_function.clean()


def test_update_config_by_dict(decorated_stub):
    updated_config = dict(
        TestConfig().DEFAULT_CONFIG, **{"test_feature_update": {"activation": "off"}}
    )

    test_function = feature_flag(
        name="test_feature_off", configuration=TestConfig().DEFAULT_CONFIG
    )
    test_function = test_function(decorated_stub)

    assert test_function.configuration == TestConfig().DEFAULT_CONFIG
    test_function.configuration = updated_config

    assert test_function.configuration != TestConfig().DEFAULT_CONFIG
    assert test_function.configuration == updated_config

    test_function.clean()


def test_load_config_by_file(decorated_stub):
    test_function = feature_flag(
        name="test_feature_off", configuration_path=TestConfig().PATH_TO_CONFIGURATION
    )
    test_function = test_function(decorated_stub)
    assert (
        test_function.feature.configuration_path == TestConfig().PATH_TO_CONFIGURATION
    )
    assert test_function.feature.configuration == TestConfig().DEFAULT_CONFIG

    test_function.clean()


def test_update_config_by_file(decorated_stub):
    test_function = feature_flag(name="test_feature_off")
    test_function = test_function(decorated_stub)
    assert test_function.feature.configuration is None

    test_function.configuration_path = TestConfig().PATH_TO_CONFIGURATION
    assert (
        test_function.feature.configuration_path == TestConfig().PATH_TO_CONFIGURATION
    )
    assert test_function.feature.configuration == TestConfig().DEFAULT_CONFIG

    test_function.clean()


def test_load_config_by_default_file(decorated_stub, default_config):
    default_config_path = default_config
    test_function = feature_flag(
        name="test_feature_off", configuration_path=default_config_path
    )
    test_function = test_function(decorated_stub)
    assert test_function.configuration == TestConfig().DEFAULT_CONFIG

    test_function.clean()


def test_no_valid_path_to_config(decorated_stub):
    with pytest.raises(FileNotFoundError):
        test_function = feature_flag(
            name="test_feature_off", configuration_path=pathlib.Path("does/not/exist")
        )
        test_function = test_function(decorated_stub)
        test_function.clean()


def test_register_feature_from_config(decorated_stub):
    test_function = feature_flag(
        name="test_feature_off", configuration=TestConfig().DEFAULT_CONFIG
    )
    test_function = test_function(None)

    assert len(test_function.registered_features) == 4
    assert (
        FeatureContent(**{"name": "test_feature_off", "activation": "off"})
        in test_function.registered_features
    )

    test_function.clean()


def test_register_feature_from_config_file(decorated_stub, default_config):
    default_config_path = default_config
    test_function = feature_flag(
        name="test_feature_off", configuration_path=default_config_path
    )

    test_function = test_function(decorated_stub)
    assert len(test_function.registered_features) == 4
    assert test_function.get_feature_by_name("test_feature_off")

    test_function.clean()


def test_register_feature_with_setting_new_config(decorated_stub):
    test_function = feature_flag(name="test_feature_off")
    test_function = test_function(decorated_stub)

    assert len(test_function.registered_features) == 1
    assert test_function.get_feature_by_name("test_feature_off")

    test_function.configuration = TestConfig().DEFAULT_CONFIG
    assert len(test_function.registered_features) == 4

    test_function.clean()


def test_use_activation_from_config_on_method(decorated_stub):
    test_function = feature_flag(
        name="test_feature_on", configuration=TestConfig().DEFAULT_CONFIG
    )
    test_function = test_function(decorated_stub)

    assert test_function() is True

    test_function.clean()


def test_override_not_config_activation(decorated_stub):
    test_function = feature_flag(
        activation="on",
        name="test_feature_off",
        configuration=TestConfig().DEFAULT_CONFIG,
    )
    test_function = test_function(decorated_stub)

    with pytest.raises(NotImplementedError):
        test_function()

    test_function.clean()


def test_use_environment_variable_activation(decorated_stub):
    os.environ["TEST_ACTIVATION"] = "off"

    test_function = feature_flag(
        name="test_feature_environment", configuration=TestConfig().DEFAULT_CONFIG
    )
    test_function = test_function(decorated_stub)

    with pytest.raises(NotImplementedError):
        test_function()

    test_function.clean()

    os.environ["TEST_ACTIVATION"] = "on"

    test_function = feature_flag(
        name="test_feature_environment", configuration=TestConfig().DEFAULT_CONFIG
    )
    test_function = test_function(decorated_stub)

    assert test_function() is True

    test_function.clean()


def test_wrong_keywords_value_in_config(decorated_stub):
    config = dict(
        **{"feature_key_value_wrong": {"activation": "wrong_value"}},
        **TestConfig().DEFAULT_CONFIG
    )
    test_function = feature_flag(name="feature_key_value_wrong", configuration=config)
    test_function = test_function(decorated_stub)

    with pytest.raises(KeyError):
        test_function()

    test_function.clean()


def test_config_has_wrong_schema(decorated_stub):
    with pytest.raises(WrongFeatureSchema):
        test_function = feature_flag(
            name="wrong_schema", configuration=TestConfig().WRONG_SCHEMA
        )
        test_function = test_function(decorated_stub)


def test_reconfiguration(decorated_stub):
    @feature_flag(name="test_reconfiguration", response="I am deactivated")
    def broken_feature():
        return "I am broken"

    assert broken_feature() == "I am deactivated"

    broken_feature.configuration = {
        "test_reconfiguration": {"activation": "off", "response": "I am re-configured"}
    }
    assert broken_feature() == "I am re-configured"
    assert broken_feature.configuration == {
        "test_reconfiguration": {"activation": "off", "response": "I am re-configured"}
    }

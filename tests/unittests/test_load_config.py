import os
import pathlib

import pytest
import toml

from flaggen.config import TestConfig
from flaggen.errors import WrongFeatureSchema
from flaggen.feature_flag import feature_flag
from flaggen.feature_schema import Feature


def create_default_config():
    with TestConfig().PATH_TO_DEFAULT_CONFIGURATION.open("w") as file:
        toml.dump(TestConfig().DEFAULT_CONFIG, file)

    yield TestConfig().PATH_TO_DEFAULT_CONFIGURATION, TestConfig().DEFAULT_CONFIG

    TestConfig().PATH_TO_DEFAULT_CONFIGURATION.unlink()


def stub_func(response=True, option=None) -> bool:
    if option:
        return option

    return response


def test_load_config_by_dict():
    test_function = feature_flag(
        name="test_feature_off", configuration=TestConfig().DEFAULT_CONFIG
    )
    test_function = test_function(stub_func)

    assert test_function.configuration == TestConfig().DEFAULT_CONFIG

    test_function.clean()


def test_update_config_by_dict():
    updated_config = dict(
        TestConfig().DEFAULT_CONFIG, **{"test_feature_update": {"activation": "off"}}
    )

    test_function = feature_flag(
        name="test_feature_off", configuration=TestConfig().DEFAULT_CONFIG
    )
    test_function = test_function(stub_func)

    assert test_function.configuration == TestConfig().DEFAULT_CONFIG
    test_function.configuration = updated_config

    assert test_function.configuration != TestConfig().DEFAULT_CONFIG
    assert test_function.configuration == updated_config

    test_function.clean()


def test_load_config_by_file():
    test_function = feature_flag(
        name="test_feature_off", configuration_path=TestConfig().PATH_TO_CONFIGURATION
    )
    test_function = test_function(stub_func)
    assert test_function.configuration_path == TestConfig().PATH_TO_CONFIGURATION
    assert test_function.configuration == TestConfig().DEFAULT_CONFIG

    test_function.clean()


def test_update_config_by_file():
    test_function = feature_flag(name="test_feature_off")
    test_function = test_function(stub_func)
    assert test_function.configuration is None

    test_function.configuration_path = TestConfig().PATH_TO_CONFIGURATION
    assert test_function.configuration_path == TestConfig().PATH_TO_CONFIGURATION
    assert test_function.configuration == TestConfig().DEFAULT_CONFIG

    test_function.clean()


def test_load_config_by_default_file():
    for default_config_path, default_config in create_default_config():
        test_function = feature_flag(
            name="test_feature_off", configuration_path=default_config_path
        )
        test_function = test_function(stub_func)
        assert test_function.configuration == default_config

    test_function = feature_flag(name="test_feature_off")
    test_function = test_function(stub_func)
    assert test_function.configuration is None
    test_function.clean()


def test_no_valid_path_to_config():
    with pytest.raises(FileNotFoundError):
        test_function = feature_flag(
            name="test_feature_off", configuration_path=pathlib.Path("does/not/exist")
        )
        test_function = test_function(stub_func)
        test_function.clean()


def test_register_feature_from_config():
    test_function = feature_flag(
        name="test_feature_off", configuration=TestConfig().DEFAULT_CONFIG
    )
    test_function = test_function(stub_func)

    assert len(test_function.registered_features) == 3
    assert (
        Feature(**{"name": "test_feature_off", "activation": "off"})
        in test_function.registered_features
    )

    test_function.clean()


def test_register_feature_from_config_file():
    for default_config_path, default_config in create_default_config():
        test_function = feature_flag(
            name="test_feature_off", configuration_path=default_config_path
        )
        test_function = test_function(stub_func)
        assert len(test_function.registered_features) == 3
        assert (
            Feature(
                **{
                    "name": "test_feature_off",
                    "activation": "off",
                }
            )
            in test_function.registered_features
        )

    test_function.clean()


def test_register_feature_with_setting_new_config():
    test_function = feature_flag(name="test_feature_off")
    test_function = test_function(stub_func)

    assert len(test_function.registered_features) == 1
    assert (
        Feature(
            **{
                "name": "test_feature_off",
                "activation": "off",
            }
        )
        in test_function.registered_features
    )

    test_function.configuration = TestConfig().DEFAULT_CONFIG
    assert len(test_function.registered_features) == 3

    test_function.clean()


def test_use_activation_from_config_on_method():
    test_function = feature_flag(
        name="test_feature_on", configuration=TestConfig().DEFAULT_CONFIG
    )
    test_function = test_function(stub_func)

    assert test_function() is True

    test_function.clean()


def test_override_not_config_activation():
    test_function = feature_flag(
        activation="on",
        name="test_feature_off",
        configuration=TestConfig().DEFAULT_CONFIG,
    )
    test_function = test_function(stub_func)

    with pytest.raises(NotImplementedError):
        test_function()

    test_function.clean()


def test_use_environment_variable_activation():
    os.environ["TEST_ACTIVATION"] = "off"

    test_function = feature_flag(
        name="test_feature_environment", configuration=TestConfig().DEFAULT_CONFIG
    )
    test_function = test_function(stub_func)

    with pytest.raises(NotImplementedError):
        test_function()

    test_function.clean()

    os.environ["TEST_ACTIVATION"] = "on"

    test_function = feature_flag(
        name="test_feature_environment", configuration=TestConfig().DEFAULT_CONFIG
    )
    test_function = test_function(stub_func)

    assert test_function() is True

    test_function.clean()


def test_wrong_keywords_value_in_config():
    config = dict(
        **{"feature_key_value_wrong": {"activation": "wrong_value"}},
        **TestConfig().DEFAULT_CONFIG
    )
    test_function = feature_flag(name="feature_key_value_wrong", configuration=config)
    test_function = test_function(stub_func)

    with pytest.raises(KeyError):
        test_function()

    test_function.clean()


def test_config_has_wrong_schema():
    with pytest.raises(WrongFeatureSchema):
        test_function = feature_flag(
            name="wrong_schema", configuration=TestConfig().WRONG_SCHEMA
        )
        test_function = test_function(stub_func)

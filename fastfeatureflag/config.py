"""Configuration

This module holds all relevant configuration parts, splitted for individual use cases.
"""
import pathlib


class Config:
    """Default configuration"""

    PATH_TO_DEFAULT_CONFIGURATION = pathlib.Path().cwd() / "fastfeatureflag_config.toml"


class TestConfig(Config):
    """Test specific configuration"""

    PATH_TO_CONFIGURATION = (
        pathlib.Path().cwd()
        / "tests"
        / "unittests"
        / "resources"
        / "fastfeatureflag_config.toml"
    )

    DEFAULT_CONFIG = config = {
        "test_feature_off": {"activation": "off"},
        "test_feature_on": {"activation": "on"},
        "test_feature_environment": {"activation": "TEST_ACTIVATION"},
    }

    WRONG_SCHEMA = {"wrong_schema": {"not_activation": "not_on"}}

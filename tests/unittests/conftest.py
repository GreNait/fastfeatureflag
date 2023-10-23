import pytest
import toml

from fastfeatureflag.config import TestConfig


@pytest.fixture
def default_config():
    try:
        with TestConfig().PATH_TO_DEFAULT_CONFIGURATION.open("w") as file:
            toml.dump(TestConfig().DEFAULT_CONFIG, file)

        yield TestConfig().PATH_TO_DEFAULT_CONFIGURATION
    finally:
        TestConfig().PATH_TO_DEFAULT_CONFIGURATION.unlink()


@pytest.fixture
def decorated_stub():
    def stub_func(response=True, option=None) -> bool:
        if option:
            return option

        return response

    return stub_func

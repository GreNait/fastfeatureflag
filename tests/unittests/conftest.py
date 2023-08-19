import pytest


@pytest.fixture
def decorated_stub():
    def stub_func(response=True, option=None) -> bool:
        if option:
            return option

        return response

    return stub_func

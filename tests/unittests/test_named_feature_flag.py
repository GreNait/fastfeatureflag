import pytest

from flaggen.feature_flag import feature_flag


def stub_func(response=True, option=None) -> bool:
    if option:
        return option

    return response


# def test_name_feature():
#     test_function = feature_flag(active="off", name="test")
#     test_function = test_function(stub_func)
#     assert test_function.feature_name == "test"

#     with pytest.raises(NotImplementedError):
#         test_function()

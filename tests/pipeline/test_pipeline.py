# import pathlib
# from unittest import mock

# import pytest
# from pipeline.ci_main import black

# # isort


# # Test autoformat (black & isort)
# @pytest.mark.asyncio
# async def test_start_black_nothing_to_change():
#     _runner = mock.Mock(
#         with_exec=mock.Mock(return_value=mock.Mock(stdout=mock.Mock(return_value="")))
#     )
#     path_to_project = pathlib.Path().cwd() / "fastfeatureflag"

#     assert await black(runner=_runner, path_to_project=path_to_project) is False
#     _runner.with_exec.assert_called_once_with(
#         ["poetry", "run", "black", "-q", str(path_to_project)]
#     )


# @pytest.mark.asyncio
# async def test_start_black_changed_files():
#     _runner = mock.Mock(
#         with_exec=mock.Mock(
#             return_value=mock.Mock(stdout=mock.Mock(return_value="formatted"))
#         )
#     )
#     path_to_project = pathlib.Path().cwd() / "fastfeatureflag"
#     assert await black(runner=_runner, path_to_project=path_to_project) is True


# @pytest.mark.asyncio
# async def test_raise_exception_non_existing_project():
#     _runner = mock.Mock()
#     path_to_project = pathlib.Path().cwd() / "NonExistentProject"

#     with pytest.raises(NonExistingProjectError):
#         await black(runner=_runner, path_to_project=path_to_project) is True


# # Test pylint score

# # Test mypy

# # Test unittest

# # Commit changes and restart

# # Test build package

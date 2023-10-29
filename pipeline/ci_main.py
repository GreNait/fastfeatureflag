import logging
import os
import pathlib
import sys

import anybadge
import anyio
import dagger
from dotenv import load_dotenv


async def main():
    async with dagger.Connection(dagger.Config(log_output=sys.stdout)) as client:
        load_dotenv()
        runner = await setup_runner(client=client)
        print(await pylint(runner=runner))
        print(await mypy(runner=runner))
        await unittests(runner=runner)
        await build_and_publish_python_package(runner)


# async def black(runner, path_to_project: pathlib.Path) -> bool:

#     formatted = runner.with_exec(["poetry", "run", "black", "-q", str(path_to_project)]).stdout()

#     if formatted:
#         return True

#     return False


async def setup_runner(client):
    return await (
        client.container()
        .from_("python:3.10-slim-buster")
        .with_mounted_cache("/root/.cache/pip", client.cache_volume("pip_cache"))
        .with_exec(["pip", "install", "poetry"])
        .with_mounted_cache("/root/.cache/poetry", client.cache_volume("poetry_cache"))
        .with_secret_variable(
            "POETRY_PYPI_TOKEN_PYPI",
            client.set_secret("pypi_token", os.getenv("PYPI_TOKEN")),
        )
        .with_directory(
            "/src",
            client.host().directory(".", exclude=[".venv", ".vscode"]),
        )
        .with_workdir("/src")
        .with_exec(["poetry", "install", "--with=dev,test"])
    )


async def pylint(runner):
    pylint_result = await runner.with_exec(
        ["poetry", "run", "pylint", "fastfeatureflag/"]
    ).stdout()

    rate_start = pylint_result.find("Your code has been rated at ") + len(
        "Your code has been rated at "
    )
    rate_end = rate_start + pylint_result[rate_start:].find("/")
    rate = pylint_result[rate_start:rate_end]

    if float(rate) < 9.5:
        print("pylint failed")

    path_to_badges = pathlib.Path().cwd() / "docs" / "badges"

    thresholds = {2: "red", 4: "orange", 6: "yellow", 10: "green"}

    path_pylint_badge = path_to_badges / "pylint.svg"

    pylint_badge = anybadge.Badge("pylint", float(rate), thresholds=thresholds)
    pylint_badge.write_badge(path_pylint_badge, overwrite=True)

    return pylint


async def mypy(runner):
    path_to_badges = pathlib.Path().cwd() / "docs" / "badges"
    path_to_mypy_badge = path_to_badges / "mypy.svg"

    try:
        mypy = await runner.with_exec(
            ["poetry", "run", "mypy", "fastfeatureflag/"]
        ).stdout()

        mypy_badge = anybadge.Badge(
            "mypy", default_color="green", value="\N{THUMBS UP SIGN}"
        )

    except dagger.ExecError as e:
        mypy_badge = anybadge.Badge(
            "mypy", default_color="red", value="\N{THUMBS DOWN SIGN}"
        )

    mypy_badge.write_badge(path_to_mypy_badge, overwrite=True)


async def unittests(runner):
    tests = await runner.with_exec(
        ["poetry", "run", "pytest", "tests/unittests"]
    ).stdout()

    path_to_badges = pathlib.Path().cwd() / "docs" / "badges"
    path_to_unittest_badge = path_to_badges / "unittests.svg"

    if "failed" in tests:
        unittest_badge = anybadge.Badge(
            label="unittests", value="failed \N{THUMBS DOWN SIGN}", default_color="red"
        )
    else:
        unittest_badge = anybadge.Badge(
            label="unittests", value="passed \N{THUMBS UP SIGN}", default_color="green"
        )

    unittest_badge.write_badge(path_to_unittest_badge, overwrite=True)


async def build_and_publish_python_package(runner):
    build_package = await runner.with_exec(
        ["poetry", "publish", "--build", "--skip-existing"]
    ).stdout()

    return build_package


if __name__ == "__main__":
    try:
        anyio.run(main)
    except dagger.ExecError as e:
        logging.exception("Unexpected dagger error")
        sys.exit(1)

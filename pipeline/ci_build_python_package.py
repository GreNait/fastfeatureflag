"""Pipeline for building and publishing python package"""
import os
import sys

import anyio
import dagger
from dotenv import load_dotenv


async def build_and_publish_python_package():
    """"""
    async with dagger.Connection(dagger.Config(log_output=sys.stdout)) as client:
        load_dotenv()
        secret = client.set_secret("PYPI_TOKEN", os.environ.get("PYPI_TOKEN"))

        runner = (
            client.container()
            .from_("python:3.10-slim-buster")
            .with_directory(
                path=".",
                directory=client.host().directory((".")),
                exclude=[".venv", ".vscode"],
            )
            .with_secret_variable("PYPI_TOKEN", secret)
            .with_exec(["pip", "install", "poetry"])
            .with_exec(["poetry", "install"])
            .with_exec(["poetry", "config", "pypi-token.pypi", "$PYPI_TOKEN"])
        )

        build_package = await runner.with_exec(
            ["poetry", "publish", "--build"]
        ).stdout()

        print(build_package)


anyio.run(build_and_publish_python_package)

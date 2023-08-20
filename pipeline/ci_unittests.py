"""Pipeline for executing unittests"""
import sys

import anyio
import dagger


async def unittest():
    """Unittest pipeline defined with Dagger"""
    config = dagger.Config(log_output=sys.stdout)

    async with dagger.Connection(config) as client:
        runner = (
            client.container()
            .from_("python:3.10-slim-buster")
            .with_directory(
                path=".",
                directory=client.host().directory((".")),
                exclude=[".venv", ".vscode"],
            )
            .with_exec(["pip", "install", "poetry"])
            .with_exec(["poetry", "install"])
        )

        unittests = await runner.with_exec(
            ["poetry", "run", "pytest", "tests/unittests"]
        ).stdout()

        print(unittests)

        # runner.with_exec(["mkdocs", "build"])


anyio.run(unittest)

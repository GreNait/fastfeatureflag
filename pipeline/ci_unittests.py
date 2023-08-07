"""Pipeline for executing unittests"""
import sys

import anyio
import dagger


async def main():
    """Unittest pipeline defined with Dagger"""
    config = dagger.Config(log_output=sys.stdout)

    async with dagger.Connection(config) as client:
        runner = (
            client.container()
            .from_("python:3.10-slim-buster")
            .with_directory(path=".", directory=client.host().directory((".")))
            .with_exec(["pip", "install", "."])
            .with_exec(["pytest", "tests/unittests"])
        )

        unittests = await runner.stdout()

        print(f"Unittest grades: {unittests}")


anyio.run(main)

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
            .with_exec(["pytest -v", "tests/unittests"])
        )

        unittests = await runner.stdout()

        # passed = unittests.count("PASSED")
        # failed = unittests.count("FAILED")

        # badge = f"![unittests passed](https://img.shields.io/badge/unittests_passed-{passed}-brightGreen)"

        # with open("../README.md", "r") as file:
        #     content = file.read()

        print(f"Unittest grades: {unittests}")


anyio.run(main)

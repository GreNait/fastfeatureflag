import pathlib
from dataclasses import dataclass, replace
from typing import Callable


@dataclass
class FeatureContent:
    activation: str
    name: str | None
    response: str | None = None
    shadow: str | None = None
    func: Callable | None = None
    configuration: dict | None = None
    configuration_path: pathlib.Path | None = None

    def update(self, **kwargs):
        """Update feature"""
        self.__dict__ = {**self.__dict__, **kwargs}

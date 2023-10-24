import pathlib
from dataclasses import dataclass
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

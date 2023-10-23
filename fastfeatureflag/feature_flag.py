"""This module contains the feature flag implementation."""

import importlib
import pathlib
from typing import Any, Callable

from fastfeatureflag.errors import CannotRunShadowWithoutFunctionError
from fastfeatureflag.feature_flag_configuration import FeatureFlagConfiguration
from fastfeatureflag.shadow_configuration import ShadowConfiguration


class feature_flag:  # pylint: disable=invalid-name
    """Feature flag

    Feature flag containing the flag and the shadow
    mode.
    """

    def __init__(
        self,
        activation: str = "off",
        response: Any | None = None,
        name: str | None = None,
        configuration: dict | None = None,
        configuration_path: pathlib.Path | None = None,
        **kwargs,
    ):
        super().__init__()
        self.activation = activation
        self.response = response
        self.name = name
        self.configuration = configuration
        self.configuration_path = configuration_path
        self.kwargs = kwargs

    def __call__(self, func):
        return FeatureFlagConfiguration(
            func=func,
            activation=self.activation,
            response=self.response,
            name=self.name,
            feature_configuration=self.configuration,
            feature_configuration_path=self.configuration_path,
            **self.kwargs,
        )

    def shadow(self, run: Callable | str, *args, **kwargs):
        """Shadow feature

        Args:
            run (function): The alternative method which should be called.
        """
        if self.activation == "on":
            return self

        if isinstance(run, str):
            module, function = run.rsplit(".", 1)
            run = getattr(importlib.import_module(module), function)

        if run is None or not callable(run):
            raise CannotRunShadowWithoutFunctionError() from None

        def decorated_function(func: Callable):
            """Inner wrapper for the decorated function.

            Args:
                func (function): The original function

            Returns:
                run: Function running the alternative function.
            """
            shadow_run = ShadowConfiguration(run, *args, **kwargs)
            return shadow_run.run

        return decorated_function

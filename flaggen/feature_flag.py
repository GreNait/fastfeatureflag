"""This module contains the simple feature flag implementation."""

import os
import pathlib
from typing import Any

import toml

from flaggen.errors import WrongFeatureSchema
from flaggen.feature_schema import Feature


class _FeatureFlag:
    _registered_features: list[Feature] = []
    _configuration: dict

    def __init__(
        self,
        func,
        activation: str = "off",
        response: Any | None = None,
        name: str | None = None,
        configuration: dict | None = None,
        configuration_path: pathlib.Path | None = None,
        **kwargs,
    ):
        self._func = func
        self._activation = activation
        self._response = response
        self._options = kwargs

        if configuration:
            self._load_configuration(configuration)

        if configuration_path:
            self._load_configuration_from_file(path=configuration_path)
            self._configuration_path = configuration_path

        if configuration_path is None and configuration is None:
            path_to_default_config = pathlib.Path().cwd() / "flaggen_config.toml"
            if path_to_default_config.exists():
                self._load_configuration_from_file(path=path_to_default_config)
                self._configuration_path = path_to_default_config
            else:
                self._configuration = None
                self._configuration_path = None

        if name:
            if self.is_registered(name):
                feature = self.find_feature(name)
                self._activation = feature.activation

            else:
                self.register(name=name, feature_content={"activation": activation})

            self._name = name

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._decorated_function(*args, **kwargs)

    def _load_configuration(self, configuration: dict):
        for feature in configuration:
            self.register(name=feature, feature_content=configuration.get(feature))
        self._configuration = configuration

    def _load_configuration_from_file(self, path):
        if path.exists():
            content = toml.load(path)
            self._load_configuration(configuration=content)
        else:
            raise FileNotFoundError("Config file not found") from None

    @classmethod
    def find_feature(cls, name) -> Feature | None:
        """Find feature

        Find registered feature by name.

        Args:
            name (str): Name of the registered feature

        Returns:
            dict: Feature
        """
        for feature in cls._registered_features:
            if name == feature.name:
                return feature
        return None

    @classmethod
    def register(cls, name: str, feature_content: dict):
        """Register feature

        Register feature by name with activation.

        Args:
            name (str): Name of the feature
            activation (str): on/off
        """
        if not cls.is_registered(name):
            try:
                feature = Feature(name=name, **feature_content)
            except TypeError as caught_exception:
                raise WrongFeatureSchema(
                    "Feature content schema not valid. Perhaps wrong keywords have been used."
                ) from caught_exception

            cls._registered_features.append(feature)

    @classmethod
    def is_registered(cls, name):
        """Check if feature is registered

        Args:
            name (str): Feature name.

        Returns:
            bool: True|False
        """
        if cls.find_feature(name):
            return True
        return False

    @classmethod
    def clean(cls):
        """Empty registered features"""
        cls._registered_features = []

    def _decorated_function(self, *args, **kwargs):
        """Function build with all parameters.

        This function is returned and executes additional steps
        before the original function (from `decorated_function`)
        is called.

        Raises:
            NotImplementedError: Raised if the feature flag is off.
            KeyError: Raised when the activation keyword is not known.

        Returns:
            object: The original/input function containing also all options.
        """
        if self._activation == "off" or os.environ.get(self._activation) == "off":
            if self._response:
                return self._response

            raise NotImplementedError("Feature not implemented") from None

        if self._activation == "on" or os.environ.get(self._activation) == "on":
            self._options = self._options | kwargs
            return self._func(*args, **self._options)

        raise KeyError(f"Wrong key. Possible keys: on|off, got: {self._activation}")

    @property
    def feature_name(self) -> str:
        """Return feature name

        Returns:
            str: Feature name
        """
        return self._name

    @property
    def feature_active(self) -> str:
        """Return activation status

        Returns:
            str: Activation: on|off
        """
        return self._activation

    @property
    def registered_features(self) -> list[Feature]:
        """Return list of registered features

        Returns:
            list[Feature]: List containing Feature()s
        """
        return self._registered_features

    @property
    def configuration(self) -> dict:
        """Return configuration

        Returns:
            dict: Configuration
        """
        return self._configuration

    @configuration.setter
    def configuration(self, new_configuration):
        self._load_configuration(configuration=new_configuration)

    @property
    def configuration_path(self) -> pathlib.Path | None:
        """Return path to configuration file

        Returns:
            pathlib.Path | None: Path to configuration file
        """
        return self._configuration_path

    @configuration_path.setter
    def configuration_path(self, path: pathlib.Path):
        self._load_configuration_from_file(path=path)
        self._configuration_path = path


def feature_flag(
    activation: str = "off",
    response=None,
    name: str | None = None,
    configuration: dict = None,
    configuration_path: pathlib.Path = None,
    **kwargs,
):
    """Feature flag.

    The outer wrapper/decorator for the feature flag.

    Args:
        activation (str, optional): Activating/deactivating the
            function(feature). Defaults to "off".
    """

    def decorated_function(func):
        """Inner wrapper for the decorated function.

        Uses the information from the feature flag (outer wrapper) and
        prepares a function wrapping around the input function.

        Args:
            func (object): The decorated function.
        """

        return _FeatureFlag(
            func=func,
            activation=activation,
            response=response,
            name=name,
            configuration=configuration,
            configuration_path=configuration_path,
            **kwargs,
        )

    return decorated_function

"""This module contains the simple feature flag implementation."""

from typing import Any


class _FeatureFlag:
    _registered_features: list = []

    def __init__(
        self,
        func,
        active: str = "off",
        response: Any | None = None,
        name: str | None = None,
        **kwargs,
    ):
        self._func = func
        self._active = active
        self._response = response
        self._options = kwargs

        if name:
            if self.is_registered(name):
                feature = self.find_feature(name)
                self._active = feature["active"]

            else:
                self.register(name, active)

            self._name = name

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._decorated_function(*args, **kwargs)

    @classmethod
    def find_feature(cls, name):
        """Find feature

        Find registered feature by name.

        Args:
            name (str): Name of the registered feature

        Returns:
            dict: Feature
        """
        for feature in cls._registered_features:
            if name in feature["name"]:
                return feature

    @classmethod
    def register(cls, name, active):
        """Register feature

        Register feature by name and active.

        Args:
            name (str): Name of the feature
            active (str): on/off
        """
        cls._registered_features.append({"name": name, "active": active})

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
        if self._active == "off":
            if self._response:
                return self._response

            raise NotImplementedError("Feature not implemented") from None

        if self._active != "on":
            raise KeyError(f"Wrong key. Possible keys: on|off, got: {self._active}")

        self._options = self._options | kwargs

        return self._func(*args, **self._options)

    @property
    def feature_name(self) -> str:
        return self._name

    @property
    def feature_active(self):
        return self._active

    @property
    def registered_features(self):
        return self._registered_features


def feature_flag(active: str = "off", response=None, name: str | None = None, **kwargs):
    """Feature flag.

    The outer wrapper/decorator for the feature flag.

    Args:
        active (str, optional): Activating/deactivating the function(feature). Defaults to "off".
    """

    def decorated_function(func):
        """Inner wrapper for the decorated function.

        Uses the information from the feature flag (outer wrapper) and
        prepares a function wrapping around the input function.

        Args:
            func (object): The decorated function.
        """

        return _FeatureFlag(func, active, response, name, **kwargs)

    return decorated_function

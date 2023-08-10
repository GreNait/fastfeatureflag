"""This module contains the simple feature flag implementation."""

from typing import Any


class _FeatureFlag:
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
            self._name = name

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._decorated_function(*args, **kwargs)

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

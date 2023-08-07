"""This module contains the simple feature flag implementation."""


def feature_flag(active: str = "off", **kwargs):
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

        def injected_function():
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
            if active == "off":
                raise NotImplementedError("Feature not implemented") from None

            if active != "on":
                raise KeyError(f"Wrong key. Possible keys: on|off, got: {active}")

            return func(**kwargs)

        return injected_function

    return decorated_function

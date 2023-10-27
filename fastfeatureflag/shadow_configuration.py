"""Defining shadow configurations."""


# pylint: disable=too-few-public-methods
class ShadowConfiguration:
    """Shadow mode configuration"""

    def __init__(self, func, *args, **kwargs) -> None:
        """Loading the shadow configuration

        With this constructor, the necessary arguments are saved
        to call the shadow method form the decorated method.

        Args:
            func (function): The alternative method which should be called
                instead of the original one.
        """
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self, *args, **kwargs):
        """Runs the alternative method

        Returns:
            Any: Returns the output from the provided alternative method.
        """
        return self.func(*args, **kwargs)

"""Custom exceptions"""


class FeatureContentNotDict(Exception):
    """Feature content appears to be no dict."""


class WrongFeatureSchema(Exception):
    """Wrong feature schema detected."""


class FeatureNotRegistered(Exception):
    """Feature not found in registered features."""

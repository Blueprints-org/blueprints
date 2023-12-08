"""Module for validation actions inside of Blueprints."""


class LessOrEqualToZeroError(Exception):
    """Raised when a value is less than or equal to zero."""

    def __init__(self, value_name: str, value: float) -> None:
        message = f"Invalid value for '{value_name}': {value}. Values for '{value_name}' must be greater than zero."
        super().__init__(message)


class NegativeValueError(Exception):
    """Raised when a value is negative."""

    def __init__(self, value_name: str, value: float) -> None:
        message = f"Invalid value for '{value_name}': {value}. Values for '{value_name}' cannot be negative."
        super().__init__(message)


class GreaterThan90Error(Exception):
    """Raised when a value is greater than 90."""

    def __init__(self, value_name: str, value: float) -> None:
        message = f"Invalid value for '{value_name}': {value}. Values for '{value_name}' cannot be greater than 90."
        super().__init__(message)


def raise_if_less_or_equal_to_zero(**kwargs: float) -> None:
    """Raise a LessOrEqualToZeroError if any of the given keyword arguments are less than or equal to zero.

    Parameters
    ----------
    **kwargs : dict[str, float]
        A dictionary of keyword arguments where keys are parameter names, and values are the values to validate.

    Raises
    ------
    LessOrEqualToZeroError
        If any value is less than or equal to zero.

    """
    for key, value in kwargs.items():
        if value <= 0:
            raise LessOrEqualToZeroError(value_name=key, value=value)


def raise_if_negative(**kwargs: float) -> None:
    """Raise a NegativeValueError if any of the given keyword arguments are negative.

    Parameters
    ----------
    **kwargs : dict[str, float]
        A dictionary of keyword arguments where keys are parameter names, and values are the values to validate.

    Raises
    ------
    NegativeValueError
        If any value is negative.

    """
    for key, value in kwargs.items():
        if value < 0:
            raise NegativeValueError(value_name=key, value=value)


def raise_if_greater_than_90(**kwargs: float) -> None:
    """Raise a GreaterThan90Error if any of the given keyword arguments are greater than 90.

    Parameters
    ----------
    **kwargs : dict[str, float]
        A dictionary of keyword arguments where keys are parameter names, and values are the values to validate.

    Raises
    ------
    GreaterThan90Error
        If any value is greater than 90.

    """
    for key, value in kwargs.items():
        if value > 90:
            raise GreaterThan90Error(value_name=key, value=value)

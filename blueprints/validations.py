"""Module for validation actions inside of Blueprints."""


class NonPositiveValueError(Exception):
    """Raised when a value is less than or equal to zero."""


class NegativeValueError(Exception):
    """Raised when a value is negative."""


def raise_if_less_or_equal_to_zero(**kwargs) -> None:
    """
    Raise a ValueError if any of the given keyword arguments are less than or equal to zero.

    Parameters
    ----------
    **kwargs
        A dictionary of keyword arguments where keys are parameter names, and values are the values to validate.

    Raises
    ------
    ValueError
        If any value is greater than zero.

    """
    for key, value in kwargs.items():
        if value <= 0:
            raise NonPositiveValueError(f"Invalid value for '{key}': {value}. Values for '{key}' must be greater than zero.")


def raise_if_negative(**kwargs) -> None:
    """
    Raise a ValueError if any of the given keyword arguments are negative.

    Parameters
    ----------
    **kwargs
        A dictionary of keyword arguments where keys are parameter names, and values are the values to validate.

    Raises
    ------
    ValueError
        If any value is greater than or equal to zero.

    """
    for key, value in kwargs.items():
        if value < 0:
            raise NegativeValueError(f"Invalid value for '{key}': {value}. Values for '{key}' cannot be negative.")

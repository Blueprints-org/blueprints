"""Math helpers for Blueprints."""

import numpy as np

from blueprints.type_alias import DEG, DIMENSIONLESS, PERCENTAGE
from blueprints.validations import raise_if_greater_than_90, raise_if_less_or_equal_to_zero, raise_if_negative


def cot(x: DEG) -> DIMENSIONLESS:
    """Calculate the cotangent of an angle in degrees.

    Parameters
    ----------
    x : DEG
        Angle in degrees.

    Returns
    -------
    DIMENSIONLESS
        Cotangent of the angle.
    """
    raise_if_less_or_equal_to_zero(x=x)
    raise_if_greater_than_90(x=x)
    return 1 / np.tan(np.deg2rad(x))


def sec(x: DEG) -> DIMENSIONLESS:
    """Calculate the secant of an angle in degrees.

    Parameters
    ----------
    x : DEG
        Angle in degrees.

    Returns
    -------
    DIMENSIONLESS
        Secant of the angle.
    """
    raise_if_negative(x=x)
    raise_if_greater_than_90(x=x)
    return 1 / np.cos(np.deg2rad(x))


def csc(x: DEG) -> DIMENSIONLESS:
    """Calculate the cosecant of an angle in degrees.

    Parameters
    ----------
    x : DEG
        Angle in degrees.

    Returns
    -------
    DIMENSIONLESS
        Cosecant of the angle.
    """
    raise_if_less_or_equal_to_zero(x=x)
    raise_if_greater_than_90(x=x)
    return 1 / np.sin(np.deg2rad(x))


def slope_to_angle(slope: PERCENTAGE) -> DEG:
    """Convert a slope (as a percentage) to an angle in degrees.

    Parameters
    ----------
    slope : PERCENTAGE
        Slope as a percentage.

    Returns
    -------
    DEG
        Angle in degrees.
    """
    return np.rad2deg(np.arctan(slope / 100))


def angle_to_slope(angle: DEG) -> PERCENTAGE:
    """Convert an angle in degrees to a slope (as a percentage).

    Parameters
    ----------
    angle : DEG
        Angle in degrees.

    Returns
    -------
    PERCENTAGE
        Slope as a percentage.
    """
    raise_if_negative(angle=angle)
    raise_if_greater_than_90(angle=angle)
    return np.tan(np.deg2rad(angle)) * 100

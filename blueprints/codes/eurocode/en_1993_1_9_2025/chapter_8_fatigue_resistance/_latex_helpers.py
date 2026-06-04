"""Shared LaTeX formatting helpers for EN 1993-1-9:2025: Chapter 8 - Fatigue resistance."""


def latex_scientific(value: float) -> str:
    r"""Format a number in LaTeX scientific notation with a single-decimal mantissa, e.g. ``2.0 \cdot 10^{6}``.

    Cycle numbers on the fatigue strength curve are of the order [$10^6$] to [$10^8$], so a fixed-point
    representation is hard to read; scientific notation keeps the numeric equation legible.

    Parameters
    ----------
    value : float
        The number to format, typically a number of cycles [$N$].

    Returns
    -------
    str
        The value as a LaTeX string, e.g. ``2.0 \cdot 10^{6}``.
    """
    mantissa, exponent = f"{value:.1e}".split("e")
    return rf"{mantissa} \cdot 10^{{{int(exponent)}}}"

"""Utilities for handling uniform corrosion related operations in structural profiles."""

from __future__ import annotations

import re
from typing import overload

from blueprints.type_alias import MM

FULL_CORROSION_TOLERANCE: MM = 1e-3


@overload
def update_name_with_corrosion(
    current_name: str,
    *,
    corrosion: MM,
    corrosion_inside: None = None,
    corrosion_outside: None = None,
) -> str: ...


@overload
def update_name_with_corrosion(
    current_name: str,
    *,
    corrosion_inside: MM,
    corrosion_outside: MM,
    corrosion: None = None,
) -> str: ...


def update_name_with_corrosion(
    current_name: str,
    *,
    corrosion: MM | None = None,
    corrosion_inside: MM | None = None,
    corrosion_outside: MM | None = None,
) -> str:
    """Update profile name with corrosion information.

    Extracts any existing corrosion value(s) from the name, adds the new corrosion,
    and returns the updated name with the total corrosion.

    This function supports two modes:
    1. Single corrosion value (uniform): Pass `corrosion` parameter
    2. Double corrosion values (inside/outside): Pass `corrosion_inside` and/or `corrosion_outside`

    Parameters
    ----------
    current_name : str
        The current profile name, which may or may not include corrosion info.
    corrosion : MM, optional
        The uniform corrosion to add (for profiles with single corrosion value) [mm].
        Mutually exclusive with corrosion_inside/corrosion_outside.
    corrosion_inside : MM, optional
        The inside corrosion to add (for hollow profiles) [mm].
        Should be used with corrosion_outside.
    corrosion_outside : MM, optional
        The outside corrosion to add (for hollow profiles) [mm].
        Should be used with corrosion_inside.

    Returns
    -------
    str
        The updated name with total corrosion information.

    Raises
    ------
    ValueError
        If both single and double corrosion parameters are provided.
    ValueError
        If neither single nor double corrosion parameters are provided.

    Examples
    --------
    Single corrosion (uniform):
    >>> update_name_with_corrosion("IPE200", corrosion=1.5)
    'IPE200 (corrosion: 1.5 mm)'
    >>> update_name_with_corrosion("IPE200 (corrosion: 1.5 mm)", corrosion=0.5)
    'IPE200 (corrosion: 2.0 mm)'

    Double corrosion (inside/outside):
    >>> update_name_with_corrosion("RHS200x100x5", corrosion_inside=1.0, corrosion_outside=2.0)
    'RHS200x100x5 (corrosion inside: 1.0 mm, outside: 2.0 mm)'
    >>> update_name_with_corrosion("RHS200x100x5 (corrosion inside: 1.0 mm, outside: 2.0 mm)", corrosion_inside=0.5, corrosion_outside=1.0)
    'RHS200x100x5 (corrosion inside: 1.5 mm, outside: 3.0 mm)'
    """
    single_mode = corrosion is not None
    double_mode = corrosion_inside is not None or corrosion_outside is not None

    if single_mode and double_mode:
        msg = "Cannot use both single corrosion and double (inside/outside) corrosion parameters"
        raise ValueError(msg)

    if not single_mode and not double_mode:
        msg = "At least one corrosion parameter must be provided"
        raise ValueError(msg)

    if single_mode:
        return _update_single_corrosion(current_name, corrosion)  # type: ignore[arg-type]
    return _update_double_corrosion(current_name, corrosion_inside or 0, corrosion_outside or 0)


def _update_single_corrosion(current_name: str, additional_corrosion: MM) -> str:
    """Update name with single (uniform) corrosion value.

    Parameters
    ----------
    current_name : str
        The current profile name.
    additional_corrosion : MM
        The additional corrosion to add [mm].

    Returns
    -------
    str
        The updated name with total corrosion.
    """
    # Pattern to match single corrosion: (corrosion: X mm)
    pattern = r"\s*\(corrosion:\s*([0-9.]+)\s*mm\)\s*$"
    match = re.search(pattern, current_name)

    if match:
        existing_corrosion = float(match.group(1))
        base_name = re.sub(pattern, "", current_name)
        total_corrosion = existing_corrosion + additional_corrosion
    else:
        base_name = current_name
        total_corrosion = additional_corrosion

    return f"{base_name} (corrosion: {total_corrosion} mm)"


def _update_double_corrosion(current_name: str, additional_inside: MM, additional_outside: MM) -> str:
    """Update name with double (inside/outside) corrosion values.

    Parameters
    ----------
    current_name : str
        The current profile name.
    additional_inside : MM
        The additional inside corrosion to add [mm].
    additional_outside : MM
        The additional outside corrosion to add [mm].

    Returns
    -------
    str
        The updated name with total corrosion values.
    """
    # Pattern to match double corrosion: (corrosion inside: X mm, outside: Y mm)
    pattern = r"\s*\(corrosion\s+inside:\s*([0-9.]+)\s*mm,\s*outside:\s*([0-9.]+)\s*mm\)\s*$"
    match = re.search(pattern, current_name)

    if match:
        existing_inside = float(match.group(1))
        existing_outside = float(match.group(2))
        base_name = re.sub(pattern, "", current_name)
        total_inside = existing_inside + additional_inside
        total_outside = existing_outside + additional_outside
    else:
        base_name = current_name
        total_inside = additional_inside
        total_outside = additional_outside

    return f"{base_name} (corrosion inside: {total_inside} mm, outside: {total_outside} mm)"

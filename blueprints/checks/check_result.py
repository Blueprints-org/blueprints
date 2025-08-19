"""Common check result class for structural checks."""

from dataclasses import dataclass


@dataclass
class CheckResult:
    """Class to hold the result of a structural check.

    Attributes
    ----------
    is_ok : bool
        Whether the check passes (True) or fails (False).
    utilization : float
        The utilization ratio (demand/capacity). Values > 1.0 indicate failure.
    required : float | None
        The required value for the check (e.g., minimum reinforcement area).
    provided : float | None
        The provided value for the check (e.g., actual reinforcement area).
    """

    is_ok: bool
    utilization: float
    required: float | None
    provided: float | None

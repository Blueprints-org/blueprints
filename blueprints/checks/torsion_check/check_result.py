"""Result data structure for structural checks."""

from dataclasses import dataclass


@dataclass
class CheckResult:
    """Contains the results of a structural engineering check.

    This class stores the outcome of any structural verification, providing
    both pass/fail status and detailed information about capacity utilization.
    Use this to understand whether your design meets code requirements and
    how efficiently you're using the available capacity.

    Parameters
    ----------
    is_ok : bool
        Whether the structural check passes code requirements.
        True means the design is safe and compliant, False means the
        design fails and needs modification (stronger materials, larger
        sections, more reinforcement, etc.).
    utilization : float
        Ratio of demand to capacity, indicating how much of the available
        strength is being used. Values < 1.0 indicate reserve capacity,
        values > 1.0 indicate over-utilization requiring design changes.
        For example: 0.85 means 85% of capacity is used (15% safety margin),
        1.20 means 120% utilization (20% over capacity - design fails).
    required : float | None
        The minimum value needed to satisfy the structural requirement.
        Units depend on the specific check (e.g., mm² for reinforcement area,
        MPa for stress, mm for spacing). None if not applicable to the check.
        Compare with 'provided' to see if you have enough.
    provided : float | None
        The actual value available in your design.
        Units match 'required'. None if not applicable to the check.
        Should be ≥ 'required' for the check to pass.

    Examples
    --------
    >>> # Reinforcement area check
    >>> result = CheckResult(
    ...     is_ok=True,
    ...     utilization=0.75,
    ...     required=1200.0,  # mm²
    ...     provided=1600.0,  # mm²
    ... )
    >>> print(f"Need {result.required} mm², have {result.provided} mm²")
    >>> print(f"Using {result.utilization * 100:.1f}% of capacity")

    >>> # Stress check that fails
    >>> result = CheckResult(
    ...     is_ok=False,
    ...     utilization=1.15,
    ...     required=None,  # No specific value applicable
    ...     provided=None,  # No specific value applicable
    ... )
    >>> print("Design fails - 15% over capacity!")

    Notes
    -----
    - Always check `is_ok` first to determine if design modifications are needed
    - Use `utilization` to optimize your design efficiency
    - Values close to 1.0 indicate efficient but potentially risky designs
    """

    is_ok: bool
    utilization: float
    required: float | None
    provided: float | None

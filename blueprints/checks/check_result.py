"""Result data structure for structural checks."""

from dataclasses import dataclass

from blueprints.validations import raise_if_negative


@dataclass
class CheckResult:
    """Contains the results of a structural engineering check.

    This class stores the outcome of any structural verification, providing
    both pass/fail status and detailed information about capacity utilization or factor of safety.
    Use this to understand whether your design meets code requirements and
    how efficiently you're using the available capacity.

    Parameters
    ----------
    is_ok : bool, default required
        Whether the structural check passes code requirements.
        True means the design is safe and compliant, False means the
        design fails and needs modification (stronger materials, larger
        sections, more reinforcement, etc.).
    unity_check : float | None, default None
        Ratio of demand to capacity, indicating how much of the available
        strength is being used. Values < 1.0 indicate reserve capacity,
        values > 1.0 indicate over-utilization requiring design changes.
        For example: 0.85 means 85% of capacity is used (15% safety margin),
        1.20 means 120% unity check (20% over capacity - design fails).
    factor_of_safety : float | None, default None
        One over utilization, indicating the safety margin in the design.
        Values > 1.0 indicate reserve capacity, values < 1.0 indicate
        over-utilization requiring design changes. If utlization is zero,
        the factor_of_safety is set to infinity.

    Examples
    --------
    >>> result = CheckResult(
    ...     unity_check=0.75,
    ... )
    >>> print(f"Using {result.unity_check * 100:.1f}% of capacity")
    >>> print(f"Factor of Safety: {result.factor_of_safety:.2f}")

    >>> result = CheckResult(
    ...     factor_of_safety=2.0,
    ... )
    >>> print(f"Using {result.unity_check * 100:.1f}% of capacity")
    >>> print(f"Factor of Safety: {result.factor_of_safety:.2f}")

    >>> result = CheckResult(
    ...     unity_check=1.15,
    ... )
    >>> print("Design fails - 15% over capacity!")

    Notes
    -----
    - Always check `is_ok` first to determine if design modifications are needed
    - Use `unity_check` to optimize your design efficiency
    - Use `factor_of_safety` to understand safety margins
    - Values close to 1.0 indicate efficient but potentially risky designs
    """

    is_ok: bool | None = None
    unity_check: float | None = None
    factor_of_safety: float | None = None

    def __post_init__(self) -> None:
        """Validate and synchronize unity_check, factor_of_safety, and is_ok."""
        # Validate non-negativity
        if self.unity_check is not None:
            raise_if_negative(unity_check=self.unity_check)
        if self.factor_of_safety is not None:
            raise_if_negative(factor_of_safety=self.factor_of_safety)

        # Consistency between unity_check and factor_of_safety
        if self.unity_check is not None and self.factor_of_safety is not None and abs(self.unity_check - 1 / self.factor_of_safety) >= 1e-6:
            raise ValueError(f"unity_check={self.unity_check} and factor_of_safety={self.factor_of_safety} are inconsistent")

        # Consistency between is_ok and unity_check/factor_of_safety
        if self.is_ok is not None:
            if self.unity_check is not None and (self.unity_check > 1) == self.is_ok:
                raise ValueError("Inconsistent CheckResult: unity_check and is_ok")
            if self.factor_of_safety is not None and (self.factor_of_safety < 1) == self.is_ok:
                raise ValueError("Inconsistent CheckResult: factor_of_safety and is_ok")

        # Calculate missing value for unity_check or factor_of_safety
        if self.unity_check is None and self.factor_of_safety is not None:
            self.unity_check = float("inf") if self.factor_of_safety == 0 else 1 / self.factor_of_safety
        elif self.factor_of_safety is None and self.unity_check is not None:
            self.factor_of_safety = float("inf") if self.unity_check == 0 else 1 / self.unity_check

        # Infer is_ok if not given
        if self.is_ok is None and self.unity_check is not None:
            self.is_ok = self.unity_check <= 1

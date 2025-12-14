"""Result data structure for structural checks."""

from dataclasses import dataclass

from blueprints.validations import raise_if_negative

TOLERANCE = 1e-6


@dataclass
class CheckResult:
    """Contains the results of a structural engineering check.

    This class stores the outcome of any structural verification, providing
    both pass/fail status and detailed information about capacity utilization or factor of safety.
    Use this to understand whether your design meets code requirements and
    how efficiently you're using the available capacity.

    You can instantiate this class by providing only the minimum required input
    (such as just `unity_check`, `factor_of_safety`, or a pair of `provided` and `limit`),
    and the other values will be computed automatically. You may also provide more than the minimum,
    but all values must be consistent or a ValueError will be raised.

    Parameters
    ----------
    is_ok : bool | None, optional
        Indicates whether the check passed (True) or failed (False).
        If None, it will be inferred from `unity_check` or `factor_of_safety` if available.
    unity_check : float | None, optional
        The ratio of applied demand to available capacity. A value <= 1.0 indicates the design passes.
    factor_of_safety : float | None, optional
        The margin of safety, defined as the ratio of capacity to demand. A value >= 1.0 indicates the design passes.
    provided : float | None, optional
        The actual calculated value from the design (e.g., applied load, stress).
    limit : float | None, optional
        The allowable limit for the design (e.g., capacity, code limit), the limit value itself is acceptable.
    operator : str, optional
        The comparison operator used to evaluate the check. Typically "<=" or ">=". Default is "<=".

    Examples
    --------
    # Minimum input required, other fields are computed:
    >>> CheckResult(is_ok=True)                            -> all fields None except is_ok=True
    >>> CheckResult(unity_check=0.8)                       -> factor_of_safety=1.25, is_ok=True
    >>> CheckResult(factor_of_safety=1.25)                 -> unity_check=0.8, is_ok=True
    >>> CheckResult(provided=80, limit=100)                -> unity_check=0.8, factor_of_safety=1.25, is_ok=True
    >>> CheckResult(provided=150, limit=100)               -> unity_check=1.5, factor_of_safety=0.666..., is_ok=False
    >>> CheckResult(provided=80, limit=100, operator=">=") -> unity_check=1.25, factor_of_safety=0.8, is_ok=False

    # More complete input will also be handled, but all fields need to be consistent:
    >>> CheckResult(is_ok=True, unity_check=0.8)           -> factor_of_safety=1.25

    # If inconsistent values are provided, a ValueError is raised:
    >>> CheckResult(is_ok=True, unity_check=1.5)           -> ValueError: Inconsistent CheckResult: unity_check and is_ok

    Notes
    -----
    - Only the minimum required input is needed; extra fields are optional but must be consistent.
    - If you provide inconsistent combinations, a ValueError will be raised.
    - Always check `is_ok` to determine if design modifications are needed.
    - Use `unity_check` to optimize your design efficiency.
    - Use `factor_of_safety` to understand safety margins.
    - Values close to 1.0 indicate efficient but potentially risky designs.
    """

    is_ok: bool | None = None
    unity_check: float | None = None
    factor_of_safety: float | None = None
    provided: float | None = None
    limit: float | None = None
    operator: str = "<="  # Options: "<=", ">="

    def __post_init__(self) -> None:  # noqa: C901 PLR0912
        """Validate and synchronize unity_check, factor_of_safety, and is_ok."""
        # Validate non-negativity
        if self.unity_check is not None:
            raise_if_negative(unity_check=self.unity_check)
        if self.factor_of_safety is not None:
            raise_if_negative(factor_of_safety=self.factor_of_safety)
        if self.provided is not None:
            raise_if_negative(provided=self.provided)
        if self.limit is not None:
            raise_if_negative(limit=self.limit)

        # Validate operator
        if self.operator not in ("<=", ">="):
            raise ValueError(f"Invalid operator: {self.operator}. Must be one of '<=', '>='.")

        # Provided and limit must both be None or both not None
        if (self.provided is None) != (self.limit is None):
            raise ValueError("Both 'provided' and 'limit' must be None or neither None")

        # If provided and limit are given, check consistency with unity_check/factor_of_safety/is_ok
        if self.provided is not None and self.limit is not None:
            # Calculate unity_check based on operator
            if self.operator == "<=":
                calculated_unity_check = 0 if self.provided == 0 else self.provided / self.limit if self.limit != 0 else float("inf")
            else:  # operator == ">="
                calculated_unity_check = self.limit / self.provided if self.provided != 0 else float("inf")

            # Consistency checks
            if self.unity_check is not None and abs(self.unity_check - calculated_unity_check) >= TOLERANCE:
                raise ValueError("Inconsistent CheckResult: provided/limit and unity_check")
            if self.factor_of_safety is not None:
                calculated_factor_of_safety = float("inf") if calculated_unity_check == 0 else 1 / calculated_unity_check
                if abs(self.factor_of_safety - calculated_factor_of_safety) >= TOLERANCE:
                    raise ValueError("Inconsistent CheckResult: provided/limit and factor_of_safety")
            if self.is_ok is not None and (calculated_unity_check > 1) == self.is_ok:
                raise ValueError("Inconsistent CheckResult: provided/limit and is_ok")

            # Fill in missing unity_check or factor_of_safety when it passes the above checks
            if self.unity_check is None:
                self.unity_check = calculated_unity_check
            if self.factor_of_safety is None:
                self.factor_of_safety = float("inf") if calculated_unity_check == 0 else 1 / calculated_unity_check

        # Consistency between unity_check and factor_of_safety, account for zero division
        if (
            self.unity_check is not None
            and self.factor_of_safety is not None  # Both provided
            and (
                (self.factor_of_safety == 0 and self.unity_check != float("inf"))  # Division by zero case
                or (self.factor_of_safety != 0 and abs(self.unity_check - 1 / self.factor_of_safety) >= TOLERANCE)  # Normal case
            )
        ):
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

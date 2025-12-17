"""Result data structure for structural checks."""

from dataclasses import dataclass

from blueprints.validations import raise_if_negative

TOLERANCE = 1e-6


@dataclass(frozen=True)
class CheckResult:
    """
    Contains the results of an engineering check.

    This class stores the outcome of any verification, providing both pass/fail status and detailed information about capacity
    utilization or factor of safety. Use this to understand whether your design meets code requirements and how
    efficiently you're using the available capacity.

    Recommended initialization methods:
    - `from_comparison(provided: float, required: float, operator: str = "<=")`:
        Create a CheckResult from direct provided and required values with a comparison operator.
    - `from_unity_check(unity_check: float)`:
        Create a CheckResult from a unity check value (provided/required).
    - `from_factor_of_safety(factor_of_safety: float)`:
        Create a CheckResult from a factor of safety value (required/provided).
    - `from_bool(is_ok: bool)`:
        Create a CheckResult from a simple pass/fail boolean.

    Initialization notes:
    - When only `is_ok` is provided: the other fields will remain None.
    - When `unity_check` is provided: `factor_of_safety` and `is_ok` will be inferred.
    - When `factor_of_safety` is provided: `unity_check` and `is_ok` will be inferred.
    - When both `provided` and `required` (with optional operator) are provided:
      `unity_check`, `factor_of_safety`, and `is_ok` will be calculated based on the operator.
      Special handling is applied for zero values and "==" or "!=" operators to avoid division by zero and ensure meaningful results.

    Direct initialization:
    - Ensure that the combination of fields provided is consistent.
      For example:
        - CheckResult(is_ok=True, unity_check=0.8) is valid.
        - CheckResult(is_ok=False, unity_check=0.8) will raise a ValueError.

    Parameters
    ----------
    provided : float | None, optional
        The actual calculated value from the design (e.g., applied load, stress).
    required : float | None, optional
        The allowable or required value for the design (e.g., capacity, code required).
    operator : str, optional
        The comparison operator used to evaluate the check: "<", "<=", "==", ">=", ">", or "!=".
        Default is "<=", meaning provided <= required.
    unity_check : float | None, optional
        The ratio of provided to required (provided / required).
        Values <= 1.0 indicate passing checks.
    factor_of_safety : float | None, optional
        The factor of safety (required / provided).
        Values >= 1.0 indicate passing checks.
    is_ok : bool | None, optional
        Indicates whether the check passed (True) or failed (False).
        If None, it will be inferred from `unity_check` or `factor_of_safety` if available.

    Notes
    -----
    - Always check `is_ok` to determine if design modifications are needed.
    - Use `unity_check` to optimize your design efficiency.
    - Use `factor_of_safety` to understand safety margins.
    - Values close to 1.0 indicate efficient but potentially risky designs.
    """

    provided: float | None = None
    required: float | None = None
    operator: str = Literal["<", "<=", "==", ">=", ">", "!="] = "<="
    unity_check: float | None = None
    factor_of_safety: float | None = None
    is_ok: bool | None = None

    @classmethod
    def from_comparison(cls, provided: float, required: float, operator: str = Literal["<", "<=", "==", ">=", ">", "!="] = "<=") -> Self:
        """
        Create a CheckResult from a direct comparison of provided and required values.
        Will automatically calculate unity_check, factor_of_safety, and is_ok.

        Please note: When either `provided` or `required` is zero, or the operator is "==" or "!=", special handling is applied
        to avoid division by zero and ensure meaningful results. Unity check and factor of safety calculations are adjusted such
        that they yield either 0.0 or infinity in these edge cases, reflecting pass/fail status appropriately.

        Example
        -------
        - CheckResult.from_comparison(provided=80, required=100, operator="<=")
          -> CheckResult with unity_check=0.8, factor_of_safety=1.25, is_ok=True
        - CheckResult.from_comparison(provided=120, required=100, operator="==")
          -> CheckResult with unity_check=inf, factor_of_safety=0.0, is_ok=False
        - CheckResult.from_comparison(provided=0, required=10, operator="<=")
          -> CheckResult with unity_check=0.0, factor_of_safety=inf, is_ok=True

        Parameters
        ----------
        provided : float
            The actual value from the design (e.g., applied load, stress).
        required : float
            The allowable or required value (e.g., capacity, code required).
        operator : str, optional
            The comparison operator ("<", "<=", "==", ">=", ">", "!="). Default is "<=".

        Returns
        -------
        CheckResult
            A new CheckResult instance with the specified values.
        """
        return cls(provided=provided, required=required, operator=operator)

    @classmethod
    def from_unity_check(cls, unity_check: float) -> Self:
        """
        Create a CheckResult from a unity check value (provided/required).

        Parameters
        ----------
        unity_check : float
            The ratio of provided to required (provided / required).
            Where values <= 1.0 indicate passing checks.

        Example
        -------
        - CheckResult.from_unity_check(unity_check=0.8)
          -> CheckResult with unity_check=0.8, factor_of_safety=1.25, is_ok=True, other fields None

        Returns
        -------
        CheckResult
            A new CheckResult instance with unity_check=unity_check.
        """
        return cls(unity_check=unity_check)

    @classmethod
    def from_factor_of_safety(cls, factor_of_safety: float) -> Self:
        """
        Create a CheckResult from a factor of safety value (required/provided).

        Parameters
        ----------
        factor_of_safety : float
            The factor of safety (required / provided).
            Where values >= 1.0 indicate passing checks.

        Example
        -------
        - CheckResult.from_factor_of_safety(factor_of_safety=1.25)
          -> CheckResult with factor_of_safety=1.25, unity_check=0.8, is_ok=True, other fields None

        Returns
        -------
        CheckResult
            A new CheckResult instance with factor_of_safety=factor_of_safety.
        """
        return cls(factor_of_safety=factor_of_safety)

    @classmethod
    def from_bool(cls, is_ok: bool) -> Self:
        """
        Create a CheckResult from a boolean pass/fail value only.

        Parameters
        ----------
        is_ok : bool
            Whether the check passed (True) or failed (False).

        Example
        -------
        - CheckResult.from_bool(is_ok=True)
          -> CheckResult with is_ok=True, other fields None

        Returns
        -------
        CheckResult
            A new CheckResult instance with only is_ok set.
        """
        return cls(is_ok=is_ok)

    def __post_init__(self) -> None:
        """Validate and synchronize unity_check, factor_of_safety, and is_ok."""
        self._validate_non_negativity()
        self._validate_operator()
        self._validate_provided_required_pair()
        self._handle_provided_required_consistency()
        self._check_unity_factor_consistency()
        self._check_is_ok_consistency()
        self._calculate_missing_unity_factor()
        self._infer_is_ok()

    def _validate_non_negativity(self) -> None:
        """Validate that all relevant fields are non-negative."""
        if self.unity_check is not None:
            raise_if_negative(unity_check=self.unity_check)
        if self.factor_of_safety is not None:
            raise_if_negative(factor_of_safety=self.factor_of_safety)
        if self.provided is not None:
            raise_if_negative(provided=self.provided)
        if self.required is not None:
            raise_if_negative(required=self.required)

    def _validate_operator(self) -> None:
        """Validate that the operator is one of the accepted values."""
        if self.operator not in ("<", "<=", "==", ">=", ">", "!="):
            raise ValueError(f"Invalid operator: {self.operator}. Must be one of '<', '<=', '==', '>=', '>' or '!='.")

    def _validate_provided_required_pair(self) -> None:
        """Ensure that provided and required are both None or both not None."""
        if (self.provided is None) != (self.required is None):
            raise ValueError("Both 'provided' and 'required' must be None or neither None")

    def _calc_unity_check(self, provided: float, required: float, operator: str) -> float:  # noqa: PLR0911
        """Calculate unity check based on provided, required, and operator."""
        if operator == "<":
            return float("inf") if required == 0 else provided / required
        if operator == "<=":
            return 0 if provided == 0 else float("inf") if required == 0 else provided / required
        if operator == ">=":
            return 0 if required == 0 else float("inf") if provided == 0 else required / provided
        if operator == ">":
            return float("inf") if provided == 0 else required / provided
        if operator == "==":
            # For "==", unity_check is 0 if values are close, else inf
            if provided == 0 and required == 0:
                return 0
            return 0 if abs(provided - required) / max(provided, required) <= TOLERANCE else float("inf")
        # For "!=" operator, unity_check is inf if values are close, else 0
        if provided == 0 and required == 0:
            return float("inf")
        return float("inf") if abs(provided - required) / max(provided, required) <= TOLERANCE else 0

    def _handle_provided_required_consistency(self) -> None:
        """
        If provided and required are given, check consistency with unity_check/factor_of_safety/is_ok.
        Fill in missing values if possible.
        """
        if self.provided is not None and self.required is not None:
            calculated_unity_check = self._calc_unity_check(self.provided, self.required, self.operator)

            # Consistency check with provided unity check
            if self.unity_check is not None and abs(self.unity_check - calculated_unity_check) >= TOLERANCE:
                raise ValueError("Inconsistent CheckResult: provided/required and unity_check")

            # Consistency check with provided factor_of_safety
            if self.factor_of_safety is not None:
                calculated_factor_of_safety = float("inf") if calculated_unity_check == 0 else 1 / calculated_unity_check
                if abs(self.factor_of_safety - calculated_factor_of_safety) >= TOLERANCE:
                    raise ValueError("Inconsistent CheckResult: provided/required and factor_of_safety")

            # Consistency check with provided is_ok
            if self.is_ok is not None and (calculated_unity_check > 1) == self.is_ok:
                raise ValueError("Inconsistent CheckResult: provided/required and is_ok")
            # Fill in missing unity_check or factor_of_safety or is_ok when it passes the above checks
            if self.unity_check is None:
                object.__setattr__(self, "unity_check", calculated_unity_check)
            if self.factor_of_safety is None:
                object.__setattr__(self, "factor_of_safety", float("inf") if calculated_unity_check == 0 else 1 / calculated_unity_check)
            if self.is_ok is None:
                # Determine pass/fail based on operator
                if self.operator in ("<", ">"):
                    object.__setattr__(self, "is_ok", calculated_unity_check < 1)
                else:  # operator in ("<=", ">=", "==", "!=")
                    object.__setattr__(self, "is_ok", calculated_unity_check <= 1)

    def _check_unity_factor_consistency(self) -> None:
        """Consistency between unity_check and factor_of_safety, account for zero division."""
        if (
            self.unity_check is not None
            and self.factor_of_safety is not None  # Both provided
            and (
                (self.factor_of_safety == 0 and self.unity_check != float("inf"))  # Division by zero case
                or (self.factor_of_safety != 0 and abs(self.unity_check - 1 / self.factor_of_safety) >= TOLERANCE)  # Normal case
            )
        ):
            raise ValueError("Inconsistent CheckResult: unity_check and factor_of_safety")

    def _check_is_ok_consistency(self) -> None:
        """Consistency between is_ok and unity_check/factor_of_safety."""
        if self.is_ok is not None:
            if self.operator in ("<", ">"):
                if self.unity_check is not None and (self.unity_check >= 1) == self.is_ok:
                    raise ValueError("Inconsistent CheckResult: unity_check and is_ok")
                if self.factor_of_safety is not None and (self.factor_of_safety <= 1) == self.is_ok:
                    raise ValueError("Inconsistent CheckResult: factor_of_safety and is_ok")
            else:  # operator in ("<=", ">=", "==", "!=")
                if self.unity_check is not None and (self.unity_check > 1) == self.is_ok:
                    raise ValueError("Inconsistent CheckResult: unity_check and is_ok")
                if self.factor_of_safety is not None and (self.factor_of_safety < 1) == self.is_ok:
                    raise ValueError("Inconsistent CheckResult: factor_of_safety and is_ok")

    def _calculate_missing_unity_factor(self) -> None:
        """Calculate missing value for unity_check or factor_of_safety."""
        if self.unity_check is None and self.factor_of_safety is not None:
            object.__setattr__(self, "unity_check", float("inf") if self.factor_of_safety == 0 else 1 / self.factor_of_safety)
        elif self.factor_of_safety is None and self.unity_check is not None:
            object.__setattr__(self, "factor_of_safety", float("inf") if self.unity_check == 0 else 1 / self.unity_check)

    def _infer_is_ok(self) -> None:
        """Infer is_ok if not given."""
        if self.is_ok is None and self.unity_check is not None:
            object.__setattr__(self, "is_ok", self.unity_check <= 1)

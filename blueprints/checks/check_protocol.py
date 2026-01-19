"""Universal protocol class for structural engineering checks."""

from typing import Protocol, runtime_checkable

from blueprints.checks.check_result import CheckResult
from blueprints.codes.formula import Formula
from blueprints.utils.report import Report


@runtime_checkable
class CheckProtocol(Protocol):
    """Protocol defining the interface for any Blueprint check.

    Any class implementing this protocol can be used as a structural check,
    regardless of inheritance. Provides maximum flexibility for simple checks
    that don't need to inherit from BaseCheck.

    Notes
    -----
    - Use for duck typing and structural subtyping
    - No inheritance required
    - Simple checks can implement this without BaseCheck inheritance
    - Enables both explicit (ABC) and implicit (Protocol) patterns

    Examples
    --------
    Simple check implementing protocol without inheritance:

    >>> @dataclass(frozen=True)
    ... class MyCheck:
    ...     name: str
    ...     source_docs: list[str]
    ...
    ...     def result(self) -> CheckResult: ...
    ...
    ...     def calculation_steps(self) -> dict[str, CheckProtocol]: ...
    ...
    ...     def report(self) -> Report: ...
    >>>
    >>> check = MyCheck(name="My Check", source_docs=["EN 1992"])
    >>> isinstance(check, CheckProtocol)  # True
    """

    name: str
    source_docs: list[str]

    def result(self) -> CheckResult:
        """Execute check and return standardized result.

        This is the primary public API method. Call this to execute your
        structural check and get a pass/fail result in a standardized format.

        Returns
        -------
        CheckResult
            Standardized Blueprints result object.
        """
        ...

    def calculation_steps(self) -> dict[str, "CheckProtocol | Formula | None"]:
        """Get sub-check instances for composite checks.

        Access this method to get all Check instances that are part of an
        orchestrated check. Each returned check object has its own result(),
        calculation_steps(), and report() methods for detailed inspection.

        When the check consists of formula direct from the code, return Formula.

        When a calculation sub check is not code yet, return None.

        Returns
        -------
        dict[str, "CheckProtocol" | None]
            Dictionary mapping descriptive names to Check instances.
            Empty dict for simple checks with no sub-checks.

        """
        ...

    def report(self) -> Report:
        """Generate formatted report of check results.

        Produces human-readable reports in various formats for documentation.

        Returns
        -------
        Report
            Formatted report object summarizing check results.
        """
        ...

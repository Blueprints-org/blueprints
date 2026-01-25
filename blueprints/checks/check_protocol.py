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
    that don't need to inherit from a common base class.

    Notes
    -----
    - Use for duck typing and structural subtyping
    - No inheritance required
    - Simple checks can implement this without inheriting from a shared base class
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
    ...     def subchecks(self) -> dict[str, CheckProtocol]: ...
    ...
    ...     def calculation_formula(self) -> dict[str, Formula]: ...
    ...
    ...     def report(self) -> Report: ...
    >>>
    >>> check = MyCheck(name="My Check", source_docs=["EN 1992"])
    >>> isinstance(check, CheckProtocol)  # True
    """

    name: str
    source_docs: list[str]

    def subchecks(self) -> dict[str, "CheckProtocol"]:
        """Get sub-check instances for composite checks.

        For example, Check A may comprise sub-checks A1, A2, and A3.
        In that case, calling subchecks() on Check A would return a dict:
        {"A1": <Check A1 instance>,
         "A2": <Check A2 instance>,
         "A3": <Check A3 instance>}.
        }

        Access this method to get all Check instances that are part of an
        orchestrated check. Each returned check object has its own result(),
        calculation_steps(), and report() methods for detailed inspection.

        For simple (leaf) checks with no sub-checks, return an empty dict.

        Returns
        -------
        dict[str, CheckProtocol]
            Dictionary mapping descriptive names to Check instances.
            Empty dict for simple checks with no sub-checks.

        """
        ...

    def calculation_formula(self) -> dict[str, "Formula"]:
        """Get calculation formula instances for this check or its sub-checks.

        Access this method to get all formula instances that are part of an
        orchestrated check. Each returned check object has its own result(),
        calculation_formula(), and report() methods for detailed inspection.

        For simple (leaf) checks with no formulas, return an empty dict.

        Returns
        -------
        dict[str, Formula]
            Dictionary mapping descriptive names to Formula instances.
            Empty dict for simple checks with no formulas.
        """
        ...

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

    def report(self) -> Report:
        """Generate formatted report of check results.

        Produces human-readable reports in various formats for documentation.

        Returns
        -------
        Report
            Formatted report object summarizing check results.
        """
        ...

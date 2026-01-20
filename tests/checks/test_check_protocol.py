"""Unit tests for the CheckProtocol implementations."""

from dataclasses import dataclass, field
from typing import Any, ClassVar

import pytest

from blueprints.checks._check_protocol import CheckProtocol
from blueprints.checks.check_result import CheckResult
from blueprints.utils.report import Report


@dataclass
class ValidCheck:
    """A valid implementation of the CheckProtocol."""

    name: str = "Valid Check"
    source_docs: list[str] = field(default_factory=lambda: ["Doc 1"])

    def result(self) -> CheckResult:
        """Return a valid result."""
        return CheckResult(is_ok=True)

    def calculation_steps(self) -> dict[str, CheckProtocol]:
        """Return empty calculation steps."""
        return {}

    def report(self) -> Report:
        """Return a valid report."""
        return Report(title=self.name)


class MissingNameCheck:
    """Missing the 'name' attribute."""

    source_docs: ClassVar[list[str]] = ["Doc 1"]

    def result(self) -> CheckResult:
        """Return a valid result."""
        return CheckResult(is_ok=True)

    def calculation_steps(self) -> dict[str, CheckProtocol]:
        """Return empty calculation steps."""
        return {}

    def report(self) -> Report:
        """Return a valid report."""
        return Report(title="Missing Name")


class MissingDocsCheck:
    """Missing the 'source_docs' attribute."""

    name: str = "Missing Docs"

    def result(self) -> CheckResult:
        """Return a valid result."""
        return CheckResult(is_ok=True)

    def calculation_steps(self) -> dict[str, CheckProtocol]:
        """Return empty calculation steps."""
        return {}

    def report(self) -> Report:
        """Return a valid report."""
        return Report(title=self.name)


class MissingResultCheck:
    """Missing the 'result' method."""

    name: str = "Missing Result"
    source_docs: ClassVar[list[str]] = ["Doc 1"]

    def calculation_steps(self) -> dict[str, CheckProtocol]:
        """Return empty calculation steps."""
        return {}

    def report(self) -> Report:
        """Return a valid report."""
        return Report(title=self.name)


class MissingStepsCheck:
    """Missing the 'calculation_steps' method."""

    name: str = "Missing Steps"
    source_docs: ClassVar[list[str]] = ["Doc 1"]

    def result(self) -> CheckResult:
        """Return a valid result."""
        return CheckResult(is_ok=True)

    def report(self) -> Report:
        """Return a valid report."""
        return Report(title=self.name)


class MissingReportCheck:
    """Missing the 'report' method."""

    name: str = "Missing Report"
    source_docs: ClassVar[list[str]] = ["Doc 1"]

    def result(self) -> CheckResult:
        """Return a valid result."""
        return CheckResult(is_ok=True)

    def calculation_steps(self) -> dict[str, CheckProtocol]:
        """Return empty calculation steps."""
        return {}


def test_valid_check_implementation() -> None:
    """Test that a complete implementation satisfies the protocol."""
    check = ValidCheck()
    assert isinstance(check, CheckProtocol)


@pytest.mark.parametrize(
    "invalid_check_class",
    [
        MissingNameCheck,
        MissingDocsCheck,
        MissingResultCheck,
        MissingStepsCheck,
        MissingReportCheck,
    ],
)
def test_invalid_check_implementations(invalid_check_class: Any) -> None:  # noqa: ANN401
    """Test that incomplete implementations do not satisfy the protocol."""
    check = invalid_check_class()
    assert not isinstance(check, CheckProtocol)

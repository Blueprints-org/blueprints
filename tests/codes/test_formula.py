"""Module for testing the Formula class."""

import pytest

from blueprints.codes.formula import Formula


class FormulaTest(Formula):
    """Dummy formula for testing purposes."""

    label = "Dummy testing formula"
    source_document = "Dummy testing document"

    def __init__(
        self,
        first: float,
        second: float,
    ) -> None:
        """Dummy formula for testing purposes."""
        super().__init__()
        self.first = first
        self.second = second

    @staticmethod
    def _evaluate(
        first: float,
        second: float,
    ) -> float:
        """Dummy formula for testing purposes."""
        return first + second


def test_raise_error_when_changing_value_after_initialization() -> None:
    """Test that an error is raised when changing a value after initialization."""
    # example values
    first = 1
    second = 2
    dummy_testing_formula = FormulaTest(first=first, second=second)
    with pytest.raises(AttributeError):
        dummy_testing_formula.first = 3


def test_raise_not_implemented_error_detailed_result() -> None:
    """Test that an error is raised when the detailed result is not implemented."""
    # example values
    first = 1
    second = 2
    dummy_testing_formula = FormulaTest(first=first, second=second)
    with pytest.raises(NotImplementedError):
        _ = dummy_testing_formula.detailed_result

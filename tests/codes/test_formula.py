"""Module for testing the Formula class."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.formula import Formula


class TestFormula(Formula):
    """Dummy formula for testing purposes."""

    label = "Dummy testing formula"
    source_document = "Dummy testing document"

    def __init__(
        self,
        a: float,
        b: float,
    ) -> None:
        """Dummy formula for testing purposes."""
        super().__init__()
        self.a = a
        self.b = b

    @staticmethod
    def _evaluate(
        a: float,
        b: float,
    ) -> float:
        """Dummy formula for testing purposes."""
        return a + b


def test_raise_error_when_changing_value_after_initialization() -> None:
    """Test that an error is raised when changing a value after initialization."""
    # example values
    a = 1
    b = 2
    dummy_testing_formula = TestFormula(a=a, b=b)
    with pytest.raises(AttributeError):
        dummy_testing_formula.a = 3


def test_raise_not_implemented_error_detailed_result() -> None:
    """Test that an error is raised when the detailed result is not implemented."""
    # example values
    a = 1
    b = 2
    dummy_testing_formula = TestFormula(a=a, b=b)
    with pytest.raises(NotImplementedError):
        _ = dummy_testing_formula.detailed_result

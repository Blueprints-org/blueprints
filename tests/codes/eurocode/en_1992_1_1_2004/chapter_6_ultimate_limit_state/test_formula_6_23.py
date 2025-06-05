"""Testing formula 6.23 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_23 import Form6Dot23CheckShearStressInterface
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot23CheckShearStressInterface:
    """Validation for formula 6.23 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_edi = 1.0
        v_rdi = 1.5

        # Object to test
        formula = Form6Dot23CheckShearStressInterface(v_edi=v_edi, v_rdi=v_rdi)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("v_edi", "v_rdi"),
        [
            (-1.0, 1.5),  # v_edi is negative
            (1.0, -1.5),  # v_rdi is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, v_edi: float, v_rdi: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot23CheckShearStressInterface(v_edi=v_edi, v_rdi=v_rdi)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to v_{Edi} \leq v_{Rdi} \to 1.000 \leq 1.500 \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_edi = 1.0
        v_rdi = 1.5

        # Object to test
        latex = Form6Dot23CheckShearStressInterface(v_edi=v_edi, v_rdi=v_rdi).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

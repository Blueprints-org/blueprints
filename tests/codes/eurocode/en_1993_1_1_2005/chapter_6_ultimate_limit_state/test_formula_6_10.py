"""Testing formula 6.10 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_10 import Form6Dot10NcRdClass1And2And3
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot10NcRdClass1And2And3:
    """Validation for formula 6.10 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a = 2000.0
        f_y = 355.0
        gamma_m0 = 1.0

        # Object to test
        formula = Form6Dot10NcRdClass1And2And3(a=a, f_y=f_y, gamma_m0=gamma_m0)

        # Expected result, manually calculated
        manually_calculated_result = 710000.0  # N

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a", "f_y", "gamma_m0"),
        [
            (-2000.0, 355.0, 1.0),  # a is negative
            (2000.0, -355.0, 1.0),  # f_y is negative
            (2000.0, 355.0, 0.0),  # gamma_m0 is zero
            (2000.0, 355.0, -1.0),  # gamma_m0 is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a: float, f_y: float, gamma_m0: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot10NcRdClass1And2And3(a=a, f_y=f_y, gamma_m0=gamma_m0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"N_{c,Rd} = \frac{A \cdot f_y}{\gamma_{M0}} = \frac{2000.000 \cdot 355.000}{1.000} = 710000.000 \ N",
            ),
            ("short", r"N_{c,Rd} = 710000.000 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a = 2000.0
        f_y = 355.0
        gamma_m0 = 1.0

        # Object to test
        latex = Form6Dot10NcRdClass1And2And3(a=a, f_y=f_y, gamma_m0=gamma_m0).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

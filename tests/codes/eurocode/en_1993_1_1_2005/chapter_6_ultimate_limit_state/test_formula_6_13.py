"""Testing formula 6.13 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_13 import Form6Dot13MCRdClass1And2
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot13MCRdClass1And2Class1And2:
    """Validation for formula 6.13 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        w_pl = 5000.0
        f_y = 355.0
        gamma_m0 = 1.0

        # Object to test
        formula = Form6Dot13MCRdClass1And2(w_pl=w_pl, f_y=f_y, gamma_m0=gamma_m0)

        # Expected result, manually calculated
        manually_calculated_result = 1775000.0  # Nmm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("w_pl", "f_y", "gamma_m0"),
        [
            (-5000.0, 355.0, 1.0),  # w_pl is negative
            (5000.0, -355.0, 1.0),  # f_y is negative
            (5000.0, 355.0, -1.0),  # gamma_m0 is negative
            (5000.0, 355.0, 0.0),  # gamma_m0 is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, w_pl: float, f_y: float, gamma_m0: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot13MCRdClass1And2(w_pl=w_pl, f_y=f_y, gamma_m0=gamma_m0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"M_{c,Rd} = \frac{W_{pl} \cdot f_y}{\gamma_{M0}} = \frac{5000.000 \cdot 355.000}{1.000} = 1775000.000 \ Nmm",
            ),
            ("short", r"M_{c,Rd} = 1775000.000 \ Nmm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        w_pl = 5000.0
        f_y = 355.0
        gamma_m0 = 1.0

        # Object to test
        latex = Form6Dot13MCRdClass1And2(w_pl=w_pl, f_y=f_y, gamma_m0=gamma_m0).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

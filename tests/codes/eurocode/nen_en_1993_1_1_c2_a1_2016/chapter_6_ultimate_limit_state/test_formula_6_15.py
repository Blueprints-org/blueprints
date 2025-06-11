"""Testing formula 6.15 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_15 import Form6Dot15McRdClass4
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot15McRdClass4:
    """Validation for formula 6.15 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        w_eff_min = 2000.0
        f_y = 355.0
        gamma_m0 = 1.0

        # Object to test
        formula = Form6Dot15McRdClass4(w_eff_min=w_eff_min, f_y=f_y, gamma_m0=gamma_m0)

        # Expected result, manually calculated
        manually_calculated_result = 710000.0  # Nmm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("w_eff_min", "f_y", "gamma_m0"),
        [
            (-2000.0, 355.0, 1.0),  # w_eff_min is negative
            (2000.0, -355.0, 1.0),  # f_y is negative
            (2000.0, 355.0, -1.0),  # gamma_m0 is negative
            (2000.0, 355.0, 0.0),  # gamma_m0 is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, w_eff_min: float, f_y: float, gamma_m0: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot15McRdClass4(w_eff_min=w_eff_min, f_y=f_y, gamma_m0=gamma_m0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"M_{c,Rd} = \frac{W_{eff,min} \cdot f_y}{\gamma_{M0}} = "
                r"\frac{2000.000 \cdot 355.000}{1.000} = 710000.000 \ Nmm",
            ),
            ("short", r"M_{c,Rd} = 710000.000 \ Nmm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        w_eff_min = 2000.0
        f_y = 355.0
        gamma_m0 = 1.0

        # Object to test
        latex = Form6Dot15McRdClass4(w_eff_min=w_eff_min, f_y=f_y, gamma_m0=gamma_m0).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

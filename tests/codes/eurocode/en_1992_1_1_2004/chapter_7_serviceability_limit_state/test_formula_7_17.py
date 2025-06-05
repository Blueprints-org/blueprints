"""Testing formula 7.17 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_7_serviceability_limit_state.formula_7_17 import (
    Form7Dot1MultiplicationFactorLimitSlenderness,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm7Dot1MultiplicationFactorLimitSlenderness:
    """Validation for formula 7.17 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        f_yk = 500.0
        a_s_req = 200.0
        a_s_prov = 250.0

        # Object to test
        formula = Form7Dot1MultiplicationFactorLimitSlenderness(f_yk=f_yk, a_s_req=a_s_req, a_s_prov=a_s_prov)

        # Expected result, manually calculated
        manually_calculated_result = 1.25  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("f_yk", "a_s_req", "a_s_prov"),
        [
            (-500.0, 200.0, 250.0),  # f_yk is negative
            (500.0, -200.0, 250.0),  # a_s_req is negative
            (500.0, 200.0, -250.0),  # a_s_prov is negative
            (500.0, 0.0, 250.0),  # a_s_req is zero
            (500.0, 200.0, 0.0),  # a_s_prov is zero
            (0.0, 200.0, 250.0),  # f_yk is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, f_yk: float, a_s_req: float, a_s_prov: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form7Dot1MultiplicationFactorLimitSlenderness(f_yk=f_yk, a_s_req=a_s_req, a_s_prov=a_s_prov)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\frac{310}{\sigma_s} = \frac{500}{f_{yk} \cdot \frac{A_{s,req}}{A_{s,prov}}} = "
                r"\frac{500}{500.000 \cdot \frac{200.000}{250.000}} = 1.250 \ -",
            ),
            ("short", r"\frac{310}{\sigma_s} = 1.250 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_yk = 500.0
        a_s_req = 200.0
        a_s_prov = 250.0

        # Object to test
        latex = Form7Dot1MultiplicationFactorLimitSlenderness(f_yk=f_yk, a_s_req=a_s_req, a_s_prov=a_s_prov).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

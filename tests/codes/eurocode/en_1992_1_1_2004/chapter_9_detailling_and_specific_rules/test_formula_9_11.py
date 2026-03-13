"""Testing formula 9.11 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_9_detailling_and_specific_rules.formula_9_11 import Form9Dot11MinimumShearReinforcement
from blueprints.validations import GreaterThan90Error, LessOrEqualToZeroError, NegativeValueError


class TestForm9Dot11MinimumShearReinforcement:
    """Validation for formula 9.11 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        alpha = 45.0
        s_r = 200.0
        s_t = 200.0
        f_ck = 30.0
        f_yk = 500.0

        # Object to test
        formula = Form9Dot11MinimumShearReinforcement(alpha=alpha, s_r=s_r, s_t=s_t, f_ck=f_ck, f_yk=f_yk)

        # Expected result, manually calculated
        manually_calculated_result = 19.8296747326  # mm^2

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("alpha", "s_r", "s_t", "f_ck", "f_yk"),
        [
            (-45.0, 200.0, 200.0, 30.0, 500.0),  # alpha is negative
            (45.0, -200.0, 200.0, 30.0, 500.0),  # s_r is negative
            (45.0, 200.0, -200.0, 30.0, 500.0),  # s_t is negative
            (45.0, 200.0, 200.0, -30.0, 500.0),  # f_ck is negative
            (45.0, 200.0, 200.0, 30.0, -500.0),  # f_yk is negative
            (45.0, 0.0, 200.0, 30.0, 500.0),  # s_r is zero
            (45.0, 200.0, 0.0, 30.0, 500.0),  # s_t is zero
            (45.0, 200.0, 200.0, 30.0, 0.0),  # f_yk is zero
            (91.0, 200.0, 200.0, 30.0, 500.0),  # alpha is greater than 90
        ],
    )
    def test_raise_error_when_invalid_values_are_given_zero_or_negative(self, alpha: float, s_r: float, s_t: float, f_ck: float, f_yk: float) -> None:
        """Test invalid values that are zero or negative."""
        with pytest.raises((LessOrEqualToZeroError, NegativeValueError, GreaterThan90Error)):
            Form9Dot11MinimumShearReinforcement(alpha=alpha, s_r=s_r, s_t=s_t, f_ck=f_ck, f_yk=f_yk)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"A_{sw,min} = \frac{0.08 \cdot \sqrt{f_{ck}}}{f_{yk}} \cdot \frac{s_r \cdot s_t}"
                r"{1.5 \cdot \sin(\alpha) + \cos(\alpha)} = "
                r"\frac{0.08 \cdot \sqrt{30.000}}{500.000} \cdot \frac{200.000 \cdot 200.000}{1.5 \cdot \sin(45.000) "
                r"+ \cos(45.000)} = 19.830 \ mm^2",
            ),
            ("short", r"A_{sw,min} = 19.830 \ mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        alpha = 45.0
        s_r = 200.0
        s_t = 200.0
        f_ck = 30.0
        f_yk = 500.0

        # Object to test
        latex = Form9Dot11MinimumShearReinforcement(alpha=alpha, s_r=s_r, s_t=s_t, f_ck=f_ck, f_yk=f_yk).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

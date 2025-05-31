"""Testing formula 9.1N of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_9_detailling_and_specific_rules.formula_9_1n import (
    Form9Dot1nMinimumTensileReinforcementBeam,
)
from blueprints.validations import NegativeValueError


class TestForm9Dot1nMinimumTensileReinforcementBeam:
    """Validation for formula 9.1N from EN 1992-1-1:2004."""

    def test_evaluation_first_term_decisive(self) -> None:
        """Test the evaluation of the result, if the first term of the formula is decisive."""
        # Example values
        f_ctm = 2  # MPa
        f_yk = 355  # MPa
        b_t = 50  # mm
        d = 150  # mm
        form_9_1n = Form9Dot1nMinimumTensileReinforcementBeam(f_ctm=f_ctm, f_yk=f_yk, b_t=b_t, d=d)

        # Expected result, manually calculated
        manually_calculated_result = 780 / 71

        assert form_9_1n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_second_term_decisive(self) -> None:
        """Test the evaluation of the result, if the second term of the formula is decisive."""
        # Example values
        f_ctm = 2  # MPa
        f_yk = 540  # MPa
        b_t = 50  # mm
        d = 150  # mm
        form_9_1n = Form9Dot1nMinimumTensileReinforcementBeam(f_ctm=f_ctm, f_yk=f_yk, b_t=b_t, d=d)

        # Expected result, manually calculated
        manually_calculated_result = 39 / 4

        assert form_9_1n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_f_ctm_is_given(self) -> None:
        """Test if error is raised when f_ctm is negative."""
        # Example values
        f_ctm = -2  # MPa
        f_yk = 355  # MPa
        b_t = 50  # mm
        d = 150  # mm

        with pytest.raises(NegativeValueError):
            Form9Dot1nMinimumTensileReinforcementBeam(f_ctm=f_ctm, f_yk=f_yk, b_t=b_t, d=d)

    def test_raise_error_when_negative_f_yk_is_given(self) -> None:
        """Test if error is raised when f_yk is negative."""
        # Example values
        f_ctm = 2  # MPa
        f_yk = -355  # MPa
        b_t = 50  # mm
        d = 150  # mm

        with pytest.raises(NegativeValueError):
            Form9Dot1nMinimumTensileReinforcementBeam(f_ctm=f_ctm, f_yk=f_yk, b_t=b_t, d=d)

    def test_raise_error_when_negative_b_t_is_given(self) -> None:
        """Test if error is raised when b_t is negative."""
        # Example values
        f_ctm = 2  # MPa
        f_yk = 355  # MPa
        b_t = -50  # mm
        d = 150  # mm

        with pytest.raises(NegativeValueError):
            Form9Dot1nMinimumTensileReinforcementBeam(f_ctm=f_ctm, f_yk=f_yk, b_t=b_t, d=d)

    def test_raise_error_when_negative_d_is_given(self) -> None:
        """Test if error is raised when d is negative."""
        # Example values
        f_ctm = 2  # MPa
        f_yk = 355  # MPa
        b_t = 50  # mm
        d = -150  # mm

        with pytest.raises(NegativeValueError):
            Form9Dot1nMinimumTensileReinforcementBeam(f_ctm=f_ctm, f_yk=f_yk, b_t=b_t, d=d)

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            (
                "complete",
                r"A_{s,min} = \max \left\{0.26 \cdot \frac{f_{ctm}}{f_{yk}} \cdot b_t \cdot d; 0.0013 \cdot b_t \cdot d\right\} = "
                r"\max \left\{0.26 \cdot \frac{2.00}{355.00} \cdot 50.00 \cdot 150.00; 0.0013 \cdot 50.00 \cdot 150.00\right\} = 10.99",
            ),
            ("short", "A_{s,min} = 10.99"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the latex representation."""
        # Example values
        f_ctm = 2  # MPa
        f_yk = 355  # MPa
        b_t = 50  # mm
        d = 150  # mm

        latex = Form9Dot1nMinimumTensileReinforcementBeam(f_ctm=f_ctm, f_yk=f_yk, b_t=b_t, d=d).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."

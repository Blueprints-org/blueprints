"""Testing formula 9.4 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_9_detailling_and_specific_rules.formula_9_4 import Form9Dot4ShearReinforcementRatio
from blueprints.validations import GreaterThan90Error, NegativeValueError


class TestForm9Dot4ShearReinforcementRatio:
    """Validation for formula 9.4 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        a_sw = 100  # mm²
        s = 200  # mm
        b_w = 150  # mm
        alpha = 85  # deg
        form_9_4 = Form9Dot4ShearReinforcementRatio(
            a_sw=a_sw,
            s=s,
            b_w=b_w,
            alpha=alpha,
        )

        # Expected result, manually calculated
        manually_calculated_result = 0.003346066

        assert form_9_4 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_a_sw_is_given(self) -> None:
        """Test if error is raised when a_sw is negative."""
        a_sw = -100  # mm²
        s = 200  # mm
        b_w = 150  # mm
        alpha = 85  # deg

        with pytest.raises(NegativeValueError):
            Form9Dot4ShearReinforcementRatio(
                a_sw=a_sw,
                s=s,
                b_w=b_w,
                alpha=alpha,
            )

    def test_raise_error_when_negative_s_is_given(self) -> None:
        """Test if error is raised when s is negative."""
        a_sw = 100  # mm²
        s = -200  # mm
        b_w = 150  # mm
        alpha = 85  # deg

        with pytest.raises(NegativeValueError):
            Form9Dot4ShearReinforcementRatio(
                a_sw=a_sw,
                s=s,
                b_w=b_w,
                alpha=alpha,
            )

    def test_raise_error_when_negative_b_w_is_given(self) -> None:
        """Test if error is raised when b_w is negative."""
        a_sw = 100  # mm²
        s = 200  # mm
        b_w = -150  # mm
        alpha = 85  # deg

        with pytest.raises(NegativeValueError):
            Form9Dot4ShearReinforcementRatio(
                a_sw=a_sw,
                s=s,
                b_w=b_w,
                alpha=alpha,
            )

    def test_raise_error_when_negative_alpha_is_given(self) -> None:
        """Test if error is raised when alpha is negative."""
        a_sw = 100  # mm²
        s = 200  # mm
        b_w = 150  # mm
        alpha = -85  # deg

        with pytest.raises(NegativeValueError):
            Form9Dot4ShearReinforcementRatio(
                a_sw=a_sw,
                s=s,
                b_w=b_w,
                alpha=alpha,
            )

    def test_raise_error_when_alpha_is_greater_90(self) -> None:
        """Test if error is raised when alpha is negative."""
        a_sw = 100  # mm²
        s = 200  # mm
        b_w = 150  # mm
        alpha = 110  # deg

        with pytest.raises(GreaterThan90Error):
            Form9Dot4ShearReinforcementRatio(
                a_sw=a_sw,
                s=s,
                b_w=b_w,
                alpha=alpha,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\rho_w = \frac{A_{sw}}{s \cdot b_w \cdot sin(\alpha)} = \frac{100.00}{200.00 \cdot 150.00 \cdot sin(85.00)} = 0.003346",
            ),
            ("short", r"\rho_w = 0.003346"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_sw = 100  # mm²
        s = 200  # mm
        b_w = 150  # mm
        alpha = 85  # deg

        # Object to test
        form_9_4_latex = Form9Dot4ShearReinforcementRatio(
            a_sw=a_sw,
            s=s,
            b_w=b_w,
            alpha=alpha,
        ).latex()

        actual = {"complete": form_9_4_latex.complete, "short": form_9_4_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

"""Testing formula 5.2 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_2 import Form5Dot2Eccentricity
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot2Eccentricity:
    """Validation for formula 5.2 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        theta_i = 0.003  # -
        l_0 = 5  # m
        form_5_2 = Form5Dot2Eccentricity(theta_i=theta_i, l_0=l_0)

        # Expected result, manually calculated
        manually_calculated_result = 0.0075

        assert form_5_2 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_theta_i_is_given(self) -> None:
        """Test a negative value for theta_i."""
        # Example values
        theta_i = -0.003  # -
        l_0 = 5  # m

        with pytest.raises(NegativeValueError):
            Form5Dot2Eccentricity(theta_i=theta_i, l_0=l_0)

    def test_raise_error_when_negative_l_0_is_given(self) -> None:
        """Test a negative value for l_0."""
        # Example values
        theta_i = 0.003  # -
        l_0 = -5  # m

        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot2Eccentricity(theta_i=theta_i, l_0=l_0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"e_i = \theta_i \cdot l_0 / 2 = 0.003 \cdot 5.000 / 2 = 0.0075",
            ),
            ("short", r"e_i = 0.0075"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        theta_i = 0.003  # -
        l_0 = 5  # m

        # Object to test
        form_5_2_latex = Form5Dot2Eccentricity(theta_i=theta_i, l_0=l_0).latex()

        actual = {
            "complete": form_5_2_latex.complete,
            "short": form_5_2_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."

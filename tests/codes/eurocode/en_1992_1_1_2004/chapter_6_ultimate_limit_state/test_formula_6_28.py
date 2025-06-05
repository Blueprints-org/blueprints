"""Testing formula 6.28 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_28 import Form6Dot28RequiredCrossSectionalArea
from blueprints.validations import GreaterThan90Error, LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot28RequiredCrossSectionalArea:
    """Validation for formula 6.28 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        u_k = 500.0
        f_yd = 435.0
        t_ed = 20.0
        a_k = 1000.0
        theta = 30.0

        # Object to test
        formula = Form6Dot28RequiredCrossSectionalArea(u_k=u_k, f_yd=f_yd, t_ed=t_ed, a_k=a_k, theta=theta)

        # Expected result, manually calculated
        manually_calculated_result = 0.01990862997  # mm2

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("u_k", "f_yd", "t_ed", "a_k", "theta"),
        [
            (-500.0, 435.0, 20.0, 1000.0, 30.0),  # u_k is negative
            (500.0, -435.0, 20.0, 1000.0, 30.0),  # f_yd is negative
            (500.0, 435.0, -20.0, 1000.0, 30.0),  # t_ed is negative
            (500.0, 435.0, 20.0, -1000.0, 30.0),  # a_k is negative
            (500.0, 435.0, 20.0, 1000.0, -30.0),  # theta is negative
            (500.0, 0.0, 20.0, 1000.0, 30.0),  # f_yd is zero
            (500.0, 435.0, 20.0, 0.0, 30.0),  # a_k is zero
            (500.0, 435.0, 20.0, 1000.0, 0.0),  # theta is zero
            (500.0, 435.0, 20.0, 1000.0, 91.0),  # theta is greater than 90
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, u_k: float, f_yd: float, t_ed: float, a_k: float, theta: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError, GreaterThan90Error)):
            Form6Dot28RequiredCrossSectionalArea(u_k=u_k, f_yd=f_yd, t_ed=t_ed, a_k=a_k, theta=theta)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\Sigma A_{sl} = \frac{u_k}{f_{yd}} \cdot \frac{T_{Ed}}{2 \cdot A_k} \cdot \cot(\theta) = "
                r"\frac{500.000}{435.000} \cdot \frac{20.000}{2 \cdot 1000.000} \cdot \cot(30.000) = 0.020 \ mm^2",
            ),
            ("short", r"\Sigma A_{sl} = 0.020 \ mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        u_k = 500.0
        f_yd = 435.0
        t_ed = 20.0
        a_k = 1000.0
        theta = 30.0

        # Object to test
        latex = Form6Dot28RequiredCrossSectionalArea(u_k=u_k, f_yd=f_yd, t_ed=t_ed, a_k=a_k, theta=theta).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

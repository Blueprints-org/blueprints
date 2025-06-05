"""Testing formula 6.43 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_43 import Form6Dot43BetaRectangular
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot43BetaRectangular:
    """Validation for formula 6.43 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        ey = 300.0
        ez = 200.0
        by = 400.0
        bz = 500.0

        # Object to test
        formula = Form6Dot43BetaRectangular(ey=ey, ez=ez, by=by, bz=bz)

        # Expected result, manually calculated
        manually_calculated_result = 2.405844942

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("ey", "ez", "by", "bz"),
        [
            (-300.0, 200.0, 400.0, 500.0),  # ey is negative
            (300.0, -200.0, 400.0, 500.0),  # ez is negative
            (300.0, 200.0, -400.0, 500.0),  # by is negative
            (300.0, 200.0, 400.0, -500.0),  # bz is negative
            (300.0, 200.0, 0.0, 500.0),  # by is zero
            (300.0, 200.0, 400.0, 0.0),  # bz is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, ey: float, ez: float, by: float, bz: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot43BetaRectangular(ey=ey, ez=ez, by=by, bz=bz)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\beta = 1 + 1.8 \cdot \sqrt{\left(\frac{e_y}{b_z}\right)^2 + \left(\frac{e_z}{b_y}\right)^2} "
                r"= 1 + 1.8 \cdot \sqrt{\left(\frac{300.000}{500.000}\right)^2 + \left(\frac{200.000}{400.000}\right)^2} = 2.406 \ -",
            ),
            ("short", r"\beta = 2.406 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        ey = 300.0
        ez = 200.0
        by = 400.0
        bz = 500.0

        # Object to test
        latex = Form6Dot43BetaRectangular(ey=ey, ez=ez, by=by, bz=bz).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

"""Testing formula 5.33 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_33 import Form5Dot33NominalSecondOrderMoment
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot33NominalSecondOrderMoment:
    """Validation for formula 5.33 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        n_ed = 100.0
        curvature = 0.01
        l_o = 5.0
        c = 10.0

        # Object to test
        formula = Form5Dot33NominalSecondOrderMoment(n_ed=n_ed, curvature=curvature, l_o=l_o, c=c)

        # Expected result, manually calculated
        manually_calculated_result = 2.5  # kNm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("n_ed", "curvature", "l_o", "c"),
        [
            (-100.0, 0.01, 5.0, 10.0),  # n_ed is negative
            (100.0, -0.01, 5.0, 10.0),  # curvature is negative
            (100.0, 0.01, -5.0, 10.0),  # l_o is negative
            (100.0, 0.01, 5.0, -10.0),  # c is negative
            (0.0, 0.01, 5.0, 10.0),  # n_ed is zero
            (100.0, 0.0, 5.0, 10.0),  # curvature is zero
            (100.0, 0.01, 0.0, 10.0),  # l_o is zero
            (100.0, 0.01, 5.0, 0.0),  # c is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, n_ed: float, curvature: float, l_o: float, c: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot33NominalSecondOrderMoment(n_ed=n_ed, curvature=curvature, l_o=l_o, c=c)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"M_{2} = N_{Ed} \cdot \left(\frac{1}{r}\right) \cdot \frac{l_{o}^2}{c} "
                r"= 100.000 \cdot \left(0.010\right) \cdot \frac{5.000^2}{10.000} = 2.500 \ kNm",
            ),
            ("short", r"M_{2} = 2.500 \ kNm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n_ed = 100.0
        curvature = 0.01
        l_o = 5.0
        c = 10

        # Object to test
        latex = Form5Dot33NominalSecondOrderMoment(n_ed=n_ed, curvature=curvature, l_o=l_o, c=c).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

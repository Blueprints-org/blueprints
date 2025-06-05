"""Testing formula 5.36 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_36 import Form5Dot36RelativeAxialForce
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot36RelativeAxialForce:
    """Validation for formula 5.36 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        n_ed = 100000.0
        ac = 2000.0
        fcd = 30.0
        as_ = 100.0
        fyd = 500.0
        n_bal = 0.4

        # Object to test
        formula = Form5Dot36RelativeAxialForce(n_ed=n_ed, ac=ac, fcd=fcd, as_=as_, fyd=fyd, n_bal=n_bal)

        # Expected result, manually calculated
        manually_calculated_result = 0.11627906976  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("n_ed", "ac", "fcd", "as_", "fyd", "n_bal"),
        [
            (-100000.0, 2000.0, 30.0, 100.0, 500.0, 0.4),  # n_ed is negative
            (100000.0, -2000.0, 30.0, 100.0, 500.0, 0.4),  # ac is negative
            (100000.0, 2000.0, -30.0, 100.0, 500.0, 0.4),  # fcd is negative
            (100000.0, 2000.0, 30.0, -100.0, 500.0, 0.4),  # as_ is negative
            (100000.0, 2000.0, 30.0, 100.0, -500.0, 0.4),  # fyd is negative
            (100000.0, 2000.0, 30.0, 100.0, 500.0, -0.4),  # n_bal is negative
            (100000.0, 0.0, 30.0, 100.0, 500.0, 0.4),  # ac is zero
            (100000.0, 2000.0, 0.0, 100.0, 500.0, 0.4),  # fcd is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, n_ed: float, ac: float, fcd: float, as_: float, fyd: float, n_bal: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot36RelativeAxialForce(n_ed=n_ed, ac=ac, fcd=fcd, as_=as_, fyd=fyd, n_bal=n_bal)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"K_{r} = \min\left(\frac{\left(1 + \frac{A_{s} \cdot f_{yd}}{A_{c} \cdot f_{cd}}\right) - "
                r"\frac{N_{Ed}}{A_{c} \cdot f_{cd}}}{\left(1 + \frac{A_{s} \cdot f_{yd}}{A_{c} \cdot f_{cd}}\right) - n_{bal}}, 1\right) "
                r"= \min\left(\frac{\left(1 + \frac{100.000 \cdot 500.000}{2000.000 \cdot 30.000}\right) - \frac{100000.000}"
                r"{2000.000 \cdot 30.000}}{\left(1 + \frac{100.000 \cdot 500.000}{2000.000 \cdot 30.000}\right) - 0.400}, 1\right) = 0.116 \ -",
            ),
            ("short", r"K_{r} = 0.116 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n_ed = 100000.0
        ac = 2000.0
        fcd = 30.0
        as_ = 100.0
        fyd = 500.0
        n_bal = 0.4

        # Object to test
        latex = Form5Dot36RelativeAxialForce(n_ed=n_ed, ac=ac, fcd=fcd, as_=as_, fyd=fyd, n_bal=n_bal).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

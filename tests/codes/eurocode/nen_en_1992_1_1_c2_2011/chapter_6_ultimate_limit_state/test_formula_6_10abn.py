"""Testing formula 6.10a/bN of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_6_ultimate_limit_state.formula_6_10abn import Form6Dot10abNStrengthReductionFactor
from blueprints.validations import NegativeValueError


class TestForm6Dot10abNStrengthReductionFactor:
    """Validation for formula 6.10a/bN from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation_above_60(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        f_ck = 75.0

        # Object to test
        formula = Form6Dot10abNStrengthReductionFactor(f_ck=f_ck)

        # Expected result, manually calculated
        manually_calculated_result = 0.525

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_below_60(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        f_ck = 30.0

        # Object to test
        formula = Form6Dot10abNStrengthReductionFactor(f_ck=f_ck)

        # Expected result, manually calculated
        manually_calculated_result = 0.6

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("f_ck"),
        [
            (-30.0),  # f_ck is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, f_ck: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form6Dot10abNStrengthReductionFactor(f_ck=f_ck)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\nu_{1} = \begin{cases} 0.600 & \text{if } f_{ck} \leq 60 MPa \\ \max\left(0.9 - \frac{f_{ck}}{200}, 0.5\right) "
                r"& \text{if } f_{ck} > 60 MPa \end{cases} = "
                r"\begin{cases} 0.600 & \text{if } 30.0 \leq 60 MPa \\ \max\left(0.9 - \frac{30.0}{200}, 0.5\right) "
                r"& \text{if } 30.0 > 60 MPa \end{cases} = 0.600 -",
            ),
            ("short", r"\nu_{1} = 0.600 -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_ck = 30.0

        # Object to test
        latex = Form6Dot10abNStrengthReductionFactor(f_ck=f_ck).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

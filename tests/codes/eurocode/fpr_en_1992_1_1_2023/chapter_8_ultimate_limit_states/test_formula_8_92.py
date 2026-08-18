"""Testing formula 8.92 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_92 import Form8Dot92DesignPunchingShearStress
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot92DesignPunchingShearStress:
    """Validation for formula 8.92 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values, an internal column with the approximated coefficient of Table 8.3
        beta_e = 1.15
        v_ed = 500000.0
        b_0_5 = 2400.0
        d_v = 200.0

        # Object to test
        formula = Form8Dot92DesignPunchingShearStress(beta_e=beta_e, v_ed=v_ed, b_0_5=b_0_5, d_v=d_v)

        # Expected result, manually calculated
        manually_calculated_result = 1.1979166667  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("beta_e", "v_ed", "b_0_5", "d_v"),
        [
            (-1.15, 500000.0, 2400.0, 200.0),  # beta_e is negative
            (1.15, -500000.0, 2400.0, 200.0),  # v_ed is negative
            (1.15, 500000.0, -2400.0, 200.0),  # b_0_5 is negative
            (1.15, 500000.0, 0.0, 200.0),  # b_0_5 is zero
            (1.15, 500000.0, 2400.0, -200.0),  # d_v is negative
            (1.15, 500000.0, 2400.0, 0.0),  # d_v is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, beta_e: float, v_ed: float, b_0_5: float, d_v: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot92DesignPunchingShearStress(beta_e=beta_e, v_ed=v_ed, b_0_5=b_0_5, d_v=d_v)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\tau_{Ed} = \beta_e \cdot \frac{V_{Ed}}{b_{0,5} \cdot d_v} = "
                    r"1.150 \cdot \frac{500000.000}{2400.000 \cdot 200.000} = 1.198 \ MPa"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\tau_{Ed} = \beta_e \cdot \frac{V_{Ed}}{b_{0,5} \cdot d_v} = "
                    r"1.150 \cdot \frac{500000.000 \ N}{2400.000 \ mm \cdot 200.000 \ mm} = 1.198 \ MPa"
                ),
            ),
            ("short", r"\tau_{Ed} = 1.198 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        beta_e = 1.15
        v_ed = 500000.0
        b_0_5 = 2400.0
        d_v = 200.0

        # Object to test
        latex = Form8Dot92DesignPunchingShearStress(beta_e=beta_e, v_ed=v_ed, b_0_5=b_0_5, d_v=d_v).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

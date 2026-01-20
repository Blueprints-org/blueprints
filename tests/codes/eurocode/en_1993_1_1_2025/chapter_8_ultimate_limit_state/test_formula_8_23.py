"""Testing formula 8.23 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2025.chapter_8_ultimate_limit_state.formula_8_23 import Form8Dot23DesignPlasticShearResistance
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot23DesignPlasticShearResistance:
    """Validation for formula 8.23 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_v = 2000.0
        f_y = 355.0
        gamma_m0 = 1.0

        # Object to test
        formula = Form8Dot23DesignPlasticShearResistance(a_v=a_v, f_y=f_y, gamma_m0=gamma_m0)

        # Expected result, manually calculated
        manually_calculated_result = 409918.6911246343  # N

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_v", "f_y", "gamma_m0"),
        [
            (-2000.0, 355.0, 1.0),  # a_v is negative
            (2000.0, -355.0, 1.0),  # f_y is negative
            (2000.0, 355.0, -1.0),  # gamma_m0 is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_v: float, f_y: float, gamma_m0: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot23DesignPlasticShearResistance(a_v=a_v, f_y=f_y, gamma_m0=gamma_m0)

    @pytest.mark.parametrize(
        ("a_v", "f_y", "gamma_m0"),
        [
            (2000.0, 355.0, 0.0),  # gamma_m0 is zero
            (2000.0, 355.0, -1.0),  # gamma_m0 is negative
        ],
    )
    def test_raise_error_when_gamma_m0_is_invalid(self, a_v: float, f_y: float, gamma_m0: float) -> None:
        """Test invalid gamma_m0 values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot23DesignPlasticShearResistance(a_v=a_v, f_y=f_y, gamma_m0=gamma_m0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"V_{pl,Rd} = \frac{A_v \cdot (f_y / \sqrt{3})}{\gamma_{M0}} = "
                r"\frac{2000.000 \cdot (355.000 / \sqrt{3})}{1.000} = 409918.691 \ N",
            ),
            ("short", r"V_{pl,Rd} = 409918.691 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_v = 2000.0
        f_y = 355.0
        gamma_m0 = 1.0

        # Object to test
        latex = Form8Dot23DesignPlasticShearResistance(a_v=a_v, f_y=f_y, gamma_m0=gamma_m0).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

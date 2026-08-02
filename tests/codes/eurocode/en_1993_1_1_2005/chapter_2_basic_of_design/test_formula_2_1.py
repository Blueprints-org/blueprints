"""Testing formula 2.1 from EN 1993-1-1:2005: Chapter 2: Basis of design."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_2_basic_of_design.formula_2_1 import Form2Dot1DesignValueResistance
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm2Dot1DesignValueResistance:
    """Validation for formula 2.1 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        r_k = 110.0  # N
        gamma_m = 1.1  # [-]

        formula = Form2Dot1DesignValueResistance(r_k=r_k, gamma_m=gamma_m)

        manually_calculated_result = 100.0  # N

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("r_k", "gamma_m", "expected_exception"),
        [
            (-110.0, 1.1, NegativeValueError),  # r_k is negative
            (110.0, -1.1, LessOrEqualToZeroError),  # gamma_m is negative
            (110.0, 0.0, LessOrEqualToZeroError),  # gamma_m is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self,
        r_k: float,
        gamma_m: float,
        expected_exception: type[Exception],
    ) -> None:
        """Test invalid values."""
        with pytest.raises(expected_exception):
            Form2Dot1DesignValueResistance(r_k=r_k, gamma_m=gamma_m)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"R_{d} = \frac{R_k}{\gamma_M} = \frac{110.000}{1.100} = 100.000 \ N",
            ),
            (
                "complete_with_units",
                r"R_{d} = \frac{R_k}{\gamma_M} = \frac{110.000 \ N}{1.100} = 100.000 \ N",
            ),
            ("short", r"R_{d} = 100.000 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the LaTeX representation of the formula."""
        r_k = 110.0  # N
        gamma_m = 1.1  # [-]

        latex = Form2Dot1DesignValueResistance(r_k=r_k, gamma_m=gamma_m).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

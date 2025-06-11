"""Testing formula 6.19 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_19 import (
    Form6Dot19CheckDesignElasticShearResistance,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot19CheckDesignElasticShearResistance:
    """Validation for formula 6.19 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        tau_ed = 100.0
        f_y = 355.0
        gamma_m0 = 1.0

        # Object to test
        formula = Form6Dot19CheckDesignElasticShearResistance(tau_ed=tau_ed, f_y=f_y, gamma_m0=gamma_m0)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("tau_ed", "f_y", "gamma_m0"),
        [
            (-100.0, 355.0, 1.0),  # tau_ed is negative
            (100.0, -355.0, 1.0),  # f_y is negative
            (100.0, 355.0, -1.0),  # gamma_m0 is negative
            (100.0, 0.0, 1.0),  # f_y is zero
            (100.0, 355.0, 0.0),  # gamma_m0 is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, tau_ed: float, f_y: float, gamma_m0: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot19CheckDesignElasticShearResistance(tau_ed=tau_ed, f_y=f_y, gamma_m0=gamma_m0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \left( \frac{\tau_{Ed}}{f_{y} / (\sqrt{3} \cdot \gamma_{M0})} \leq 1.0 \right) \to "
                r"\left( \frac{100.000}{355.000 / (\sqrt{3} \cdot 1.000)} \leq 1.0 \right) \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        tau_ed = 100.0
        f_y = 355.0
        gamma_m0 = 1.0

        # Object to test
        latex = Form6Dot19CheckDesignElasticShearResistance(tau_ed=tau_ed, f_y=f_y, gamma_m0=gamma_m0).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

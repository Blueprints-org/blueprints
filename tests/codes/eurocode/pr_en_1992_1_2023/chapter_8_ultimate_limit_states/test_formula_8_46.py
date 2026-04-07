"""Testing formula 8.46 of prEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.pr_en_1992_1_2023.chapter_8_ultimate_limit_states.formula_8_46 import Form8Dot46AverageStrainBottomTopChords
from blueprints.validations import NegativeValueError


class TestForm8Dot46AverageStrain:
    """Validation for formula 8.46 from prEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        epsilon_xt = 0.0032  # dimensionless
        epsilon_xc = 0.0004  # dimensionless

        # Object to test
        formula = Form8Dot46AverageStrainBottomTopChords(epsilon_xt=epsilon_xt, epsilon_xc=epsilon_xc)

        # Expected result
        expected_result = 0.0018

        assert expected_result == pytest.approx(formula, rel=1e-4)

    @pytest.mark.parametrize(
        ("epsilon_xt", "epsilon_xc"),
        [
            (-0.0032, 0.0004),  # epsilon_xt is negative
            (0.0032, -0.0004),  # epsilon_xc is negative
        ],
    )
    def test_raise_error_when_inputs_are_negative(self, epsilon_xt: float, epsilon_xc: float) -> None:
        """Test invalid values where a strain input is negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot46AverageStrainBottomTopChords(epsilon_xt=epsilon_xt, epsilon_xc=epsilon_xc)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\varepsilon_x = \frac{\varepsilon_{xt} + \varepsilon_{xc}}{2} = \frac{0.0032 + 0.0004}{2} = 0.0018 \ge 0 = 0.0018",
            ),
            (
                "complete_with_units",
                r"\varepsilon_x = \frac{\varepsilon_{xt} + \varepsilon_{xc}}{2} = \frac{0.0032 + 0.0004}{2} = 0.0018 \ge 0 = 0.0018",
            ),
            ("short", r"\varepsilon_x = 0.0018"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        epsilon_xt = 0.0032  # dimensionless
        epsilon_xc = 0.0004  # dimensionless

        # Object to test
        latex = Form8Dot46AverageStrainBottomTopChords(epsilon_xt=epsilon_xt, epsilon_xc=epsilon_xc).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

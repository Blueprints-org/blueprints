"""Testing formula 6.7 of NEN-EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_7 import (
    Form6Dot7DesignUltimateResistanceNetCrossSection,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot7DesignUltimateResistanceNetCrossSection:
    """Validation for formula 6.7 from NEN-EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_net = 2000.0
        f_u = 400.0
        gamma_m2 = 1.1

        # Object to test
        formula = Form6Dot7DesignUltimateResistanceNetCrossSection(a_net=a_net, f_u=f_u, gamma_m2=gamma_m2)

        # Expected result, manually calculated
        manually_calculated_result = 654545.454545454  # N

        assert formula == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_net", "f_u", "gamma_m2"),
        [
            (2000.0, 400.0, 0.0),  # gamma_m2 is zero
            (-2000.0, 400.0, 1.1),  # a_net is negative
            (2000.0, -400.0, 1.1),  # f_u is negative
            (2000.0, 400.0, -1.1),  # gamma_m2 is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_net: float, f_u: float, gamma_m2: float) -> None:
        """Test invalid values."""
        with pytest.raises((LessOrEqualToZeroError, NegativeValueError)):
            Form6Dot7DesignUltimateResistanceNetCrossSection(a_net=a_net, f_u=f_u, gamma_m2=gamma_m2)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"N_{u,Rd} = 0.9 \cdot \frac{A_{net} \cdot f_u}{\gamma_{M2}} = "
                r"0.9 \cdot \frac{2000.000 \cdot 400.000}{1.100} = 654545.455 \ N",
            ),
            ("short", r"N_{u,Rd} = 654545.455 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_net = 2000.0
        f_u = 400.0
        gamma_m2 = 1.1

        # Object to test
        latex = Form6Dot7DesignUltimateResistanceNetCrossSection(a_net=a_net, f_u=f_u, gamma_m2=gamma_m2).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

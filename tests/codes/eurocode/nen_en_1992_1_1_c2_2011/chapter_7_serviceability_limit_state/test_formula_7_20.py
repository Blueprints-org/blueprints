"""Testing formula 7.20 of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_7_serviceability_limit_state.formula_7_20 import Form7Dot20EffectiveModulus
from blueprints.validations import NegativeValueError


class TestForm7Dot20EffectiveModulus:
    """Validation for formula 7.20 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        e_cm = 30000.0  # MPa
        phi_inf_t0 = 2.0  # dimensionless

        # Object to test
        formula = Form7Dot20EffectiveModulus(e_cm=e_cm, phi_inf_t0=phi_inf_t0)

        # Expected result, manually calculated
        manually_calculated_result = 10000.0  # MPa

        assert formula == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("e_cm", "phi_inf_t0"),
        [
            (-30000.0, 2.0),  # e_cm is negative
            (30000.0, -2.0),  # phi_inf_t0 is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, e_cm: float, phi_inf_t0: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form7Dot20EffectiveModulus(e_cm=e_cm, phi_inf_t0=phi_inf_t0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"E_{c,eff} = \frac{E_{cm}}{1 + \phi(\infty , t_0)} = \frac{30000.000}{1 + 2.000} = 10000.000 \ MPa",
            ),
            ("short", r"E_{c,eff} = 10000.000 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        e_cm = 30000.0  # MPa
        phi_inf_t0 = 2.0  # dimensionless

        # Object to test
        latex = Form7Dot20EffectiveModulus(e_cm=e_cm, phi_inf_t0=phi_inf_t0).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

"""Testing formula 7.21 of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_7_serviceability_limit_state.formula_7_21 import Form7Dot21CurvatureDueToShrinkage
from blueprints.validations import NegativeValueError


class TestForm7Dot21CurvatureDueToShrinkage:
    """Validation for formula 7.21 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        epsilon_cs = 0.0003  # dimensionless
        es = 200000.0  # MPa
        ec_eff = 30000.0  # MPa
        s = 50000.0  # mm^3
        i = 200000.0  # mm^4

        # Object to test
        formula = Form7Dot21CurvatureDueToShrinkage(epsilon_cs=epsilon_cs, es=es, ec_eff=ec_eff, s=s, i=i)

        # Expected result, manually calculated
        manually_calculated_result = 0.0005  # dimensionless

        assert formula == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("epsilon_cs", "es", "ec_eff", "s", "i"),
        [
            (-0.0003, 200000.0, 30000.0, 50000.0, 200000.0),  # epsilon_cs is negative
            (0.0003, -200000.0, 30000.0, 50000.0, 200000.0),  # es is negative
            (0.0003, 200000.0, -30000.0, 50000.0, 200000.0),  # ec_eff is negative
            (0.0003, 200000.0, 30000.0, -50000.0, 200000.0),  # s is negative
            (0.0003, 200000.0, 30000.0, 50000.0, -200000.0),  # i is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, epsilon_cs: float, es: float, ec_eff: float, s: float, i: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form7Dot21CurvatureDueToShrinkage(epsilon_cs=epsilon_cs, es=es, ec_eff=ec_eff, s=s, i=i)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\frac{1}{r_{cs}} = \epsilon_{cs} \cdot \frac{E_s}{E_{c,eff}} \cdot \frac{S}{I} = "
                r"0.0003 \cdot \frac{200000.000}{30000.000} \cdot \frac{50000.000}{200000.000} = 0.000500 mm^{-1}",
            ),
            ("short", r"\frac{1}{r_{cs}} = 0.000500 mm^{-1}"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        epsilon_cs = 0.0003  # dimensionless
        es = 200000.0  # MPa
        ec_eff = 30000.0  # MPa
        s = 50000.0  # mm^3
        i = 200000.0  # mm^4

        # Object to test
        latex = Form7Dot21CurvatureDueToShrinkage(epsilon_cs=epsilon_cs, es=es, ec_eff=ec_eff, s=s, i=i).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

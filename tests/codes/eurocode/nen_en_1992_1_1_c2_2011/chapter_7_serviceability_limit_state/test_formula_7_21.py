"""Testing formula 7.21 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_7_serviceability_limit_state.formula_7_21 import Form7Dot21CurvatureDueToShrinkage
from blueprints.validations import NegativeValueError


class TestForm7Dot21CurvatureDueToShrinkage:
    """Validation for formula 7.21 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        epsilon_cs = 0.0003  # dimensionless
        es = 200000.0  # MPa
        ec_eff = 30000.0  # MPa
        capital_s = 50000.0  # mm^3
        capital_i = 200000.0  # mm^4

        # Object to test
        formula = Form7Dot21CurvatureDueToShrinkage(epsilon_cs=epsilon_cs, es=es, ec_eff=ec_eff, capital_s=capital_s, capital_i=capital_i)

        # Expected result, manually calculated
        manually_calculated_result = 0.0005  # dimensionless

        assert formula == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("epsilon_cs", "es", "ec_eff", "capital_s", "capital_i"),
        [
            (-0.0003, 200000.0, 30000.0, 50000.0, 200000.0),  # epsilon_cs is negative
            (0.0003, -200000.0, 30000.0, 50000.0, 200000.0),  # es is negative
            (0.0003, 200000.0, -30000.0, 50000.0, 200000.0),  # ec_eff is negative
            (0.0003, 200000.0, 30000.0, -50000.0, 200000.0),  # capital_s is negative
            (0.0003, 200000.0, 30000.0, 50000.0, -200000.0),  # capital_i is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, epsilon_cs: float, es: float, ec_eff: float, capital_s: float, capital_i: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form7Dot21CurvatureDueToShrinkage(epsilon_cs=epsilon_cs, es=es, ec_eff=ec_eff, capital_s=capital_s, capital_i=capital_i)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\frac{1}{r_{cs}} = \epsilon_{cs} \cdot \frac{E_s}{E_{c,eff}} \cdot \frac{S}{I} = "
                r"0.0003 \cdot \frac{200000.000}{30000.000} \cdot \frac{50000.000}{200000.000} = 0.000500 \ mm^{-1}",
            ),
            ("short", r"\frac{1}{r_{cs}} = 0.000500 \ mm^{-1}"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        epsilon_cs = 0.0003  # dimensionless
        es = 200000.0  # MPa
        ec_eff = 30000.0  # MPa
        capital_s = 50000.0  # mm^3
        capital_i = 200000.0  # mm^4

        # Object to test
        latex = Form7Dot21CurvatureDueToShrinkage(epsilon_cs=epsilon_cs, es=es, ec_eff=ec_eff, capital_s=capital_s, capital_i=capital_i).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

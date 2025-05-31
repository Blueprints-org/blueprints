"""Testing formula 5.39 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_39 import Form5Dot39SimplifiedCriterionBiaxialBending
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot39SimplifiedCriterionBiaxialBending:
    """Validation for formula 5.39 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        m_edz = 10.0  # KNM
        m_rdz = 20.0  # KNM
        m_edy = 15.0  # KNM
        m_rdy = 25.0  # KNM
        a = 0.8  # DIMENSIONLESS

        # Object to test
        formula = Form5Dot39SimplifiedCriterionBiaxialBending(m_edz=m_edz, m_rdz=m_rdz, m_edy=m_edy, m_rdy=m_rdy, a=a)

        # Expected result, manually calculated
        expected_result = False

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("m_edz", "m_rdz", "m_edy", "m_rdy", "a"),
        [
            (-10.0, 20.0, 15.0, 25.0, 0.8),  # m_edz is negative
            (10.0, -20.0, 15.0, 25.0, 0.8),  # m_rdz is negative
            (10.0, 20.0, -15.0, 25.0, 0.8),  # m_edy is negative
            (10.0, 20.0, 15.0, -25.0, 0.8),  # m_rdy is negative
            (10.0, 20.0, 15.0, 25.0, -0.8),  # a is negative
            (10.0, 0.0, 15.0, 25.0, 0.8),  # m_rdz is zero
            (10.0, 20.0, 15.0, 0.0, 0.8),  # m_rdy is zero
            (10.0, 20.0, 15.0, 25.0, 0.0),  # a is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, m_edz: float, m_rdz: float, m_edy: float, m_rdy: float, a: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot39SimplifiedCriterionBiaxialBending(m_edz=m_edz, m_rdz=m_rdz, m_edy=m_edy, m_rdy=m_rdy, a=a)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \left( \frac{M_{Edz}}{M_{Rdz}} \right)^{a} + \left( \frac{M_{Edy}}{M_{Rdy}} \right)^{a} \leq 1 \to "
                r"\left( \frac{10.000}{20.000} \right)^{0.800} + \left( \frac{15.000}{25.000} \right)^{0.800} \leq 1 \to \text{Not OK}",
            ),
            ("short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        m_edz = 10.0  # KNM
        m_rdz = 20.0  # KNM
        m_edy = 15.0  # KNM
        m_rdy = 25.0  # KNM
        a = 0.8  # DIMENSIONLESS

        # Object to test
        latex = Form5Dot39SimplifiedCriterionBiaxialBending(m_edz=m_edz, m_rdz=m_rdz, m_edy=m_edy, m_rdy=m_rdy, a=a).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

"""Testing formula 5.4 of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_5_structural_analysis.formula_5_4 import Form5Dot4TTransverseForceEffectBracingSystem
from blueprints.validations import NegativeValueError


class TestForm5Dot4TTransverseForceEffectBracingSystem:
    """Validation for formula 5.4 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        theta_i = 0.003  # -
        n_a = 5  # kN
        n_b = 10  # kN

        # Object to test
        form_5_4 = Form5Dot4TTransverseForceEffectBracingSystem(theta_i=theta_i, n_a=n_a, n_b=n_b)

        # Expected result, manually calculated
        manually_calculated_result = 0.015  # kN

        assert form_5_4 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_theta_i_is_given(self) -> None:
        """Test a negative value for theta_i."""
        # Example values
        theta_i = -0.003
        n_a = 5
        n_b = 10

        with pytest.raises(NegativeValueError):
            Form5Dot4TTransverseForceEffectBracingSystem(theta_i=theta_i, n_a=n_a, n_b=n_b)

    def test_raise_error_when_negative_n_a_is_given(self) -> None:
        """Test a negative value for n_a."""
        # Example values
        theta_i = 0.003
        n_a = -5
        n_b = 10

        with pytest.raises(NegativeValueError):
            Form5Dot4TTransverseForceEffectBracingSystem(theta_i=theta_i, n_a=n_a, n_b=n_b)

    def test_raise_error_when_negative_n_b_is_given(self) -> None:
        """Test a negative value for n_b."""
        # Example values
        theta_i = 0.003
        n_a = 5
        n_b = -10

        with pytest.raises(NegativeValueError):
            Form5Dot4TTransverseForceEffectBracingSystem(theta_i=theta_i, n_a=n_a, n_b=n_b)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"H_{i} = Θ_{i} \cdot (N_{b} - N_{a}) = 0.003 \cdot (10.000 - 5.000) = 0.015",
            ),
            ("short", r"H_{i} = 0.015"),
            (
                "string",
                r"H_{i} = Θ_{i} \cdot (N_{b} - N_{a}) = 0.003 \cdot (10.000 - 5.000) = 0.015",
            ),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        theta_i = 0.003  # -
        n_a = 5  # kN
        n_b = 10  # kN

        # Object to test
        form_5_4_latex = Form5Dot4TTransverseForceEffectBracingSystem(
            theta_i=theta_i,
            n_a=n_a,
            n_b=n_b,
        ).latex()

        actual = {
            "complete": form_5_4_latex.complete,
            "short": form_5_4_latex.short,
            "string": str(form_5_4_latex),
        }

        assert (
            actual[representation] == expected
        ), f"{representation} representation failed."

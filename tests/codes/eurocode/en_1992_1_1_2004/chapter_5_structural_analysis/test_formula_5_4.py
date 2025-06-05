"""Testing formula 5.4 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_4 import Form5Dot4TransverseForceEffectBracingSystem
from blueprints.validations import NegativeValueError


class TestForm5Dot4TransverseForceEffectBracingSystem:
    """Validation for formula 5.4 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        theta_i = 0.003  # -
        n_a = 5  # kN
        n_b = 10  # kN

        # Object to test
        form_5_4 = Form5Dot4TransverseForceEffectBracingSystem(theta_i=theta_i, n_a=n_a, n_b=n_b)

        # Expected result, manually calculated
        manually_calculated_result = 0.015  # kN

        assert form_5_4 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("theta_i", "n_a", "n_b"),
        [
            (-0.003, 5, 10),
            (0.003, -5, 10),
            (0.003, 5, -10),
        ],
    )
    def test_raise_error_when_negative_theta_i_is_given(
        self,
        theta_i: float,
        n_a: float,
        n_b: float,
    ) -> None:
        """Test negative values for theta_i, n_a and n_b."""
        with pytest.raises(NegativeValueError):
            Form5Dot4TransverseForceEffectBracingSystem(theta_i=theta_i, n_a=n_a, n_b=n_b)

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
        form_5_4_latex = Form5Dot4TransverseForceEffectBracingSystem(
            theta_i=theta_i,
            n_a=n_a,
            n_b=n_b,
        ).latex()

        actual = {
            "complete": form_5_4_latex.complete,
            "short": form_5_4_latex.short,
            "string": str(form_5_4_latex),
        }

        assert actual[representation] == expected, f"{representation} representation failed."

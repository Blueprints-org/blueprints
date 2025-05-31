"""Testing formula 5.5 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_5 import Form5Dot5TransverseForceEffectFloorDiaphragm
from blueprints.validations import NegativeValueError


class TestForm5Dot5TransverseForceEffectFloorDiaphragm:
    """Validation for formula 5.5 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        theta_i = 0.003  # -
        n_a = 5  # kN
        n_b = 10  # kN

        # Object to test
        form_5_4 = Form5Dot5TransverseForceEffectFloorDiaphragm(theta_i=theta_i, n_a=n_a, n_b=n_b)

        # Expected result, manually calculated
        manually_calculated_result = 0.0225  # kN

        assert form_5_4 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("theta_i", "n_a", "n_b"),
        [
            (-0.003, 5, 10),
            (0.003, -5, 10),
            (0.003, 5, -10),
        ],
    )
    def test_raise_error_when_negative_theta_i_is_given(self, theta_i: float, n_a: float, n_b: float) -> None:
        """Test negative values for theta_i, n_a and n_b."""
        with pytest.raises(NegativeValueError):
            Form5Dot5TransverseForceEffectFloorDiaphragm(theta_i=theta_i, n_a=n_a, n_b=n_b)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"H_{i} = Θ_{i} \cdot (N_{b} + N_{a}) / 2 = 0.003 \cdot (10.000 + 5.000) / 2 = 0.022",
            ),
            ("short", "H_{i} = 0.022"),
            (
                "string",
                r"H_{i} = Θ_{i} \cdot (N_{b} + N_{a}) / 2 = 0.003 \cdot (10.000 + 5.000) / 2 = 0.022",
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
        form_5_5_latex = Form5Dot5TransverseForceEffectFloorDiaphragm(
            theta_i=theta_i,
            n_a=n_a,
            n_b=n_b,
        ).latex()

        actual = {
            "complete": form_5_5_latex.complete,
            "short": form_5_5_latex.short,
            "string": str(form_5_5_latex),
        }

        assert actual[representation] == expected, f"{representation} representation failed."

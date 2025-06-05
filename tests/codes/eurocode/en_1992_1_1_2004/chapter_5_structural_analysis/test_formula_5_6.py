"""Testing formula 5.6 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_6 import Form5Dot6TransverseForceEffectRoofDiaphragm
from blueprints.validations import NegativeValueError


class TestForm5Dot6TransverseForceEffectRoofDiaphragm:
    """Validation for formula 5.6 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        theta_i = 0.003  # -
        n_a = 5  # kN

        # Object to test
        form_5_6 = Form5Dot6TransverseForceEffectRoofDiaphragm(theta_i=theta_i, n_a=n_a)

        # Expected result, manually calculated
        manually_calculated_result = 0.015  # kN

        assert form_5_6 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_theta_i_is_given(self) -> None:
        """Test a negative value for theta_i."""
        # Example values
        theta_i = -0.003
        n_a = 5

        with pytest.raises(NegativeValueError):
            Form5Dot6TransverseForceEffectRoofDiaphragm(theta_i=theta_i, n_a=n_a)

    def test_raise_error_when_negative_n_a_is_given(self) -> None:
        """Test a negative value for n_a."""
        # Example values
        theta_i = 0.003
        n_a = -5

        with pytest.raises(NegativeValueError):
            Form5Dot6TransverseForceEffectRoofDiaphragm(theta_i=theta_i, n_a=n_a)

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            ("complete", r"H_{i} = Θ_{i} \cdot N_{a} = 0.003 \cdot 5.000 = 0.015"),
            ("short", "H_{i} = 0.015"),
            ("string", r"H_{i} = Θ_{i} \cdot N_{a} = 0.003 \cdot 5.000 = 0.015"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        theta_i = 0.003  # -
        n_a = 5  # kN

        # Object to test
        form_5_6_latex = Form5Dot6TransverseForceEffectRoofDiaphragm(
            theta_i=theta_i,
            n_a=n_a,
        ).latex()

        actual = {
            "complete": form_5_6_latex.complete,
            "short": form_5_6_latex.short,
            "string": str(form_5_6_latex),
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."

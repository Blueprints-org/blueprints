"""Testing formula 5.23 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_23 import Form5Dot23FactorConcreteStrengthClass
from blueprints.validations import NegativeValueError


class TestForm5Dot23FactorConcreteStrengthClass:
    """Validation for formula 5.23 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_ck = 30  # MPa

        # Object to test
        form_5_23 = Form5Dot23FactorConcreteStrengthClass(f_ck=f_ck)

        # Expected result, manually calculated
        manually_calculated_result = 1.2247  # -

        assert form_5_23 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_f_ck_is_given(self) -> None:
        """Test a negative value for f_ck."""
        # Example values
        f_ck = -30

        with pytest.raises(NegativeValueError):
            Form5Dot23FactorConcreteStrengthClass(f_ck=f_ck)

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            ("complete", r"k_{1} = \sqrt{\frac{f_{ck}}{20}} = \sqrt{\frac{30.000}{20}} = 1.225"),
            ("short", "k_{1} = 1.225"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_ck = 30  # MPa

        # Object to test
        form_5_23_latex = Form5Dot23FactorConcreteStrengthClass(f_ck=f_ck).latex()

        actual = {
            "complete": form_5_23_latex.complete,
            "short": form_5_23_latex.short,
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."

"""Testing formula 5.8 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_8 import Form5Dot8EffectiveSpan
from blueprints.validations import NegativeValueError


class TestForm5Dot8EffectiveSpan:
    """Validation for formula 5.8 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        l_n = 5  # m
        a_1 = 0.5  # m
        a_2 = 0.35  # m

        # Object to test
        form_5_8 = Form5Dot8EffectiveSpan(l_n=l_n, a_1=a_1, a_2=a_2)

        # Expected result, manually calculated
        manually_calculated_result = 5.85  # kN

        assert form_5_8 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("l_n", "a_1", "a_2"),
        [
            (-5, 0.5, 0.35),
            (5, -0.5, 0.35),
            (5, 0.5, -0.35),
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, l_n: float, a_1: float, a_2: float) -> None:
        """Test negative values."""
        with pytest.raises(NegativeValueError):
            Form5Dot8EffectiveSpan(l_n=l_n, a_1=a_1, a_2=a_2)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"l_{eff} = l_{n} + a_{1} + a_{2} = 5.000 + 0.500 + 0.350 = 5.850",
            ),
            ("short", r"l_{eff} = 5.850"),
            (
                "string",
                r"l_{eff} = l_{n} + a_{1} + a_{2} = 5.000 + 0.500 + 0.350 = 5.850",
            ),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        l_n = 5  # m
        a_1 = 0.5  # m
        a_2 = 0.35  # m

        # Object to test
        form_5_8_latex = Form5Dot8EffectiveSpan(
            l_n=l_n,
            a_1=a_1,
            a_2=a_2,
        ).latex()

        actual = {
            "complete": form_5_8_latex.complete,
            "short": form_5_8_latex.short,
            "string": str(form_5_8_latex),
        }

        assert expected == actual[representation], f"{representation} representation failed."

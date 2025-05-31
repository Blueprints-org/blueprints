"""Testing formula 5.15 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_15 import Form5Dot15EffectiveLengthBraced
from blueprints.validations import NegativeValueError


class TestForm5Dot15EffectiveLengthBraced:
    """Validation for formula 5.15 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        k_1 = 2.0  # -
        k_2 = 3.0  # -
        height = 4.0  # M

        # Object to test
        form_5_15 = Form5Dot15EffectiveLengthBraced(k_1=k_1, k_2=k_2, height=height)

        # Expected result, manually calculated
        manually_calculated_result = 3.6855  # M

        assert form_5_15 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("k_1", "k_2", "height"),
        [
            (-2, 3, 4),
            (2, -3, 4),
            (2, 3, -4),
        ],
    )
    def test_raise_error_when_negative_theta_i_is_given(self, k_1: float, k_2: float, height: float) -> None:
        """Test negative values for theta_i, n_a and n_b."""
        with pytest.raises(NegativeValueError):
            Form5Dot15EffectiveLengthBraced(k_1=k_1, k_2=k_2, height=height)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"l_0 = 0.5 \cdot l \cdot \sqrt{"
                r"\left(1+\frac{k_1}{0.45 + k_1}\right) \cdot "
                r"\left(1 + \frac{k_2}{0.45 + k_2}\right)} = "
                r"0.5 \cdot 4.000 \cdot \sqrt{"
                r"\left(1+\frac{2.000}{0.45 + 2.000}\right) \cdot "
                r"\left(1 + \frac{3.000}{0.45 + 3.000}\right)} = "
                r"3.686",
            ),
            ("short", r"l_0 = 3.686"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        k_1 = 2.0  # -
        k_2 = 3.0  # -
        height = 4.0  # M

        # Object to test
        form_5_15_latex = Form5Dot15EffectiveLengthBraced(k_1=k_1, k_2=k_2, height=height).latex()

        actual = {
            "complete": form_5_15_latex.complete,
            "short": form_5_15_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."

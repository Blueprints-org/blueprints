"""Testing formula 5.16 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_16 import Form5Dot16EffectiveLengthUnbraced
from blueprints.validations import NegativeValueError


class TestForm5Dot16EffectiveLengthUnbraced:
    """Validation for formula 5.16 from EN 1992-1-1:2004, where left side of max statement is active."""

    def test_evaluation_left(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        k_1 = 2.0  # -
        k_2 = 3.0  # -
        height = 4.0  # M

        # Object to test
        form_5_16 = Form5Dot16EffectiveLengthUnbraced(k_1=k_1, k_2=k_2, height=height)

        # Expected result, manually calculated
        manually_calculated_result = 14.4222  # M

        assert form_5_16 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_right(self) -> None:
        """Validation for formula 5.16 from EN 1992-1-1:2004, where right side of max statement is active."""
        # Example values
        k_1 = 0.0  # -
        k_2 = 3.0  # -
        height = 4.0  # M

        # Object to test
        form_5_16 = Form5Dot16EffectiveLengthUnbraced(k_1=k_1, k_2=k_2, height=height)

        # Expected result, manually calculated
        manually_calculated_result = 7.0  # M

        assert form_5_16 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

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
            Form5Dot16EffectiveLengthUnbraced(k_1=k_1, k_2=k_2, height=height)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"l_0 = l \cdot max\left\{"
                r"\sqrt{1+10 \cdot \frac{k_1 \cdot k_2}{k_1+k_2}}; "
                r"\left(1+\frac{k_1}{1 + k_1}\right) \cdot \left(1 + \frac{k_2}{1 + k_2}\right) \right\}"
                r" = "
                r"4.000 \cdot max\left\{"
                r"\sqrt{1+10 \cdot \frac{2.000 \cdot 3.000}{2.000+3.000}}; "
                r"\left(1+\frac{2.000}{1 + 2.000}\right) \cdot "
                r"\left(1 + \frac{3.000}{1 + 3.000}\right) \right\}"
                r" = 14.422",
            ),
            ("short", r"l_0 = 14.422"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        k_1 = 2.0  # -
        k_2 = 3.0  # -
        height = 4.0  # M

        # Object to test
        form_5_16_latex = Form5Dot16EffectiveLengthUnbraced(k_1=k_1, k_2=k_2, height=height).latex()

        actual = {
            "complete": form_5_16_latex.complete,
            "short": form_5_16_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."

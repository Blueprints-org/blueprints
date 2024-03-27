"""Test formula 1.0.1 from NEN 9997-1+C2:2017: Chapter 1: General rules."""

import pytest

from blueprints.codes.eurocode.nen_9997_1_c2_2017.chapter_1_general_rules.formula_1_0_1 import Form1Dot0Dot1EquivalentPilePointCenterline
from blueprints.validations import LessOrEqualToZeroError


class TestForm1Dot0Dot1EquivalentPilePointCenterline:
    """Validation for formula 1.0.1 from NEN 9997-1+C2:2017."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        a = 0.3  # m
        b = 0.2  # m

        form_1_0_1 = Form1Dot0Dot1EquivalentPilePointCenterline(a=a, b=b)

        # manually calculated result
        manually_calculated_result = 0.2767923

        assert form_1_0_1 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a", "b"),
        [
            (-0.3, 0.45),
            (0.3, -0.45),
            (0.3, 0),
        ],
    )
    def test_raise_error_if_zero_or_negative(self, a: float, b: float) -> None:
        """Test if zero or negative values are given."""
        with pytest.raises(LessOrEqualToZeroError):
            Form1Dot0Dot1EquivalentPilePointCenterline(a=a, b=b)

    def test_raise_error_if_b_greater_than_1_5_times_a(self) -> None:
        """Test if b is greater than 1.5 times a."""
        with pytest.raises(ValueError):
            Form1Dot0Dot1EquivalentPilePointCenterline(a=0.3, b=0.5)

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            (
                "complete",
                r"D_{eq} = 1.13 \cdot a \cdot \sqrt{\frac{min(b, 1.5 \cdot a)}{a}} = 1.13 \cdot 0.3 \cdot \sqrt\frac{0.2}{0.3} = 0.277",
            ),
            ("short", "D_{eq} = 0.277"),
            (
                "string",
                r"D_{eq} = 1.13 \cdot a \cdot \sqrt{\frac{min(b, 1.5 \cdot a)}{a}} = 1.13 \cdot 0.3 \cdot \sqrt\frac{0.2}{0.3} = 0.277",
            ),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a = 0.3  # m
        b = 0.2  # m

        # Object to test
        form = Form1Dot0Dot1EquivalentPilePointCenterline(a=a, b=b).latex()

        actual = {
            "complete": form.complete,
            "short": form.short,
            "string": str(form),
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."

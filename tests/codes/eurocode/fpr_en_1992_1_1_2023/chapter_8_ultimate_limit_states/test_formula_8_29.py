"""Testing formula 8.29 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_29 import Form8Dot29MechanicalShearSpan
from blueprints.validations import LessOrEqualToZeroError


class TestForm8Dot29MechanicalShearSpan:
    """Validation for formula 8.29 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_cs = 1333.333333
        d = 500.0

        # Object to test
        formula = Form8Dot29MechanicalShearSpan(a_cs=a_cs, d=d)

        # Expected result, manually calculated
        manually_calculated_result = 408.248290  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_when_the_shear_span_equals_four_times_the_effective_depth(self) -> None:
        """Tests the upper edge of the range of application, where the mechanical shear span equals the effective depth."""
        # At a_cs = 4 * d the formula returns d itself
        formula = Form8Dot29MechanicalShearSpan(a_cs=2000.0, d=500.0)

        assert formula == pytest.approx(expected=500.0, rel=1e-9)

    @pytest.mark.parametrize(
        ("a_cs", "d"),
        [
            (-1333.333333, 500.0),  # a_cs is negative
            (0.0, 500.0),  # a_cs is zero
            (1333.333333, -500.0),  # d is negative
            (1333.333333, 0.0),  # d is zero, which is not a cross-section
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero(self, a_cs: float, d: float) -> None:
        """Test if error is raised for parameters that are not allowed to be zero or less."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot29MechanicalShearSpan(a_cs=a_cs, d=d)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"a_v = \sqrt{\frac{a_{cs}}{4} \cdot d} = \sqrt{\frac{1333.333}{4} \cdot 500.000} = 408.248 \ mm",
            ),
            (
                "complete_with_units",
                r"a_v = \sqrt{\frac{a_{cs}}{4} \cdot d} = \sqrt{\frac{1333.333 \ mm}{4} \cdot 500.000 \ mm} = 408.248 \ mm",
            ),
            ("short", r"a_v = 408.248 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_cs = 1333.333333
        d = 500.0

        # Object to test
        latex = Form8Dot29MechanicalShearSpan(a_cs=a_cs, d=d).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

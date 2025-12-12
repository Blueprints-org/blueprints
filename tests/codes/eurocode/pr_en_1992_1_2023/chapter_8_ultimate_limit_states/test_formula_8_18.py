"""Testing formula 8.18 of prEN 1992-1-1:2023"""

import pytest

from blueprints.codes.eurocode.pr_en_1992_1_2023.chapter_8_ultimate_limit_states.formula_8_18 import Form8Dot18AverageShearStress
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot18AverageShearStress:
    """Validation for formula 8.18 form prEN 1993-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed = 10000.0
        b_w = 50.0
        z = 215.0

        # Create object to test
        test_formula = Form8Dot18AverageShearStress(
            v_ed=v_ed,
            b_w=b_w,
            z=z
        )

        # Expected result, manually calculated
        manually_calculated_result = 0.93023 # MPa

        # Perform test by assert
        assert test_formula == pytest.approx(
            expected=manually_calculated_result,
            rel=1e-4
        )

    @pytest.mark.parametrize(
        ("v_ed", "b_w", "z"),
        [
            (-10000.0, 50.0, 215.0), # v_ed is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, v_ed: float, b_w: float, z:float):
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot18AverageShearStress(v_ed=v_ed, b_w=b_w, z=z)

    @pytest.mark.parametrize(
        ("v_ed", "b_w", "z"),
        [
            (10000.0, -50.0, 215.0),  # b_w is negative
            (10000.0, 0, 215.0),  # b_w is zero
            (10000.0, 50.0, -215.0),  # z is negative
            (10000.0, 50.0, 0),  # z is zero
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero(self, v_ed: float, b_w: float, z: float) -> None:
        """Test if error is raised for parameters that are not allowed to be zero or less."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot18AverageShearStress(v_ed=v_ed, b_w=b_w, z=z)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\tau_{Ed} = \frac{V_{Ed}}{b_w \cdot z} = \frac{10000.000}{50.000 \cdot 215.000} = 0.930 \ MPa"
            ),
            (
                "short", r"\tau_{Ed} = 0.930 \ MPa"
            )
        ]
    )
    def test_latex(self, representation: str, expected: str):
        """Test the latex representation of the formula."""
        # Example values
        v_ed = 10000.0
        b_w = 50.0
        z = 215.0

        # Object to test
        test_latex = Form8Dot18AverageShearStress(v_ed=v_ed, b_w=b_w, z=z).latex()

        actual = {
            "complete": test_latex.complete,
            "short": test_latex.short
        }

        assert expected == actual[representation]

"""Testing formula 8.113 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_113 import (
    Form8Dot113CompressiveStressInStrutOrCompressionField,
)
from blueprints.validations import LessOrEqualToZeroError


class TestForm8Dot113CompressiveStressInStrutOrCompressionField:
    """Validation for formula 8.113 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        f_cd = 150000.0
        b_c = 300.0
        t = 200.0

        # Object to test
        formula = Form8Dot113CompressiveStressInStrutOrCompressionField(f_cd=f_cd, b_c=b_c, t=t)

        # Expected result, manually calculated
        manually_calculated_result = 2.5  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_with_negative_force(self) -> None:
        """Tests the evaluation of the result when the compressive force is given as a negative value."""
        # Example values
        f_cd = -150000.0
        b_c = 300.0
        t = 200.0

        # Object to test
        formula = Form8Dot113CompressiveStressInStrutOrCompressionField(f_cd=f_cd, b_c=b_c, t=t)

        # Expected result, manually calculated
        manually_calculated_result = 2.5  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("f_cd", "b_c", "t"),
        [
            (150000.0, -300.0, 200.0),  # b_c is negative
            (150000.0, 0.0, 200.0),  # b_c is zero
            (150000.0, 300.0, -200.0),  # t is negative
            (150000.0, 300.0, 0.0),  # t is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, f_cd: float, b_c: float, t: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot113CompressiveStressInStrutOrCompressionField(f_cd=f_cd, b_c=b_c, t=t)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\sigma_{cd} = \frac{\left|F_{cd}\right|}{b_c \cdot t} = \frac{\left|150000.000\right|}{300.000 \cdot 200.000} = 2.500 \ MPa",
            ),
            (
                "complete_with_units",
                (
                    r"\sigma_{cd} = \frac{\left|F_{cd}\right|}{b_c \cdot t} = "
                    r"\frac{\left|150000.000 \ N\right|}{300.000 \ mm \cdot 200.000 \ mm} = 2.500 \ MPa"
                ),
            ),
            ("short", r"\sigma_{cd} = 2.500 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_cd = 150000.0
        b_c = 300.0
        t = 200.0

        # Object to test
        latex = Form8Dot113CompressiveStressInStrutOrCompressionField(f_cd=f_cd, b_c=b_c, t=t).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

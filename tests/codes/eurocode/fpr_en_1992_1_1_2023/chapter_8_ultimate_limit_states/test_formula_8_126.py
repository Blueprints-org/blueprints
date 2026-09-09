"""Testing formula 8.126 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_126 import (
    Form8Dot126CheckPartiallyLoadedAreaResistance,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot126CheckPartiallyLoadedAreaResistance:
    """Validation for formula 8.126 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("f_cd", "a_c1", "a_c0", "nu_part", "expected"),
        [
            (20.0, 90000.0, 40000.0, 3.0, True),  # the design resistance suffices
            (20.0, 360000.0, 40000.0, 3.0, True),  # exactly on the boundary, which the standard includes
            (20.0, 490000.0, 40000.0, 3.0, False),  # the design resistance does not suffice
        ],
    )
    def test_evaluation(self, f_cd: float, a_c1: float, a_c0: float, nu_part: float, expected: bool) -> None:
        """Tests the evaluation of the result."""
        assert bool(Form8Dot126CheckPartiallyLoadedAreaResistance(f_cd=f_cd, a_c1=a_c1, a_c0=a_c0, nu_part=nu_part)) is expected

    @pytest.mark.parametrize(
        ("f_cd", "a_c1", "a_c0", "nu_part"),
        [
            (-20.0, 90000.0, 40000.0, 3.0),  # f_cd is negative
            (20.0, -90000.0, 40000.0, 3.0),  # a_c1 is negative
            (20.0, 90000.0, 40000.0, -3.0),  # nu_part is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, f_cd: float, a_c1: float, a_c0: float, nu_part: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot126CheckPartiallyLoadedAreaResistance(f_cd=f_cd, a_c1=a_c1, a_c0=a_c0, nu_part=nu_part)

    @pytest.mark.parametrize(
        "a_c0",
        [
            -40000.0,  # a_c0 is negative
            0.0,  # a_c0 is zero
        ],
    )
    def test_raise_error_when_a_c0_is_less_or_equal_to_zero(self, a_c0: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot126CheckPartiallyLoadedAreaResistance(f_cd=20.0, a_c1=90000.0, a_c0=a_c0, nu_part=3.0)

    @pytest.mark.parametrize(
        ("a_c1", "representation", "expected"),
        [
            (
                90000.0,
                "complete",
                (
                    r"CHECK \to \sigma_{Rdu} = f_{cd} \cdot \sqrt{\frac{A_{c1}}{A_{c0}}} \leq \nu_{part} \cdot f_{cd} \to "
                    r"30.000 = 20.000 \cdot \sqrt{\frac{90000.000}{40000.000}} \leq 3.000 \cdot 20.000 \to OK"
                ),
            ),
            (
                90000.0,
                "complete_with_units",
                (
                    r"CHECK \to \sigma_{Rdu} = f_{cd} \cdot \sqrt{\frac{A_{c1}}{A_{c0}}} \leq \nu_{part} \cdot f_{cd} \to "
                    r"30.000 \ MPa = 20.000 \ MPa \cdot \sqrt{\frac{90000.000 \ mm^2}{40000.000 \ mm^2}} \leq "
                    r"3.000 \cdot 20.000 \ MPa \to OK"
                ),
            ),
            (90000.0, "short", r"CHECK \to OK"),
            (490000.0, "short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, a_c1: float, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = Form8Dot126CheckPartiallyLoadedAreaResistance(f_cd=20.0, a_c1=a_c1, a_c0=40000.0, nu_part=3.0).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

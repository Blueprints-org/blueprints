"""Testing formula 8.122 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_122 import (
    Form8Dot122CheckTieResistance,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot122CheckTieResistance:
    """Validation for formula 8.122 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("f_td", "a_s", "f_yd", "a_p", "f_pd", "expected"),
        [
            (200000.0, 300.0, 500.0, 100.0, 1000.0, True),  # the tie resists the tensile force
            (250000.0, 300.0, 500.0, 100.0, 1000.0, True),  # exactly on the boundary, which the standard includes
            (300000.0, 300.0, 500.0, 100.0, 1000.0, False),  # the tie does not resist the tensile force
            (100000.0, 500.0, 435.0, 0.0, 0.0, True),  # no prestressed reinforcement
        ],
    )
    def test_evaluation(self, f_td: float, a_s: float, f_yd: float, a_p: float, f_pd: float, expected: bool) -> None:
        """Tests the evaluation of the result."""
        assert bool(Form8Dot122CheckTieResistance(f_td=f_td, a_s=a_s, f_yd=f_yd, a_p=a_p, f_pd=f_pd)) is expected

    @pytest.mark.parametrize(
        ("f_td", "a_s", "f_yd", "a_p", "f_pd"),
        [
            (-200000.0, 300.0, 500.0, 100.0, 1000.0),  # f_td is negative
            (200000.0, -300.0, 500.0, 100.0, 1000.0),  # a_s is negative
            (200000.0, 300.0, -500.0, 100.0, 1000.0),  # f_yd is negative
            (200000.0, 300.0, 500.0, -100.0, 1000.0),  # a_p is negative
            (200000.0, 300.0, 500.0, 100.0, -1000.0),  # f_pd is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, f_td: float, a_s: float, f_yd: float, a_p: float, f_pd: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot122CheckTieResistance(f_td=f_td, a_s=a_s, f_yd=f_yd, a_p=a_p, f_pd=f_pd)

    @pytest.mark.parametrize(
        ("f_td", "representation", "expected"),
        [
            (
                200000.0,
                "complete",
                (
                    r"CHECK \to F_{td} \leq A_s \cdot f_{yd} + A_p \cdot f_{pd} \to "
                    r"200000.000 \leq 300.000 \cdot 500.000 + 100.000 \cdot 1000.000 \to OK"
                ),
            ),
            (
                200000.0,
                "complete_with_units",
                (
                    r"CHECK \to F_{td} \leq A_s \cdot f_{yd} + A_p \cdot f_{pd} \to "
                    r"200000.000 \ N \leq 300.000 \ mm^2 \cdot 500.000 \ MPa + 100.000 \ mm^2 \cdot 1000.000 \ MPa \to OK"
                ),
            ),
            (200000.0, "short", r"CHECK \to OK"),
            (300000.0, "short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, f_td: float, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = Form8Dot122CheckTieResistance(f_td=f_td, a_s=300.0, f_yd=500.0, a_p=100.0, f_pd=1000.0).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

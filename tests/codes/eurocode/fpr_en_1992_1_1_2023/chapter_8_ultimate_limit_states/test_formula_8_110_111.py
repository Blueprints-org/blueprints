"""Testing formulas 8.110 and 8.111 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_110_111 import (
    Form8Dot110To111CoefficientForPunchingShearReinforcingSystem,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot110To111CoefficientForPunchingShearReinforcingSystem:
    """Validation for formulas 8.110 and 8.111 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("b_0", "d_v", "is_stud", "expected"),
        [
            (600.0, 200.0, True, 1.529127),  # studs, formula (8.110), expression governs
            (600.0, 200.0, False, 1.329127),  # links and stirrups, formula (8.111), expression governs
            (1.0, 1000.0, False, 1.0),  # links and stirrups, the lower bound of 1.0 governs
        ],
    )
    def test_evaluation(self, b_0: float, d_v: float, is_stud: bool, expected: float) -> None:
        """Tests the evaluation of the result."""
        formula = Form8Dot110To111CoefficientForPunchingShearReinforcingSystem(b_0=b_0, d_v=d_v, is_stud=is_stud)

        assert formula == pytest.approx(expected=expected, rel=1e-4)

    @pytest.mark.parametrize(
        ("b_0", "d_v", "is_stud"),
        [
            (-600.0, 200.0, True),  # b_0 is negative
            (600.0, -200.0, True),  # d_v is negative
            (600.0, 0.0, True),  # d_v is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, b_0: float, d_v: float, is_stud: bool) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot110To111CoefficientForPunchingShearReinforcingSystem(b_0=b_0, d_v=d_v, is_stud=is_stud)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\eta_{sys} = \begin{cases} \max\left(0.70 + 0.63 \cdot \left(\frac{b_0}{d_v}\right)^{\frac{1}{4}}, 1.0\right) & "
                    r"\text{if studs} \\ \max\left(0.50 + 0.63 \cdot \left(\frac{b_0}{d_v}\right)^{\frac{1}{4}}, 1.0\right) & "
                    r"\text{if links and stirrups} \end{cases} = "
                    r"\begin{cases} \max\left(0.70 + 0.63 \cdot \left(\frac{600.000}{200.000}\right)^{\frac{1}{4}}, 1.0\right) & "
                    r"\text{if studs} \\ \max\left(0.50 + 0.63 \cdot \left(\frac{600.000}{200.000}\right)^{\frac{1}{4}}, 1.0\right) & "
                    r"\text{if links and stirrups} \end{cases} = 1.529 \ -"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\eta_{sys} = \begin{cases} \max\left(0.70 + 0.63 \cdot \left(\frac{b_0}{d_v}\right)^{\frac{1}{4}}, 1.0\right) & "
                    r"\text{if studs} \\ \max\left(0.50 + 0.63 \cdot \left(\frac{b_0}{d_v}\right)^{\frac{1}{4}}, 1.0\right) & "
                    r"\text{if links and stirrups} \end{cases} = "
                    r"\begin{cases} \max\left(0.70 + 0.63 \cdot \left(\frac{600.000 \ mm}{200.000 \ mm}\right)^{\frac{1}{4}}, 1.0\right) & "
                    r"\text{if studs} \\ \max\left(0.50 + 0.63 \cdot \left(\frac{600.000 \ mm}{200.000 \ mm}\right)^{\frac{1}{4}}, 1.0\right) & "
                    r"\text{if links and stirrups} \end{cases} = 1.529 \ -"
                ),
            ),
            ("short", r"\eta_{sys} = 1.529 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        b_0 = 600.0
        d_v = 200.0
        is_stud = True

        # Object to test
        latex = Form8Dot110To111CoefficientForPunchingShearReinforcingSystem(b_0=b_0, d_v=d_v, is_stud=is_stud).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

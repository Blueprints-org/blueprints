"""Testing formula 12.2 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_12_plain_and_lightly_reinforced_concrete_structures.formula_12_2 import (
    Form12Dot2PlainConcreteBendingResistance,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm12Dot2PlainConcreteBendingResistance:
    """Validation for formula 12.2 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        eta_f_cd_pl = 30.0  # MPa
        b = 300.0  # mm
        h_w = 500.0  # mm
        e = 100.0  # mm

        # Object to test
        form_12_2 = Form12Dot2PlainConcreteBendingResistance(eta_f_cd_pl=eta_f_cd_pl, b=b, h_w=h_w, e=e)

        # Expected result, manually calculated
        manually_calculated_result = 2700000.0  # N

        assert round(form_12_2, 3) == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("eta_f_cd_pl", "b", "h_w", "e"),
        [
            (-30.0, 300.0, 500.0, 100.0),
            (30.0, -300.0, 500.0, 100.0),
            (30.0, 300.0, 500.0, -100.0),
        ],
    )
    def test_raise_error_when_negative_values_are_given(
        self,
        eta_f_cd_pl: float,
        b: float,
        h_w: float,
        e: float,
    ) -> None:
        """Test negative values for eta_f_cd_pl, b, h_w, and e."""
        with pytest.raises(NegativeValueError):
            Form12Dot2PlainConcreteBendingResistance(eta_f_cd_pl=eta_f_cd_pl, b=b, h_w=h_w, e=e)

    @pytest.mark.parametrize(
        ("eta_f_cd_pl", "b", "h_w"),
        [
            (30.0, 300.0, 0.0),
            (30.0, 300.0, -20),
        ],
    )
    def test_raise_error_when_values_are_less_or_equal_to_zero(
        self,
        eta_f_cd_pl: float,
        b: float,
        h_w: float,
    ) -> None:
        """Test values less or equal to zero for eta_f_cd_pl, b, and h_w."""
        with pytest.raises(LessOrEqualToZeroError):
            Form12Dot2PlainConcreteBendingResistance(eta_f_cd_pl=eta_f_cd_pl, b=b, h_w=h_w, e=100.0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"N_{Rd} = \eta f_{cd,pl} \cdot b \cdot h_w \cdot \left(1 - \frac{2e}{h_w}\right) = 30.000 \cdot "
                r"300.000 \cdot 500.000 \cdot \left(1 - \frac{2 \cdot 100.000}{500.000}\right) = 2700000.000",
            ),
            ("short", r"N_{Rd} = 2700000.000"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        eta_f_cd_pl = 30.0  # MPa
        b = 300.0  # mm
        h_w = 500.0  # mm
        e = 100.0  # mm

        # Object to test
        form_12_2_latex = Form12Dot2PlainConcreteBendingResistance(
            eta_f_cd_pl=eta_f_cd_pl,
            b=b,
            h_w=h_w,
            e=e,
        ).latex()

        actual = {
            "complete": form_12_2_latex.complete,
            "short": form_12_2_latex.short,
            "string": str(form_12_2_latex),
        }

        assert actual[representation] == expected, f"{representation} representation failed."

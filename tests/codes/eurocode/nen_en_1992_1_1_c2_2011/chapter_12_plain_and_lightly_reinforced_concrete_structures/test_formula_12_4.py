"""Testing formula 12.4 of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_12_plain_and_lightly_reinforced_concrete_structures.formula_12_4 import (
    Form12Dot4PlainConcreteShearStress,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm12Dot4PlainConcreteShearStress:
    """Validation for formula 12.4 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        k = 1.5  # Nationally determined parameter
        v_ed = 100000.0  # N
        a_cc = 50000.0  # mm^2

        # Object to test
        form_12_4 = Form12Dot4PlainConcreteShearStress(k=k, v_ed=v_ed, a_cc=a_cc)

        # Expected result, manually calculated
        manually_calculated_result = 3.0  # MPa

        assert round(form_12_4, 3) == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("v_ed", "a_cc"),
        [
            (0.0, 50000.0),
            (100000.0, 0.0),
        ],
    )
    def test_raise_error_when_values_are_less_or_equal_to_zero(
        self,
        v_ed: float,
        a_cc: float,
    ) -> None:
        """Test values less or equal to zero for v_ed and a_cc."""
        with pytest.raises(LessOrEqualToZeroError):
            Form12Dot4PlainConcreteShearStress(k=1.5, v_ed=v_ed, a_cc=a_cc)

    @pytest.mark.parametrize(
        ("v_ed", "a_cc"),
        [
            (-100000.0, 50000.0),
            (100000.0, -50000.0),
        ],
    )
    def test_raise_error_when_negative_values_are_given(
        self,
        v_ed: float,
        a_cc: float,
    ) -> None:
        """Test negative values for v_ed and a_cc."""
        with pytest.raises(NegativeValueError):
            Form12Dot4PlainConcreteShearStress(k=1.5, v_ed=v_ed, a_cc=a_cc)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\tau_{cp} = k \cdot \frac{V_{Ed}}{A_{cc}} = 1.500 \cdot \frac{100000.000}{50000.000} = 3.000",
            ),
            ("short", r"\tau_{cp} = 3.000"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        k = 1.5  # Nationally determined parameter
        v_ed = 100000.0  # N
        a_cc = 50000.0  # mm^2

        # Object to test
        form_12_4_latex = Form12Dot4PlainConcreteShearStress(
            k=k,
            v_ed=v_ed,
            a_cc=a_cc,
        ).latex()

        actual = {
            "complete": form_12_4_latex.complete,
            "short": form_12_4_latex.short,
            "string": str(form_12_4_latex),
        }

        assert actual[representation] == expected, f"{representation} representation failed."

"""Testing formula 12.3 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_12_plain_and_lightly_reinforced_concrete_structures.formula_12_3 import (
    Form12Dot3PlainConcreteShearStress,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm12Dot3PlainConcreteShearStress:
    """Validation for formula 12.3 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        n_ed = 100000.0  # N
        a_cc = 50000.0  # mm^2

        # Object to test
        form_12_3 = Form12Dot3PlainConcreteShearStress(n_ed=n_ed, a_cc=a_cc)

        # Expected result, manually calculated
        manually_calculated_result = 2.0  # MPa

        assert round(form_12_3, 3) == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("n_ed", "a_cc"),
        [
            (100000.0, 0.0),
        ],
    )
    def test_raise_error_when_values_are_less_or_equal_to_zero(
        self,
        n_ed: float,
        a_cc: float,
    ) -> None:
        """Test values less or equal to zero for n_ed and a_cc."""
        with pytest.raises(LessOrEqualToZeroError):
            Form12Dot3PlainConcreteShearStress(n_ed=n_ed, a_cc=a_cc)

    @pytest.mark.parametrize(
        ("n_ed", "a_cc"),
        [
            (-100000.0, 500),
        ],
    )
    def test_raise_error_when_values_are_less_to_zero(
        self,
        n_ed: float,
        a_cc: float,
    ) -> None:
        """Test values less or equal to zero for n_ed and a_cc."""
        with pytest.raises(NegativeValueError):
            Form12Dot3PlainConcreteShearStress(n_ed=n_ed, a_cc=a_cc)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\sigma_{cp} = \frac{N_{Ed}}{A_{cc}} = \frac{100000.000}{50000.000} = 2.000",
            ),
            ("short", r"\sigma_{cp} = 2.000"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n_ed = 100000.0  # N
        a_cc = 50000.0  # mm^2

        # Object to test
        form_12_3_latex = Form12Dot3PlainConcreteShearStress(
            n_ed=n_ed,
            a_cc=a_cc,
        ).latex()

        actual = {
            "complete": form_12_3_latex.complete,
            "short": form_12_3_latex.short,
            "string": str(form_12_3_latex),
        }

        assert actual[representation] == expected, f"{representation} representation failed."

"""Testing formula NB.NB.11 of NEN-EN 1993-1-1:2006."""

import pytest

from blueprints.codes.eurocode.national_annex.nl.nen_en_1993_1_1_2006.chapter_NB_NB_critical_buckling_moment.formula_nb_nb_11 import (
    FormNBDotNB11CoefficientC,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestFormNBDotNB11CoefficientC:
    """Validation for formula NB.NB.11 from NEN-EN 1993-1-1:2006."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        c_1 = 1.13
        c_2 = 0.45
        l_g = 5000.0
        l_kip = 6000.0
        s = 1000.0

        # Object to test
        formula = FormNBDotNB11CoefficientC(c_1=c_1, c_2=c_2, l_g=l_g, l_kip=l_kip, s=s)

        # Expected result, manually calculated
        manually_calculated_result = 4.108336496226734

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("c_1", "c_2", "l_g", "l_kip", "s"),
        [
            (-1.13, 0.45, 5000.0, 6000.0, 1000.0),  # c_1 is negative
            (1.13, -0.45, 5000.0, 6000.0, 1000.0),  # c_2 is negative
            (1.13, 0.45, -5000.0, 6000.0, 1000.0),  # l_g is negative
            (1.13, 0.45, 5000.0, 6000.0, -1000.0),  # s is negative
            (1.13, 0.45, 5000.0, 0.0, 1000.0),  # l_kip is zero
            (1.13, 0.45, 5000.0, -6000.0, 1000.0),  # l_kip is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, c_1: float, c_2: float, l_g: float, l_kip: float, s: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            FormNBDotNB11CoefficientC(c_1=c_1, c_2=c_2, l_g=l_g, l_kip=l_kip, s=s)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"C = \frac{\pi \cdot C_1 \cdot L_g}{L_{kip}} \cdot \left( \sqrt{1 + \frac{\pi^2 \cdot S^2}{L_{kip}^2} "
                r"\cdot \left(C_2^2 + 1\right)} + \frac{\pi \cdot C_2 \cdot S}{L_{kip}} \right) = "
                r"\frac{\pi \cdot 1.130 \cdot 5000.000}{6000.000} \cdot \left( \sqrt{1 + \frac{\pi^2 \cdot 1000.000^2}{6000.000^2} "
                r"\cdot \left(0.450^2 + 1\right)} + \frac{\pi \cdot 0.450 \cdot 1000.000}{6000.000} \right) = 4.108 \ -",
            ),
            (
                "complete_with_units",
                r"C = \frac{\pi \cdot C_1 \cdot L_g}{L_{kip}} \cdot \left( \sqrt{1 + \frac{\pi^2 \cdot S^2}{L_{kip}^2} "
                r"\cdot \left(C_2^2 + 1\right)} + \frac{\pi \cdot C_2 \cdot S}{L_{kip}} \right) = "
                r"\frac{\pi \cdot 1.130 \cdot 5000.000 \ mm}{6000.000 \ mm} \cdot \left( "
                r"\sqrt{1 + \frac{\pi^2 \cdot 1000.000 \ mm^2}{6000.000 \ mm^2} "
                r"\cdot \left(0.450^2 + 1\right)} + \frac{\pi \cdot 0.450 \cdot 1000.000 \ mm}{6000.000 \ mm} \right) = 4.108 \ -",
            ),
            ("short", r"C = 4.108 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        c_1 = 1.13
        c_2 = 0.45
        l_g = 5000.0
        l_kip = 6000.0
        s = 1000.0

        # Object to test
        latex = FormNBDotNB11CoefficientC(c_1=c_1, c_2=c_2, l_g=l_g, l_kip=l_kip, s=s).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

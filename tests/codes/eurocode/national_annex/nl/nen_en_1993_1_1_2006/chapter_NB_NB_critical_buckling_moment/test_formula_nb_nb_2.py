"""Testing formula NB.NB.2 of NEN-EN 1993-1-1:2006."""

import pytest

from blueprints.codes.eurocode.national_annex.nl.nen_en_1993_1_1_2006.chapter_NB_NB_critical_buckling_moment.formula_nb_nb_2 import (
    FormNBDotNB2CriticalElasticBucklingMoment,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestFormNBDotNB2CriticalElasticBucklingMoment:
    """Validation for formula NB.NB.2 from NEN-EN 1993-1-1:2006."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        k_red = 1.0
        c = 0.99
        l_g = 5000.0
        e = 210000.0
        i_z = 8000000.0
        g = 81000.0
        i_t = 200000.0

        # Object to test
        formula = FormNBDotNB2CriticalElasticBucklingMoment(k_red=k_red, c=c, l_g=l_g, e=e, i_z=i_z, g=g, i_t=i_t)

        # Expected result, manually calculated
        manually_calculated_result = 103144738.576

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("k_red", "c", "l_g", "e", "i_z", "g", "i_t"),
        [
            (-1.0, 0.99, 5000.0, 210000.0, 8000000.0, 81000.0, 200000.0),  # k_red is negative
            (1.0, -0.99, 5000.0, 210000.0, 8000000.0, 81000.0, 200000.0),  # c is negative
            (1.0, 0.99, 5000.0, -210000.0, 8000000.0, 81000.0, 200000.0),  # e is negative
            (1.0, 0.99, 5000.0, 210000.0, -8000000.0, 81000.0, 200000.0),  # i_z is negative
            (1.0, 0.99, 5000.0, 210000.0, 8000000.0, -81000.0, 200000.0),  # g is negative
            (1.0, 0.99, 5000.0, 210000.0, 8000000.0, 81000.0, -200000.0),  # i_t is negative
            (1.0, 0.99, 0.0, 210000.0, 8000000.0, 81000.0, 200000.0),  # l_g is zero
            (1.0, 0.99, -5000.0, 210000.0, 8000000.0, 81000.0, 200000.0),  # l_g is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self, k_red: float, c: float, l_g: float, e: float, i_z: float, g: float, i_t: float
    ) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            FormNBDotNB2CriticalElasticBucklingMoment(k_red=k_red, c=c, l_g=l_g, e=e, i_z=i_z, g=g, i_t=i_t)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"M_{cr} = k_{red} \cdot \frac{C}{L_g} \cdot \sqrt{E \cdot I_z \cdot G \cdot I_t} = "
                r"1.000 \cdot \frac{0.990}{5000.000} \cdot \sqrt{210000.000 \cdot 8000000.000 \cdot 81000.000 \cdot 200000.000} = 103144738.576 \ Nmm",
            ),
            (
                "complete_with_units",
                r"M_{cr} = k_{red} \cdot \frac{C}{L_g} \cdot \sqrt{E \cdot I_z \cdot G \cdot I_t} = "
                r"1.000 \cdot \frac{0.990}{5000.000 \ mm} \cdot \sqrt{210000.000 \ MPa \cdot 8000000.000 \ mm^4 \cdot 81000.000 \ MPa \cdot 200000.000 \ mm^4} = 103144738.576 \ Nmm",
            ),
            ("short", r"M_{cr} = 103144738.576 \ Nmm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        k_red = 1.0
        c = 0.99
        l_g = 5000.0
        e = 210000.0
        i_z = 8000000.0
        g = 81000.0
        i_t = 200000.0

        # Object to test
        latex = FormNBDotNB2CriticalElasticBucklingMoment(k_red=k_red, c=c, l_g=l_g, e=e, i_z=i_z, g=g, i_t=i_t).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

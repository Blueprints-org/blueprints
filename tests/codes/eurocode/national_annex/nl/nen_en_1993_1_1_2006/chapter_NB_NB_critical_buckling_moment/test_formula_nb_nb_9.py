"""Testing formula NB.NB.9 of NEN-EN 1993-1-1:2006."""

import pytest

from blueprints.codes.eurocode.national_annex.nl.nen_en_1993_1_1_2006.chapter_NB_NB_critical_buckling_moment.formula_nb_nb_9 import (
    FormNBDotNB9Alpha,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestFormNBDotNB9Alpha:
    """Validation for formula NB.NB.9 from NEN-EN 1993-1-1:2006."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        h = 400.0
        t_f = 15.0
        t_w = 8.0
        b = 200.0
        l_g = 5000.0

        # Object to test
        formula = FormNBDotNB9Alpha(h=h, t_f=t_f, t_w=t_w, b=b, l_g=l_g)

        # Expected result, manually calculated
        manually_calculated_result = 2343.75

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_result_575(self) -> None:
        """Tests the evaluation of the result if it is limited with the 575."""
        # Example values
        h = 10.0
        t_f = 15.0
        t_w = 8.0
        b = 200.0
        l_g = 5000.0

        # Object to test
        formula = FormNBDotNB9Alpha(h=h, t_f=t_f, t_w=t_w, b=b, l_g=l_g)

        # Expected result, manually calculated
        manually_calculated_result = 575.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("h", "t_f", "t_w", "b", "l_g"),
        [
            (-400.0, 15.0, 8.0, 200.0, 5000.0),  # h is negative
            (400.0, -15.0, 8.0, 200.0, 5000.0),  # t_f is negative
            (400.0, 15.0, 0.0, 200.0, 5000.0),  # t_w is zero
            (400.0, 15.0, -8.0, 200.0, 5000.0),  # t_w is negative
            (400.0, 15.0, 8.0, 0.0, 5000.0),  # b is zero
            (400.0, 15.0, 8.0, -200.0, 5000.0),  # b is negative
            (400.0, 15.0, 8.0, 200.0, 0.0),  # l_g is zero
            (400.0, 15.0, 8.0, 200.0, -5000.0),  # l_g is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, h: float, t_f: float, t_w: float, b: float, l_g: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            FormNBDotNB9Alpha(h=h, t_f=t_f, t_w=t_w, b=b, l_g=l_g)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\alpha = \max\left(575, \frac{h \cdot t_f \cdot 10^{12}}{t_w^3 \cdot b \cdot L_g^2}\right) = "
                r"\max\left(575, \frac{400.000 \cdot 15.000 \cdot 10^{12}}{8.000^3 \cdot 200.000 \cdot 5000.000^2}\right) = 2343.750 \ -",
            ),
            (
                "complete_with_units",
                r"\alpha = \max\left(575, \frac{h \cdot t_f \cdot 10^{12}}{t_w^3 \cdot b \cdot L_g^2}\right) = "
                r"\max\left(575, \frac{400.000 \ mm \cdot 15.000 \ mm \cdot 10^{12}}{8.000 \ mm^3 \cdot 200.000 \ mm "
                r"\cdot 5000.000 \ mm^2}\right) = 2343.750 \ -",
            ),
            ("short", r"\alpha = 2343.750 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        h = 400.0
        t_f = 15.0
        t_w = 8.0
        b = 200.0
        l_g = 5000.0

        # Object to test
        latex = FormNBDotNB9Alpha(h=h, t_f=t_f, t_w=t_w, b=b, l_g=l_g).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

"""Testing formula 9.12 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_9_detailling_and_specific_rules.formula_9_12n import (
    Form9Dot12nMinimumLongitudinalReinforcementColumns,
)
from blueprints.validations import NegativeValueError


class TestForm9Dot12nMinimumLongitudinalReinforcementColumns:
    """Validation for formula 9.12N from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        n_ed = 200  # kN
        f_yd = 500  # MPa
        a_c = 5000  # mm²
        form_9_12n = Form9Dot12nMinimumLongitudinalReinforcementColumns(n_ed=n_ed, f_yd=f_yd, a_c=a_c)

        # Expected result, manually calculated
        manually_calculated_result = 40

        assert form_9_12n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_upper_limit(self) -> None:
        """Test the evaluation of the result if the upper limit is reached."""
        # Example values
        n_ed = 200  # kN
        f_yd = 500  # MPa
        a_c = 25000  # mm²
        form_9_12n = Form9Dot12nMinimumLongitudinalReinforcementColumns(n_ed=n_ed, f_yd=f_yd, a_c=a_c)

        # Expected result, manually calculated
        manually_calculated_result = 50

        assert form_9_12n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_n_ed_is_given(self) -> None:
        """Test whether negative value error is raised if n_ed is negative."""
        n_ed = -200  # kN
        f_yd = 500  # MPa
        a_c = 5000  # mm²

        with pytest.raises(NegativeValueError):
            Form9Dot12nMinimumLongitudinalReinforcementColumns(n_ed=n_ed, f_yd=f_yd, a_c=a_c)

    def test_raise_error_when_negative_f_yd_is_given(self) -> None:
        """Test whether negative value error is raised if f_yd is negative."""
        n_ed = 200  # kN
        f_yd = -500  # MPa
        a_c = 5000  # mm²

        with pytest.raises(NegativeValueError):
            Form9Dot12nMinimumLongitudinalReinforcementColumns(n_ed=n_ed, f_yd=f_yd, a_c=a_c)

    def test_raise_error_when_negative_a_c_is_given(self) -> None:
        """Test whether negative value error is raised if a_c is negative."""
        n_ed = 200  # kN
        f_yd = 500  # MPa
        a_c = -5000  # mm²

        with pytest.raises(NegativeValueError):
            Form9Dot12nMinimumLongitudinalReinforcementColumns(n_ed=n_ed, f_yd=f_yd, a_c=a_c)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"A_{s,min} = \max( \frac{0.10 \cdot N_{Ed}}{f_{yd}}, 0.002 \cdot A_c ) = "
                    r"\max( \frac{0.10 \cdot 200.00}{500.00}, 0.002 \cdot 25000.00 ) = 50.00"
                ),
            ),
            ("short", r"A_{s,min} = 50.00"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n_ed = 200  # kN
        f_yd = 500  # MPa
        a_c = 25000  # mm²

        # Object to test
        form_9_12n_latex = Form9Dot12nMinimumLongitudinalReinforcementColumns(n_ed=n_ed, f_yd=f_yd, a_c=a_c).latex()

        actual = {"complete": form_9_12n_latex.complete, "short": form_9_12n_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

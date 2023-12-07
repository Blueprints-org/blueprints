"""Testing formula 9.12 of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_9_detailling_and_specific_rules.formula_9_12n import (
    Form9Dot12NMinimumLongitudinalReinforcementColumns,
)
from blueprints.validations import NegativeValueError


class TestForm9Dot12NMinimumLongitudinalReinforcementColumns:
    """Validation for formula 9.12N from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        n_ed = 200  # kN
        f_yd = 500  # MPa
        a_c = 5000  # mm²
        form_9_12n = Form9Dot12NMinimumLongitudinalReinforcementColumns(n_ed=n_ed, f_yd=f_yd, a_c=a_c)

        # Expected result, manually calculated
        manually_calculated_result = 40

        assert form_9_12n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_upper_limit(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        n_ed = 200  # kN
        f_yd = 500  # MPa
        a_c = 25000  # mm²
        form_9_12n = Form9Dot12NMinimumLongitudinalReinforcementColumns(n_ed=n_ed, f_yd=f_yd, a_c=a_c)

        # Expected result, manually calculated
        manually_calculated_result = 50

        assert form_9_12n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_n_ed_is_given(self) -> None:
        """Test the evaluation of the result."""
        n_ed = -200  # kN
        f_yd = 500  # MPa
        a_c = 5000  # mm²

        with pytest.raises(NegativeValueError):
            Form9Dot12NMinimumLongitudinalReinforcementColumns(n_ed=n_ed, f_yd=f_yd, a_c=a_c)

    def test_raise_error_when_negative_f_yd_is_given(self) -> None:
        """Test the evaluation of the result."""
        n_ed = 200  # kN
        f_yd = -500  # MPa
        a_c = 5000  # mm²

        with pytest.raises(NegativeValueError):
            Form9Dot12NMinimumLongitudinalReinforcementColumns(n_ed=n_ed, f_yd=f_yd, a_c=a_c)

    def test_raise_error_when_negative_a_c_is_given(self) -> None:
        """Test the evaluation of the result."""
        n_ed = 200  # kN
        f_yd = 500  # MPa
        a_c = -5000  # mm²

        with pytest.raises(NegativeValueError):
            Form9Dot12NMinimumLongitudinalReinforcementColumns(n_ed=n_ed, f_yd=f_yd, a_c=a_c)

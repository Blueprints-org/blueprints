"""Testing formula 9.5N of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_9_detailling_and_specific_rules.formula_9_5n import (
    Form9Dot5NMinimumShearReinforcementRatio,
)
from blueprints.validations import NegativeValueError


class TestForm9Dot5NMinimumShearReinforcementRatio:
    """Validation for formula 9.5N from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_ck = 30  # MPa
        f_yk = 500  # MPa
        form_9_5n = Form9Dot5NMinimumShearReinforcementRatio(f_ck=f_ck, f_yk=f_yk)

        # Expected result, manually calculated
        manually_calculated_result = 0.000876356

        assert form_9_5n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_f_ck_is_given(self) -> None:
        """Test if error is raised when f_ck is negative"""
        f_ck = -30  # MPa
        f_yk = 500  # MPa

        with pytest.raises(NegativeValueError):
            Form9Dot5NMinimumShearReinforcementRatio(f_ck=f_ck, f_yk=f_yk)

    def test_raise_error_when_negative_f_yk_is_given(self) -> None:
        """Test if error is raised when f_yk is negative"""
        f_ck = 30  # MPa
        f_yk = -500  # MPa

        with pytest.raises(NegativeValueError):
            Form9Dot5NMinimumShearReinforcementRatio(f_ck=f_ck, f_yk=f_yk)

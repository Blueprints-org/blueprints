"""Testing formula 9.5N of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_9_detailling_and_specific_rules.formula_9_5n import (
    Form9Dot5nMinimumShearReinforcementRatio,
)
from blueprints.validations import NegativeValueError


class TestForm9Dot5nMinimumShearReinforcementRatio:
    """Validation for formula 9.5N from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_ck = 30  # MPa
        f_yk = 500  # MPa
        form_9_5n = Form9Dot5nMinimumShearReinforcementRatio(f_ck=f_ck, f_yk=f_yk)

        # Expected result, manually calculated
        manually_calculated_result = 0.000876356

        assert form_9_5n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_f_ck_is_given(self) -> None:
        """Test if error is raised when f_ck is negative."""
        f_ck = -30  # MPa
        f_yk = 500  # MPa

        with pytest.raises(NegativeValueError):
            Form9Dot5nMinimumShearReinforcementRatio(f_ck=f_ck, f_yk=f_yk)

    def test_raise_error_when_negative_f_yk_is_given(self) -> None:
        """Test if error is raised when f_yk is negative."""
        f_ck = 30  # MPa
        f_yk = -500  # MPa

        with pytest.raises(NegativeValueError):
            Form9Dot5nMinimumShearReinforcementRatio(f_ck=f_ck, f_yk=f_yk)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\rho_{w,min} = \left( 0.08 \cdot \sqrt{f_{ck}} \right) / f_{yk} = \left( 0.08 \cdot \sqrt{30.00} \right) / 500.00 = 0.000876",
            ),
            ("short", r"\rho_{w,min} = 0.000876"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_ck = 30  # MPa
        f_yk = 500  # MPa

        # Object to test
        form_9_5n_latex = Form9Dot5nMinimumShearReinforcementRatio(f_ck=f_ck, f_yk=f_yk).latex()

        actual = {"complete": form_9_5n_latex.complete, "short": form_9_5n_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

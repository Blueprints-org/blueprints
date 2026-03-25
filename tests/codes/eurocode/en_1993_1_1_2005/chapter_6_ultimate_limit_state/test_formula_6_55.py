"""Testing formula 6.55 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_55 import (
    Form6Dot55DesignBucklingResistanceMoment,
)
from blueprints.validations import (
    LessOrEqualToZeroError,
    NegativeValueError,
)


class TestForm6Dot55DesignBucklingResistanceMoment:
    """Validation for formula 6.55 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        chi_lt = 0.8
        w_y = 500000.0
        f_y = 355.0
        gamma_m1 = 1.0

        # Object to test
        formula = Form6Dot55DesignBucklingResistanceMoment(
            chi_lt=chi_lt,
            w_y=w_y,
            f_y=f_y,
            gamma_m1=gamma_m1,
        )

        # Expected result, manually calculated
        manually_calculated_result = 142000000.0  # Nmm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("chi_lt", "w_y", "f_y", "gamma_m1"),
        [
            (-0.8, 500000.0, 355.0, 1.0),  # chi_lt is negative
            (0.8, -500000.0, 355.0, 1.0),  # w_y is negative
            (0.8, 500000.0, -355.0, 1.0),  # f_y is negative
            (0.8, 500000.0, 355.0, 0.0),  # gamma_m1 is zero
            (0.8, 500000.0, 355.0, -1.0),  # gamma_m1 is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self,
        chi_lt: float,
        w_y: float,
        f_y: float,
        gamma_m1: float,
    ) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot55DesignBucklingResistanceMoment(
                chi_lt=chi_lt,
                w_y=w_y,
                f_y=f_y,
                gamma_m1=gamma_m1,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"M_{b,Rd} = \chi_{LT} \cdot W_y \cdot "
                r"\frac{f_y}{\gamma_{M1}} = "
                r"0.800 \cdot 500000.000 \cdot "
                r"\frac{355.000}{1.000} = 142000000.000 \ Nmm",
            ),
            (
                "complete_with_units",
                r"M_{b,Rd} = \chi_{LT} \cdot W_y \cdot "
                r"\frac{f_y}{\gamma_{M1}} = "
                r"0.800 \cdot 500000.000 \ mm^3 \cdot "
                r"\frac{355.000 \ MPa}{1.000} = 142000000.000 \ Nmm",
            ),
            ("short", r"M_{b,Rd} = 142000000.000 \ Nmm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        chi_lt = 0.8
        w_y = 500000.0
        f_y = 355.0
        gamma_m1 = 1.0

        # Object to test
        latex = Form6Dot55DesignBucklingResistanceMoment(
            chi_lt=chi_lt,
            w_y=w_y,
            f_y=f_y,
            gamma_m1=gamma_m1,
        ).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

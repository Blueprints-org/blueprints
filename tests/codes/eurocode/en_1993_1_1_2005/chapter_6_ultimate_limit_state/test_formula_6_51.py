"""Testing formula 6.51 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_51 import (
    Form6Dot51NonDimensionalSlendernessClass4,
    Form6Dot51NonDimensionalSlendernessFromBucklingLengthClass4,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot51NonDimensionalSlendernessClass4:
    """Validation for formula 6.51 from EN 1993-1-1:2005, the expression with the elastic critical force."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_eff = 4200.0
        f_y = 355.0
        n_cr = 1500000.0

        # Object to test
        formula = Form6Dot51NonDimensionalSlendernessClass4(a_eff=a_eff, f_y=f_y, n_cr=n_cr)

        # Expected result, manually calculated
        # sqrt(4200 * 355 / 1500000) = sqrt(0.994) = 0.996995
        manually_calculated_result = 0.996995  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_eff", "f_y", "n_cr"),
        [
            (-4200.0, 355.0, 1500000.0),  # a_eff is negative
            (4200.0, -355.0, 1500000.0),  # f_y is negative
            (4200.0, 355.0, 0.0),  # n_cr is zero
            (4200.0, 355.0, -1500000.0),  # n_cr is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_eff: float, f_y: float, n_cr: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot51NonDimensionalSlendernessClass4(a_eff=a_eff, f_y=f_y, n_cr=n_cr)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\overline{\lambda} = \sqrt{\frac{A_{eff} \cdot f_y}{N_{cr}}} = "
                    r"\sqrt{\frac{4200.000 \cdot 355.000}{1500000.000}} = 0.997 \ -"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\overline{\lambda} = \sqrt{\frac{A_{eff} \cdot f_y}{N_{cr}}} = "
                    r"\sqrt{\frac{4200.000 \ mm^2 \cdot 355.000 \ MPa}{1500000.000 \ N}} = 0.997 \ -"
                ),
            ),
            ("short", r"\overline{\lambda} = 0.997 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_eff = 4200.0
        f_y = 355.0
        n_cr = 1500000.0

        # Object to test
        latex = Form6Dot51NonDimensionalSlendernessClass4(a_eff=a_eff, f_y=f_y, n_cr=n_cr).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot51NonDimensionalSlendernessFromBucklingLengthClass4:
    """Validation for formula 6.51 from EN 1993-1-1:2005, the expression with the buckling length."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        l_cr = 4000.0
        i = 50.0
        a_eff = 4200.0
        a = 5000.0
        lambda_1 = 76.4

        # Object to test
        formula = Form6Dot51NonDimensionalSlendernessFromBucklingLengthClass4(l_cr=l_cr, i=i, a_eff=a_eff, a=a, lambda_1=lambda_1)

        # Expected result, manually calculated
        # 4000 / 50 * sqrt(4200 / 5000) / 76.4 = 80 * sqrt(0.84) / 76.4 = 80 * 0.916515 / 76.4 = 0.959702
        manually_calculated_result = 0.959702  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("l_cr", "i", "a_eff", "a", "lambda_1"),
        [
            (-4000.0, 50.0, 4200.0, 5000.0, 76.4),  # l_cr is negative
            (4000.0, 0.0, 4200.0, 5000.0, 76.4),  # i is zero
            (4000.0, -50.0, 4200.0, 5000.0, 76.4),  # i is negative
            (4000.0, 50.0, -4200.0, 5000.0, 76.4),  # a_eff is negative
            (4000.0, 50.0, 4200.0, 0.0, 76.4),  # a is zero
            (4000.0, 50.0, 4200.0, -5000.0, 76.4),  # a is negative
            (4000.0, 50.0, 4200.0, 5000.0, 0.0),  # lambda_1 is zero
            (4000.0, 50.0, 4200.0, 5000.0, -76.4),  # lambda_1 is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, l_cr: float, i: float, a_eff: float, a: float, lambda_1: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot51NonDimensionalSlendernessFromBucklingLengthClass4(l_cr=l_cr, i=i, a_eff=a_eff, a=a, lambda_1=lambda_1)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\overline{\lambda} = \frac{L_{cr}}{i} \cdot \frac{\sqrt{\frac{A_{eff}}{A}}}{\lambda_1} = "
                    r"\frac{4000.000}{50.000} \cdot \frac{\sqrt{\frac{4200.000}{5000.000}}}{76.400} = 0.960 \ -"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\overline{\lambda} = \frac{L_{cr}}{i} \cdot \frac{\sqrt{\frac{A_{eff}}{A}}}{\lambda_1} = "
                    r"\frac{4000.000 \ mm}{50.000 \ mm} \cdot \frac{\sqrt{\frac{4200.000 \ mm^2}{5000.000 \ mm^2}}}{76.400} = 0.960 \ -"
                ),
            ),
            ("short", r"\overline{\lambda} = 0.960 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        l_cr = 4000.0
        i = 50.0
        a_eff = 4200.0
        a = 5000.0
        lambda_1 = 76.4

        # Object to test
        latex = Form6Dot51NonDimensionalSlendernessFromBucklingLengthClass4(l_cr=l_cr, i=i, a_eff=a_eff, a=a, lambda_1=lambda_1).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

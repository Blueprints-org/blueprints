"""Testing formula 6.50 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_50 import (
    Form6Dot50NonDimensionalSlendernessClass1And2And3,
    Form6Dot50NonDimensionalSlendernessFromBucklingLengthClass1And2And3,
    SubForm6Dot50SlendernessValueLambda1,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot50NonDimensionalSlendernessClass1And2And3:
    """Validation for formula 6.50 from EN 1993-1-1:2005, the expression with the elastic critical force."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a = 6000.0
        f_y = 235.0
        n_cr = 3000000.0

        # Object to test
        formula = Form6Dot50NonDimensionalSlendernessClass1And2And3(a=a, f_y=f_y, n_cr=n_cr)

        # Expected result, manually calculated
        # sqrt(6000 * 235 / 3000000) = sqrt(0.47) = 0.685565
        manually_calculated_result = 0.685565  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a", "f_y", "n_cr"),
        [
            (-6000.0, 235.0, 3000000.0),  # a is negative
            (6000.0, -235.0, 3000000.0),  # f_y is negative
            (6000.0, 235.0, 0.0),  # n_cr is zero
            (6000.0, 235.0, -3000000.0),  # n_cr is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a: float, f_y: float, n_cr: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot50NonDimensionalSlendernessClass1And2And3(a=a, f_y=f_y, n_cr=n_cr)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\overline{\lambda} = \sqrt{\frac{A \cdot f_y}{N_{cr}}} = "
                    r"\sqrt{\frac{6000.000 \cdot 235.000}{3000000.000}} = 0.686 \ -"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\overline{\lambda} = \sqrt{\frac{A \cdot f_y}{N_{cr}}} = "
                    r"\sqrt{\frac{6000.000 \ mm^2 \cdot 235.000 \ MPa}{3000000.000 \ N}} = 0.686 \ -"
                ),
            ),
            ("short", r"\overline{\lambda} = 0.686 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a = 6000.0
        f_y = 235.0
        n_cr = 3000000.0

        # Object to test
        latex = Form6Dot50NonDimensionalSlendernessClass1And2And3(a=a, f_y=f_y, n_cr=n_cr).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot50NonDimensionalSlendernessFromBucklingLengthClass1And2And3:
    """Validation for formula 6.50 from EN 1993-1-1:2005, the expression with the buckling length."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        l_cr = 4000.0
        i = 50.0
        lambda_1 = 76.4

        # Object to test
        formula = Form6Dot50NonDimensionalSlendernessFromBucklingLengthClass1And2And3(l_cr=l_cr, i=i, lambda_1=lambda_1)

        # Expected result, manually calculated
        # 4000 / 50 * 1 / 76.4 = 80 / 76.4 = 1.047120
        manually_calculated_result = 1.047120  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("l_cr", "i", "lambda_1"),
        [
            (-4000.0, 50.0, 76.4),  # l_cr is negative
            (4000.0, 0.0, 76.4),  # i is zero
            (4000.0, -50.0, 76.4),  # i is negative
            (4000.0, 50.0, 0.0),  # lambda_1 is zero
            (4000.0, 50.0, -76.4),  # lambda_1 is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, l_cr: float, i: float, lambda_1: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot50NonDimensionalSlendernessFromBucklingLengthClass1And2And3(l_cr=l_cr, i=i, lambda_1=lambda_1)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\overline{\lambda} = \frac{L_{cr}}{i} \cdot \frac{1}{\lambda_1} = "
                    r"\frac{4000.000}{50.000} \cdot \frac{1}{76.400} = 1.047 \ -"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\overline{\lambda} = \frac{L_{cr}}{i} \cdot \frac{1}{\lambda_1} = "
                    r"\frac{4000.000 \ mm}{50.000 \ mm} \cdot \frac{1}{76.400} = 1.047 \ -"
                ),
            ),
            ("short", r"\overline{\lambda} = 1.047 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        l_cr = 4000.0
        i = 50.0
        lambda_1 = 76.4

        # Object to test
        latex = Form6Dot50NonDimensionalSlendernessFromBucklingLengthClass1And2And3(l_cr=l_cr, i=i, lambda_1=lambda_1).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestSubForm6Dot50SlendernessValueLambda1:
    """Validation for the sub-formula of formulas 6.50 and 6.51 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        e = 210000.0
        f_y = 355.0

        # Object to test
        formula = SubForm6Dot50SlendernessValueLambda1(e=e, f_y=f_y)

        # Expected result, manually calculated
        # pi * sqrt(210000 / 355) = 3.141593 * sqrt(591.549296) = 3.141593 * 24.321787 = 76.409146
        manually_calculated_result = 76.409146  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("e", "f_y"),
        [
            (-210000.0, 355.0),  # e is negative
            (210000.0, 0.0),  # f_y is zero
            (210000.0, -355.0),  # f_y is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, e: float, f_y: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            SubForm6Dot50SlendernessValueLambda1(e=e, f_y=f_y)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\lambda_1 = \pi \cdot \sqrt{\frac{E}{f_y}} = \pi \cdot \sqrt{\frac{210000.000}{355.000}} = 76.409 \ -",
            ),
            (
                "complete_with_units",
                r"\lambda_1 = \pi \cdot \sqrt{\frac{E}{f_y}} = \pi \cdot \sqrt{\frac{210000.000 \ MPa}{355.000 \ MPa}} = 76.409 \ -",
            ),
            ("short", r"\lambda_1 = 76.409 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        e = 210000.0
        f_y = 355.0

        # Object to test
        latex = SubForm6Dot50SlendernessValueLambda1(e=e, f_y=f_y).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

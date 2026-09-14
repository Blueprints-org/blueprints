"""Testing formula 8.114 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_114 import (
    Form8Dot114CheckCompressiveStressInStrutOrCompressionField,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot114CheckCompressiveStressInStrutOrCompressionField:
    """Validation for formula 8.114 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("sigma_cd", "nu", "f_cd", "expected"),
        [
            (2.5, 0.7, 25.0, True),  # the strut resists the compressive stress
            (17.5, 0.7, 25.0, True),  # exactly on the boundary, which the standard includes
            (20.0, 0.7, 25.0, False),  # the strut does not resist the compressive stress
        ],
    )
    def test_evaluation(self, sigma_cd: float, nu: float, f_cd: float, expected: bool) -> None:
        """Tests the evaluation of the result."""
        assert bool(Form8Dot114CheckCompressiveStressInStrutOrCompressionField(sigma_cd=sigma_cd, nu=nu, f_cd=f_cd)) is expected

    @pytest.mark.parametrize(
        ("sigma_cd", "nu", "f_cd"),
        [
            (-2.5, 0.7, 25.0),  # sigma_cd is negative
            (2.5, -0.7, 25.0),  # nu is negative
            (2.5, 0.0, 25.0),  # nu is zero
            (2.5, 0.7, -25.0),  # f_cd is negative
            (2.5, 0.7, 0.0),  # f_cd is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, sigma_cd: float, nu: float, f_cd: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot114CheckCompressiveStressInStrutOrCompressionField(sigma_cd=sigma_cd, nu=nu, f_cd=f_cd)

    @pytest.mark.parametrize(
        ("sigma_cd", "representation", "expected"),
        [
            (2.5, "complete", r"CHECK \to \sigma_{cd} \leq \nu \cdot f_{cd} \to 2.500 \leq 0.700 \cdot 25.000 \to OK"),
            (
                2.5,
                "complete_with_units",
                r"CHECK \to \sigma_{cd} \leq \nu \cdot f_{cd} \to 2.500 \ MPa \leq 0.700 \cdot 25.000 \ MPa \to OK",
            ),
            (2.5, "short", r"CHECK \to OK"),
            (20.0, "short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, sigma_cd: float, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = Form8Dot114CheckCompressiveStressInStrutOrCompressionField(sigma_cd=sigma_cd, nu=0.7, f_cd=25.0).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

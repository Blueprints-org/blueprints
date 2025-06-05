"""Testing formula 3.24 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_24_25 import (
    Form3Dot24And25IncreasedCharacteristicCompressiveStrength,
)
from blueprints.validations import NegativeValueError


class TestForm3Dot24And25IncreasedCharacteristicCompressiveStrength:
    """Validation for formula 3.24 and 3.25 from EN 1992-1-1:2004."""

    def test_evaluation_small_sigma_2(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_ck = 12.2  # MPa
        sigma_2 = 0.03 * f_ck  # MPa

        form_3_24 = Form3Dot24And25IncreasedCharacteristicCompressiveStrength(f_ck=f_ck, sigma_2=sigma_2)

        # Expected result, manually calculated
        manually_calculated_result = 14.03

        assert form_3_24 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_f_ck_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        f_ck = -12.2  # MPa
        sigma_2 = 0.03 * f_ck  # MPa

        with pytest.raises(NegativeValueError):
            Form3Dot24And25IncreasedCharacteristicCompressiveStrength(f_ck=f_ck, sigma_2=sigma_2)

    def test_evaluation_large_sigma_2(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_ck = 12.2  # MPa
        sigma_2 = 0.08 * f_ck  # MPa

        form_3_25 = Form3Dot24And25IncreasedCharacteristicCompressiveStrength(f_ck=f_ck, sigma_2=sigma_2)

        # Expected result, manually calculated
        manually_calculated_result = 16.165

        assert form_3_25 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"f_{ck,c} = f_{ck} \cdot (1.000 + 5.0 \cdot \sigma_2 / f_{ck}) = 12.20 \cdot (1.000 + 5.0 \cdot 0.50 / 12.20) = 14.70",
            ),
            ("short", r"f_{ck,c} = 14.70"),
        ],
    )
    def test_latex_below_0dot05fck(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_ck = 12.2  # MPa
        sigma_2 = 0.5  # MPa

        # Object to test
        form_3_24_25_latex = Form3Dot24And25IncreasedCharacteristicCompressiveStrength(f_ck=f_ck, sigma_2=sigma_2).latex()

        actual = {"complete": form_3_24_25_latex.complete, "short": form_3_24_25_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"f_{ck,c} = f_{ck} \cdot (1.125 + 2.5 \cdot \sigma_2 / f_{ck}) = 12.20 \cdot (1.125 + 2.5 \cdot 1.00 / 12.20) = 16.23",
            ),
            ("short", r"f_{ck,c} = 16.23"),
        ],
    )
    def test_latex_above_0dot05fck(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_ck = 12.2  # MPa
        sigma_2 = 1  # MPa

        # Object to test
        form_3_24_25_latex = Form3Dot24And25IncreasedCharacteristicCompressiveStrength(f_ck=f_ck, sigma_2=sigma_2).latex()

        actual = {"complete": form_3_24_25_latex.complete, "short": form_3_24_25_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

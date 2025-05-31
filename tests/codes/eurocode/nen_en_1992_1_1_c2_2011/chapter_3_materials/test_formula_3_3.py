"""Testing formula 3.3 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_3 import (
    Form3Dot3AxialTensileStrengthFromTensileSplittingStrength,
)


class TestForm3Dot3AxialTensileStrengthFromTensileSplittingStrength:
    """Validation for formula 3.3 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_ct_sp = 3.4  # MPa
        form_3_3 = Form3Dot3AxialTensileStrengthFromTensileSplittingStrength(f_ct_sp=f_ct_sp)

        # Expected result, manually calculated
        manually_calculated_result = 3.06

        assert form_3_3 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_f_ct_sp_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_ct_sp = -3.4  # MPa

        with pytest.raises(ValueError):
            Form3Dot3AxialTensileStrengthFromTensileSplittingStrength(f_ct_sp=f_ct_sp)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"f_{ct} = 0.9 \cdot f_{ct,sp} = 0.9 \cdot 3.400 = 3.060",
            ),
            ("short", r"f_{ct} = 3.060"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_ct_sp = 3.4  # MPa

        # Object to test
        form_3_3_latex = Form3Dot3AxialTensileStrengthFromTensileSplittingStrength(f_ct_sp=f_ct_sp).latex()

        actual = {"complete": form_3_3_latex.complete, "short": form_3_3_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

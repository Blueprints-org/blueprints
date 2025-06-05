"""Testing formula 3.12 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_12 import Form3Dot12AutogeneShrinkageInfinity


class TestForm3Dot11AutogeneShrinkage:
    """Validation for formula 3.12 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_ck = 15.8  # MPa
        form_3_12 = Form3Dot12AutogeneShrinkageInfinity(f_ck=f_ck)

        # Expected result, manually calculated
        manually_calculated_result = 1.45e-5

        assert form_3_12 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_f_ck_is_given(self) -> None:
        """Test formula raising error by a negative value."""
        # Example values
        f_ck = -15.8  # MPa

        with pytest.raises(ValueError):
            Form3Dot12AutogeneShrinkageInfinity(f_ck=f_ck)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\epsilon_{ca}(\infty) = 2.5 \cdot (f_{ck} - 10) \cdot 10^{-6} = 2.5 \cdot (15.800 - 10) \cdot 10^{-6} = 0.000015",
            ),
            ("short", r"\epsilon_{ca}(\infty) = 0.000015"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_ck = 15.8  # MPa

        # Object to test
        form_3_12_latex = Form3Dot12AutogeneShrinkageInfinity(f_ck=f_ck).latex()

        actual = {"complete": form_3_12_latex.complete, "short": form_3_12_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

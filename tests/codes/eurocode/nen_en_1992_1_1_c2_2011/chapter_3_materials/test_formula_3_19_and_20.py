"""Testing formula 3.19 and 20 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_19_20 import Form3Dot19And20EffectivePressureZoneHeight


class TestForm3Dot19And20EffectivePressureZoneHeight:
    """Validation for formula 3.19 and 20 from EN 1992-1-1:2004."""

    def test_evaluation_1(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_ck = 18.50  # MPa

        form_3_19_20 = Form3Dot19And20EffectivePressureZoneHeight(f_ck=f_ck)

        # Expected result, manually calculated
        manually_calculated_result = 0.8

        assert form_3_19_20 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_2(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_ck = 83.5  # MPa

        form_3_19_20 = Form3Dot19And20EffectivePressureZoneHeight(f_ck=f_ck)

        # Expected result, manually calculated
        manually_calculated_result = 0.71625

        assert form_3_19_20 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_f_ck_is_larger_than_90(self) -> None:
        """Test a too large value."""
        # Example values
        f_ck = 105  # MPa

        with pytest.raises(ValueError):
            Form3Dot19And20EffectivePressureZoneHeight(f_ck=f_ck)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\lambda = 0.8 = 0.8 = 0.800",
            ),
            ("short", r"\lambda = 0.800"),
        ],
    )
    def test_latex_below_50(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_ck = 18.50  # -

        # Object to test
        form_3_19_20_latex = Form3Dot19And20EffectivePressureZoneHeight(f_ck=f_ck).latex()

        actual = {"complete": form_3_19_20_latex.complete, "short": form_3_19_20_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\lambda = 0.8 - (f_{ck} - 50) / 400 = 0.8 - (83.500 - 50) / 400 = 0.716",
            ),
            ("short", r"\lambda = 0.716"),
        ],
    )
    def test_latex_above_50(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_ck = 83.5  # -

        # Object to test
        form_3_19_20_latex = Form3Dot19And20EffectivePressureZoneHeight(f_ck=f_ck).latex()

        actual = {"complete": form_3_19_20_latex.complete, "short": form_3_19_20_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

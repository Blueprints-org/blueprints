"""Testing formula 3.27 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_27 import Form3Dot27IncreasedStrainLimitValue


class TestForm3Dot27IncreasedStrainLimitValue:
    """Validation for formula 3.27 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_ck = 12.2  # MPa
        sigma_2 = 0.08  # MPa
        epsilon_cu2 = 0.33  # -

        form_3_27 = Form3Dot27IncreasedStrainLimitValue(f_ck=f_ck, sigma_2=sigma_2, epsilon_cu2=epsilon_cu2)

        # Expected result, manually calculated
        manually_calculated_result = 0.331311

        assert form_3_27 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_f_ck_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        f_ck = -12.2  # MPa
        sigma_2 = 0.08  # MPa
        epsilon_cu2 = 0.33  # -

        with pytest.raises(ValueError):
            Form3Dot27IncreasedStrainLimitValue(f_ck=f_ck, sigma_2=sigma_2, epsilon_cu2=epsilon_cu2)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\epsilon_{cu2,c} = \epsilon_{cu2} + 0.2 \cdot \sigma_2 / f_{ck} = 0.330 + 0.2 \cdot 0.080 / 12.200 = 0.331",
            ),
            ("short", r"\epsilon_{cu2,c} = 0.331"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_ck = 12.2  # MPa
        sigma_2 = 0.08  # MPa
        epsilon_cu2 = 0.33  # -

        # Object to test
        form_3_27_latex = Form3Dot27IncreasedStrainLimitValue(f_ck=f_ck, sigma_2=sigma_2, epsilon_cu2=epsilon_cu2).latex()

        actual = {"complete": form_3_27_latex.complete, "short": form_3_27_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

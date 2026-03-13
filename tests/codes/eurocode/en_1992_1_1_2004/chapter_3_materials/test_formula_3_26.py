"""Testing formula 3.26 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_26 import Form3Dot26IncreasedStrainAtMaxStrength


class TestForm3Dot26IncreasedStrainAtMaxStrength:
    """Validation for formula 3.26 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_ck = 12.2  # MPa
        f_ck_c = 14.08  # MPa
        epsilon_c2 = 0.33  # -

        form_3_26 = Form3Dot26IncreasedStrainAtMaxStrength(f_ck=f_ck, f_ck_c=f_ck_c, epsilon_c2=epsilon_c2)

        # Expected result, manually calculated
        manually_calculated_result = 0.43954

        assert form_3_26 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_f_ck_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        f_ck = -12.2  # MPa
        f_ck_c = 14.08  # MPa
        epsilon_c2 = 0.33  # -

        with pytest.raises(ValueError):
            Form3Dot26IncreasedStrainAtMaxStrength(f_ck=f_ck, f_ck_c=f_ck_c, epsilon_c2=epsilon_c2)

    def test_raise_error_when_negative_f_ck_c_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        f_ck = 12.2  # MPa
        f_ck_c = -14.08  # MPa
        epsilon_c2 = 0.33  # -

        with pytest.raises(ValueError):
            Form3Dot26IncreasedStrainAtMaxStrength(f_ck=f_ck, f_ck_c=f_ck_c, epsilon_c2=epsilon_c2)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\epsilon_{c2,c} = \epsilon_{c2} \cdot ( f_{ck,c} / f_{ck} )^2 = 0.330 \cdot ( 14.080 / 12.200 )^2 = 0.440",
            ),
            ("short", r"\epsilon_{c2,c} = 0.440"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_ck = 12.2  # MPa
        f_ck_c = 14.08  # MPa
        epsilon_c2 = 0.33  # -

        # Object to test
        form_3_26_latex = Form3Dot26IncreasedStrainAtMaxStrength(f_ck=f_ck, f_ck_c=f_ck_c, epsilon_c2=epsilon_c2).latex()

        actual = {"complete": form_3_26_latex.complete, "short": form_3_26_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

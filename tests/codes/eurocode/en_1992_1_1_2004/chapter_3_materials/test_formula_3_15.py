"""Testing formula 3.15 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_15 import Form3Dot15DesignValueCompressiveStrength


class TestForm3Dot15DesignValueCompressiveStrength:
    """Validation for formula 3.15 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        alpha_cc = 1.0  # -
        f_ck = 10.5  # MPa
        gamma_c = 0.8

        form_3_15 = Form3Dot15DesignValueCompressiveStrength(alpha_cc=alpha_cc, f_ck=f_ck, gamma_c=gamma_c)

        # Expected result, manually calculated
        manually_calculated_result = 13.125

        assert form_3_15 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_alpha_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        alpha_cc = -1.0  # -
        f_ck = 10.5  # MPa
        gamma_c = 0.8

        with pytest.raises(ValueError):
            Form3Dot15DesignValueCompressiveStrength(alpha_cc=alpha_cc, f_ck=f_ck, gamma_c=gamma_c)

    def test_raise_error_when_negative_f_ck_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        alpha_cc = 1.0  # -
        f_ck = -10.5  # MPa
        gamma_c = 0.8

        with pytest.raises(ValueError):
            Form3Dot15DesignValueCompressiveStrength(alpha_cc=alpha_cc, f_ck=f_ck, gamma_c=gamma_c)

    def test_raise_error_when_negative_gamma_c_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        alpha_cc = 1.0  # -
        f_ck = 10.5  # MPa
        gamma_c = -0.8

        with pytest.raises(ValueError):
            Form3Dot15DesignValueCompressiveStrength(alpha_cc=alpha_cc, f_ck=f_ck, gamma_c=gamma_c)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"f_{cd} = \alpha_{cc} \cdot f_{ck} / \gamma_C = 1.000 \cdot 10.500 / 0.800 = 13.125",
            ),
            ("short", r"f_{cd} = 13.125"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        alpha_cc = 1.0  # -
        f_ck = 10.5  # MPa
        gamma_c = 0.8

        # Object to test
        form_3_15_latex = Form3Dot15DesignValueCompressiveStrength(alpha_cc=alpha_cc, f_ck=f_ck, gamma_c=gamma_c).latex()

        actual = {"complete": form_3_15_latex.complete, "short": form_3_15_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

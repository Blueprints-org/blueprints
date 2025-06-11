"""Testing formula 3.4 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_4 import Form3Dot4DevelopmentTensileStrength


class TestForm3Dot4DevelopmentTensileStrength:
    """Validation for formula 3.4 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        beta_cc_t = 0.32  # -
        alpha = 2 / 3  # -
        f_ctm = 3.45  # MPa
        form_3_4 = Form3Dot4DevelopmentTensileStrength(beta_cc_t=beta_cc_t, alpha=alpha, f_ctm=f_ctm)

        # Expected result, manually calculated
        manually_calculated_result = 1.614058

        assert form_3_4 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_alpha_is_given(self) -> None:
        """Test that an error is raised when alpha is negative."""
        # Example values
        beta_cc_t = 0.32  # -> Positive
        alpha = -0.4  # -> Negative
        f_ctm = 3.45  # MPa -> Positive

        with pytest.raises(ValueError):
            Form3Dot4DevelopmentTensileStrength(beta_cc_t=beta_cc_t, alpha=alpha, f_ctm=f_ctm)

    def test_raise_error_when_negative_beta_cc_t_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        beta_cc_t = -0.32  # - -> Negative
        alpha = 2 / 3  # - -> Equal to 1 or 2/3
        f_ctm = 3.45  # MPa -> Positive

        with pytest.raises(ValueError):
            Form3Dot4DevelopmentTensileStrength(beta_cc_t=beta_cc_t, alpha=alpha, f_ctm=f_ctm)

    def test_raise_error_when_negative_f_ctm_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        beta_cc_t = 0.32  # - -> Positive
        alpha = 2 / 3  # - -> unequal to 1 or 2/3
        f_ctm = -3.45  # MPa -> Negative

        with pytest.raises(ValueError):
            Form3Dot4DevelopmentTensileStrength(beta_cc_t=beta_cc_t, alpha=alpha, f_ctm=f_ctm)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"f_{ctm}(t) = (\beta_{cc}(t))^{\alpha} \cdot f_{ctm} = (0.320)^{0.667} \cdot 3.450 = 1.614",
            ),
            ("short", r"f_{ctm}(t) = 1.614"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        beta_cc_t = 0.32  # -
        alpha = 2 / 3  # -
        f_ctm = 3.45  # MPa

        # Object to test
        form_3_4_latex = Form3Dot4DevelopmentTensileStrength(beta_cc_t=beta_cc_t, alpha=alpha, f_ctm=f_ctm).latex()

        actual = {"complete": form_3_4_latex.complete, "short": form_3_4_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

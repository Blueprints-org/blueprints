"""Testing sub-formula 2 from 8.15 from EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_4 import Form3Dot4DevelopmentTensileStrength
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_15 import (
    SubForm8Dot15TensileStrengthAtRelease,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestSubForm8Dot15TensileStrengthAtRelease:
    """Validation for sub-formula 2 from 8.15 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        alpha_ct = 1.0  # [-]
        f_ctm_t = 2.5  # [MPa]
        gamma_c = 1.5  # [-]
        sub_form_8_15 = SubForm8Dot15TensileStrengthAtRelease(
            alpha_ct=alpha_ct,
            f_ctm_t=f_ctm_t,
            gamma_c=gamma_c,
        )

        # manually calculated result
        manually_calculated_result = 1.166666666666  # [MPa]

        assert sub_form_8_15 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_negative_alpha_ct(self) -> None:
        """Test if NegativeValueError is raised for negative alpha_ct."""
        # example values
        alpha_ct = -1.0  # [-]
        f_ctm_t = 2.5  # [MPa]
        gamma_c = 1.5  # [-]
        with pytest.raises(NegativeValueError):
            SubForm8Dot15TensileStrengthAtRelease(
                alpha_ct=alpha_ct,
                f_ctm_t=f_ctm_t,
                gamma_c=gamma_c,
            )

    def test_negative_f_ctd_t(self) -> None:
        """Test if NegativeValueError is raised for negative f_ctd_t."""
        # example values
        alpha_ct = 1.0  # [-]
        f_ctm_t = -2.5  # [MPa]
        gamma_c = 1.5  # [-]
        with pytest.raises(NegativeValueError):
            SubForm8Dot15TensileStrengthAtRelease(
                alpha_ct=alpha_ct,
                f_ctm_t=f_ctm_t,
                gamma_c=gamma_c,
            )

    def test_negative_gamma_c(self) -> None:
        """Test if LessOrEqualToZeroError is raised for negative gamma_c."""
        # example values
        alpha_ct = 1.0  # [-]
        f_ctm_t = 2.5  # [MPa]
        gamma_c = -1.5  # [-]
        with pytest.raises(LessOrEqualToZeroError):
            SubForm8Dot15TensileStrengthAtRelease(
                alpha_ct=alpha_ct,
                f_ctm_t=f_ctm_t,
                gamma_c=gamma_c,
            )

    def test_zero_gamma_c(self) -> None:
        """Test if LessOrEqualToZeroError is raised for zero gamma_c."""
        # example values
        alpha_ct = 1.0  # [-]
        f_ctm_t = 2.5  # [MPa]
        gamma_c = 0.0  # [-]
        with pytest.raises(LessOrEqualToZeroError):
            SubForm8Dot15TensileStrengthAtRelease(
                alpha_ct=alpha_ct,
                f_ctm_t=f_ctm_t,
                gamma_c=gamma_c,
            )

    def test_integration_with_form_3_4(self) -> None:
        """Test the integration with Form3Dot4DevelopmentTensileStrength."""
        # example values
        alpha_ct = 1.0  # [-]
        gamma_c = 1.5  # [-]
        beta_cc_t = 0.7  # [-]
        alpha = 1.0  # [-]
        f_ctm = 2.5  # [MPa]
        f_ctm_t = Form3Dot4DevelopmentTensileStrength(beta_cc_t=beta_cc_t, alpha=alpha, f_ctm=f_ctm)

        sub_form_8_15 = SubForm8Dot15TensileStrengthAtRelease(
            alpha_ct=alpha_ct,
            f_ctm_t=f_ctm_t,
            gamma_c=gamma_c,
        )

        # manually calculated result
        manually_calculated_result = 0.816666666  # [MPa]

        assert sub_form_8_15 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (r"f_{ctd}(t) = \frac{\alpha_{ct} \cdot 0.7 \cdot f_{ctm}(t)}{\gamma_c} = \frac{1.00 \cdot 0.7 \cdot 1.75}{1.50} = 0.82"),
            ),
            ("short", r"f_{ctd}(t) = 0.82"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # example values
        alpha_ct = 1.0  # [-]
        gamma_c = 1.5  # [-]
        beta_cc_t = 0.7  # [-]
        alpha = 1.0  # [-]
        f_ctm = 2.5  # [MPa]
        f_ctm_t = Form3Dot4DevelopmentTensileStrength(beta_cc_t=beta_cc_t, alpha=alpha, f_ctm=f_ctm)

        # Object to test
        form_8_15_p2_latex = SubForm8Dot15TensileStrengthAtRelease(
            alpha_ct=alpha_ct,
            f_ctm_t=f_ctm_t,
            gamma_c=gamma_c,
        ).latex()

        actual = {"complete": form_8_15_p2_latex.complete, "short": form_8_15_p2_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

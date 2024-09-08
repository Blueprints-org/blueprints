"""Testing formula 3.7 of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials.formula_3_7 import Form3Dot7NonLinearCreepCoefficient


class TestForm3Dot7NonLinearCreepCoefficient:
    """Validation for formula 3.7 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        phi_inf_t0 = 0.25  # -
        k_sigma = 2.47  # days
        form_3_7 = Form3Dot7NonLinearCreepCoefficient(phi_inf_t0=phi_inf_t0, k_sigma=k_sigma)

        # Expected result, manually calculated
        manually_calculated_result = 5.174308

        assert form_3_7 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_phi_inf_t0_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        phi_inf_t0 = -0.25  # -
        k_sigma = 2.47  # days

        with pytest.raises(ValueError):
            Form3Dot7NonLinearCreepCoefficient(phi_inf_t0=phi_inf_t0, k_sigma=k_sigma)

    def test_raise_error_when_negative_k_sigma_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        phi_inf_t0 = 0.25  # -
        k_sigma = -2.47  # days

        with pytest.raises(ValueError):
            Form3Dot7NonLinearCreepCoefficient(phi_inf_t0=phi_inf_t0, k_sigma=k_sigma)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\varphi_{nl}(\infty, t_0) = \varphi(\infty, t_0) \cdot \exp( 1.5 ( k_{\sigma} - 0.45)) = 0.250 \cdot \exp( 1.5 ( 2.470 - 0.45)) = "
                r"5.174",
            ),
            ("short", r"\varphi_{nl}(\infty, t_0) = 5.174"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        phi_inf_t0 = 0.25  # -
        k_sigma = 2.47  # days

        # Object to test
        form_3_7_latex = Form3Dot7NonLinearCreepCoefficient(phi_inf_t0=phi_inf_t0, k_sigma=k_sigma).latex()

        actual = {"complete": form_3_7_latex.complete, "short": form_3_7_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

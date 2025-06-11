"""Testing formula 3.6 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_6 import Form3Dot6CreepDeformationOfConcrete


class TestForm3Dot6CreepDeformationOfConcrete:
    """Validation for formula 3.6 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        phi_inf_t0 = 0.34  # -
        sigma_c = 0.75  # MPa
        e_c = 2.45  # MPa
        form_3_6 = Form3Dot6CreepDeformationOfConcrete(phi_inf_t0=phi_inf_t0, sigma_c=sigma_c, e_c=e_c)

        # Expected result, manually calculated
        manually_calculated_result = 0.1040816

        assert form_3_6 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_phi_inf_t0_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        phi_inf_t0 = -0.34  # -
        sigma_c = 0.75  # MPa
        e_c = 2.45  # MPa

        with pytest.raises(ValueError):
            Form3Dot6CreepDeformationOfConcrete(phi_inf_t0=phi_inf_t0, sigma_c=sigma_c, e_c=e_c)

    def test_raise_error_when_negative_sigma_c_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        phi_inf_t0 = 0.34  # -
        sigma_c = -0.75  # MPa
        e_c = 2.45  # MPa

        with pytest.raises(ValueError):
            Form3Dot6CreepDeformationOfConcrete(phi_inf_t0=phi_inf_t0, sigma_c=sigma_c, e_c=e_c)

    def test_raise_error_when_negative_e_c_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        phi_inf_t0 = 0.34  # -
        sigma_c = 0.75  # MPa
        e_c = -2.45  # MPa

        with pytest.raises(ValueError):
            Form3Dot6CreepDeformationOfConcrete(phi_inf_t0=phi_inf_t0, sigma_c=sigma_c, e_c=e_c)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\epsilon_{cc}(\infty, t_0) = \varphi(\infty, t_0) \cdot ( \sigma_c / E_c ) = 0.340 \cdot ( 0.750 / 2.450 ) = 0.104",
            ),
            ("short", r"\epsilon_{cc}(\infty, t_0) = 0.104"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        phi_inf_t0 = 0.34  # -
        sigma_c = 0.75  # MPa
        e_c = 2.45  # MPa

        # Object to test
        form_3_6_latex = Form3Dot6CreepDeformationOfConcrete(phi_inf_t0=phi_inf_t0, sigma_c=sigma_c, e_c=e_c).latex()

        actual = {"complete": form_3_6_latex.complete, "short": form_3_6_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

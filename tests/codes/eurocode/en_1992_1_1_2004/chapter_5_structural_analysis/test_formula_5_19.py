"""Testing formula 5.19 from EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_19 import Form5Dot19EffectiveCreepCoefficient
from blueprints.validations import LessOrEqualToZeroError


class TestForm5Dot19EffectiveCreepCoefficient:
    """Validation for formula 5.19 from EN 1992-1-1:2004."""

    @pytest.fixture
    def form_5_19(self) -> Form5Dot19EffectiveCreepCoefficient:
        """Setup and teardown for test."""
        return Form5Dot19EffectiveCreepCoefficient(phi_inf_t0=2.0, m0_eqp=100, m0_ed=200)

    def test_evaluation(self, form_5_19: Form5Dot19EffectiveCreepCoefficient) -> None:
        """Test the evaluation of the result."""
        # Expected result, manually calculated
        manually_calculated_result = 2.0 * (100 / 200)
        assert form_5_19 == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("phi_inf_t0", "m0_eqp", "m0_ed"),
        [
            (2.0, 100, 0),
        ],
    )
    def test_raise_error_when_zero_pars_are_given(self, phi_inf_t0: float, m0_eqp: float, m0_ed: float) -> None:
        """Test zero values for m0_eqp, m0_ed."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot19EffectiveCreepCoefficient(phi_inf_t0=phi_inf_t0, m0_eqp=m0_eqp, m0_ed=m0_ed)

    @pytest.mark.parametrize(
        ("phi_inf_t0", "m0_eqp", "m0_ed", "expected"),
        [
            (2.0, 100, 200, 1.0),
            (1.5, 150, 300, 0.75),
        ],
    )
    def test_properties(self, phi_inf_t0: float, m0_eqp: float, m0_ed: float, expected: float) -> None:
        """Test the properties of the formula."""
        form_5_19 = Form5Dot19EffectiveCreepCoefficient(phi_inf_t0=phi_inf_t0, m0_eqp=m0_eqp, m0_ed=m0_ed)
        assert form_5_19 == pytest.approx(expected, rel=1e-4)

    def test_latex(self, form_5_19: Form5Dot19EffectiveCreepCoefficient) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        form_5_19_latex = form_5_19.latex()
        expected_complete = r"\phi_{ef} = \phi (\infty,t_0) \cdot \frac{M_{0,Eqp}}{M_{0,Ed}} = 2.0 \cdot \frac{100}{200} = 1.000"
        expected_short = r"\phi_{ef} = 1.000"

        assert form_5_19_latex.complete == expected_complete, "Complete representation failed."
        assert form_5_19_latex.short == expected_short, "Short representation failed."

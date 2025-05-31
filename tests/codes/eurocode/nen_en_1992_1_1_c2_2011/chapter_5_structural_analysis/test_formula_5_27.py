"""Testing formula 5.27 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_27 import Form5Dot27EffectiveDesignModulusElasticity
from blueprints.validations import NegativeValueError


class TestForm5Dot27EffectiveDesignModulusElasticity:
    """Validation for formula 5.27 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        e_cd = 30000  # MPA
        phi_ef = 2.0  # Dimensionless

        # Object to test
        form_5_27 = Form5Dot27EffectiveDesignModulusElasticity(e_cd=e_cd, phi_ef=phi_ef)

        # Expected result, manually calculated
        manually_calculated_result = 10000.0  # MPA

        assert form_5_27 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_e_cd_is_given(self) -> None:
        """Test a negative value for e_cd."""
        # Example values
        e_cd = -30000
        phi_ef = 2.0

        with pytest.raises(NegativeValueError):
            Form5Dot27EffectiveDesignModulusElasticity(e_cd=e_cd, phi_ef=phi_ef)

    def test_raise_error_when_negative_phi_ef_is_given(self) -> None:
        """Test a negative value for phi_ef."""
        # Example values
        e_cd = 30000
        phi_ef = -2.0

        with pytest.raises(NegativeValueError):
            Form5Dot27EffectiveDesignModulusElasticity(e_cd=e_cd, phi_ef=phi_ef)

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            ("complete", r"E_{cd,eff} = \frac{E_{cd}}{1 + \phi_{ef}} = \frac{30000.000}{1 + 2.000} = 10000.000"),
            ("short", "E_{cd,eff} = 10000.000"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        e_cd = 30000  # MPA
        phi_ef = 2.0  # Dimensionless

        # Object to test
        form_5_27_latex = Form5Dot27EffectiveDesignModulusElasticity(e_cd=e_cd, phi_ef=phi_ef).latex()

        actual = {
            "complete": form_5_27_latex.complete,
            "short": form_5_27_latex.short,
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."

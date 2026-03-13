"""Testing formula 8.2 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_2 import (
    Form8Dot2UltimateBondStress,
    SubForm8Dot2CoefficientBarDiameter,
    SubForm8Dot2CoefficientQualityOfBond,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot2UltimateBondStress:
    """Validation for formula 8.2 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        eta_1 = 1  # -
        eta_2 = 1  # −
        f_ctd = 20  # MPa
        form_8_2 = Form8Dot2UltimateBondStress(eta_1=eta_1, eta_2=eta_2, f_ctd=f_ctd)

        # Expected result, manually calculated
        manually_calculated_result = 45  # MPa

        assert form_8_2 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_eta_1_is_given(self) -> None:
        """Test if NegativeValueError is raised when a negative value is given for eta_1."""
        # Example values
        eta_1 = -1  # -
        eta_2 = 1  # −
        f_ctd = 20  # MPa

        with pytest.raises(NegativeValueError):
            Form8Dot2UltimateBondStress(eta_1=eta_1, eta_2=eta_2, f_ctd=f_ctd)

    def test_raise_error_when_negative_eta_2_is_given(self) -> None:
        """Test if NegativeValueError is raised when a negative value is given for eta_2."""
        # Example values
        eta_1 = 1  # -
        eta_2 = -1  # −
        f_ctd = 20  # MPa

        with pytest.raises(NegativeValueError):
            Form8Dot2UltimateBondStress(eta_1=eta_1, eta_2=eta_2, f_ctd=f_ctd)

    def test_raise_error_when_negative_f_ctd_is_given(self) -> None:
        """Test if NegativeValueError is raised when a negative value is given for f_ctd."""
        # Example values
        eta_1 = 1  # -
        eta_2 = 1  # −
        f_ctd = -20  # MPa

        with pytest.raises(NegativeValueError):
            Form8Dot2UltimateBondStress(eta_1=eta_1, eta_2=eta_2, f_ctd=f_ctd)

    def test_integration_with_sub_formula_8_2_coefficient_quality_of_bond(self) -> None:
        """Test the integration with sub-formula 8.2 for the coefficient for quality of bond η1."""
        # Example values
        eta_1 = SubForm8Dot2CoefficientQualityOfBond(bond_quality="good")
        eta_2 = 1  # −
        f_ctd = 20  # MPa

        # Object to test
        form_8_2 = Form8Dot2UltimateBondStress(eta_1=eta_1, eta_2=eta_2, f_ctd=f_ctd)

        # Expected result, manually calculated
        manually_calculated_result = 45

        assert form_8_2 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_integration_with_sub_formula_8_2_coefficient_bar_diameter(self) -> None:
        """Test the integration with sub-formula 8.2 for the coefficient for bar diameter η2."""
        # Example values
        eta_1 = 1  # −
        eta_2 = SubForm8Dot2CoefficientBarDiameter(16)
        f_ctd = 20  # MPa

        # Object to test
        form_8_2 = Form8Dot2UltimateBondStress(eta_1=eta_1, eta_2=eta_2, f_ctd=f_ctd)

        # Expected result, manually calculated
        manually_calculated_result = 45

        assert form_8_2 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            (
                "complete",
                r"f_{bd} = 2.25 \cdot \eta_1 \cdot \eta_2 \cdot f_{ctd} = 2.25 \cdot 1.00 \cdot 1.00 \cdot 20.00 = 45.00",
            ),
            ("short", "f_{bd} = 45.00"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the LaTeX representation."""
        eta_1 = 1  # -
        eta_2 = 1  # −
        f_ctd = 20  # MPa

        latex = Form8Dot2UltimateBondStress(eta_1=eta_1, eta_2=eta_2, f_ctd=f_ctd).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."

"""Testing formula 2.2 from EN 1993-1-1:2005: Chapter 2: Basis of design."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_2_basic_of_design.formula_2_2 import Form2Dot2CharacteristicValueResistance
from blueprints.validations import NegativeValueError


class TestForm2Dot2CharacteristicValueResistance:
    """Validation for formula 2.2 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        r_d = 100  # kN
        gamma_mi = 1.1  # [-]

        form_2_2 = Form2Dot2CharacteristicValueResistance(r_d=r_d, gamma_mi=gamma_mi)
        # manually calculated result
        manually_calculated_result = 110

        assert form_2_2 == pytest.approx(expected=manually_calculated_result, rel=1e-9)

    def test_raise_error_if_negative_r_d(self) -> None:
        """Test that a NegativeValueError is raised when a negative value is passed for r_d."""
        r_d = -1
        gamma_mi = 1.1
        with pytest.raises(NegativeValueError):
            Form2Dot2CharacteristicValueResistance(r_d=r_d, gamma_mi=gamma_mi)

    def test_raise_error_if_negative_gamma_mi(self) -> None:
        """Test that a NegativeValueError is raised when a negative value is passed for gamma_mi."""
        r_d = 100
        gamma_mi = -1.1
        with pytest.raises(NegativeValueError):
            Form2Dot2CharacteristicValueResistance(r_d=r_d, gamma_mi=gamma_mi)

    def test_latex_complete(self) -> None:
        """Tests the latex representation of the formula."""
        r_d = 100
        gamma_mi = 1.1
        form_2_2 = Form2Dot2CharacteristicValueResistance(r_d=r_d, gamma_mi=gamma_mi)
        assert form_2_2.latex().complete == r"R_{k} = R_d \cdot \gamma_{Mi} = 100.00 \cdot 1.10 = 110.00"

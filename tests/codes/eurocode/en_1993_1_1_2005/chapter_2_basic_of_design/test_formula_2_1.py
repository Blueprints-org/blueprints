"""Testing formula 2.1 from EN 1993-1-1:2005: Chapter 2: Basis of design."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_2_basic_of_design.formula_2_1 import Form2Dot1DesignValueResistance
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm2Dot1DesignValueResistance:
    """Validation for formula 2.1 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        r_k = 110  # kN
        gamma_m = 1.1  # [-]

        form_2_1 = Form2Dot1DesignValueResistance(r_k=r_k, gamma_m=gamma_m)
        manually_calculated_result = 100

        assert form_2_1 == pytest.approx(expected=manually_calculated_result, rel=1e-9)

    def test_raise_error_if_negative_r_k(self) -> None:
        """Test that a NegativeValueError is raised when a negative value is passed for r_k."""
        r_k = -110  # kN
        gamma_m = 1.1  # [-]

        with pytest.raises(NegativeValueError):
            Form2Dot1DesignValueResistance(r_k=r_k, gamma_m=gamma_m)

    def test_raise_error_if_negative_gamma_m(self) -> None:
        """Test that a LessOrEqualToZeroError is raised when a negative value is passed for gamma_m."""
        r_k = 110  # kN
        gamma_m = -1.1  # [-]

        with pytest.raises(LessOrEqualToZeroError):
            Form2Dot1DesignValueResistance(r_k=r_k, gamma_m=gamma_m)

    def test_raise_error_if_zero_gamma_m(self) -> None:
        """Test that a LessOrEqualToZeroError is raised when a zero value is passed for gamma_m."""
        r_k = 110  # kN
        gamma_m = 0  # [-]

        with pytest.raises(LessOrEqualToZeroError):
            Form2Dot1DesignValueResistance(r_k=r_k, gamma_m=gamma_m)

    def test_latex_complete(self) -> None:
        """Tests the latex representation of the formula."""
        r_k = 110
        gamma_m = 1.1
        form_2_1 = Form2Dot1DesignValueResistance(r_k=r_k, gamma_m=gamma_m)
        assert form_2_1.latex().complete == r"R_{d} = \frac{R_k}{\gamma_M} = \frac{110.00}{1.10} = 100.00"

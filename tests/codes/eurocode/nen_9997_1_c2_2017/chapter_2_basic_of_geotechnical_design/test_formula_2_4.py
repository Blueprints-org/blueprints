"""Testing Formula 2.4 from NEN 9997-1+C2:2017: Chapter 2: Basis of geotechnical design."""

import pytest

from blueprints.codes.eurocode.nen_9997_1_c2_2017.chapter_2_basic_of_geotechnical_design.formula_2_4 import Form2Dot4DesignValueGeotechnicalParameter
from blueprints.validations import NegativeValueError


class TestForm2Dot4DesignValueGeotechnicalParameter:
    """Validation for formula 2.4 from NEN 9997-1+C2:2017."""

    def test_evaluation_lower_than(self) -> None:
        """Test the evaluation of the result."""
        assert Form2Dot4DesignValueGeotechnicalParameter(e_dst_d=0.2, e_stb_d=0.3, t_d=-0.1) == pytest.approx(1.0)

    def test_evaluation_equals(self) -> None:
        """Test the evaluation of the result."""
        assert Form2Dot4DesignValueGeotechnicalParameter(e_dst_d=1, e_stb_d=0.5, t_d=0.5) == pytest.approx(1.0)

    def test_evaluation_greater_than(self) -> None:
        """Test the evaluation of the result."""
        assert Form2Dot4DesignValueGeotechnicalParameter(e_dst_d=2.01, e_stb_d=1, t_d=1) == pytest.approx(0.0)

    def test_raise_error_if_negative_e_dst_d(self) -> None:
        """Test that a NegativeValueError is raised when a negative value is passed for E_dst;d."""
        with pytest.raises(NegativeValueError):
            Form2Dot4DesignValueGeotechnicalParameter(e_dst_d=-1, e_stb_d=1, t_d=1)

    def test_raise_error_if_negative_e_stb_d(self) -> None:
        """Test that a NegativeValueError is raised when a negative value is passed for E_stb;d."""
        with pytest.raises(NegativeValueError):
            Form2Dot4DesignValueGeotechnicalParameter(e_dst_d=1, e_stb_d=-1, t_d=1)

# TODO: latex gedeelte, wanneer latex zelf ook gefixt is
    # @pytest.mark.parametrize(
    #     ("representation", "expected_result"),
    #     [
    #         ("complete", r"X_d = \frac{X_{k}}{\gamma_M} = \frac{25.000}{1.450} = 17.241"),
    #         ("short", r"X_d = 17.241"),
    #     ],
    # )
    # def test_latex(self, representation: str, expected_result: str) -> None:
    #     """Test the latex representation of the formula."""
    #     # Object to test
    #     latex = Form2Dot2DesignValueGeotechnicalParameter(x_k=25.0, gamma_m=1.45).latex()

    #     actual = {
    #         "complete": latex.complete,
    #         "short": latex.short,
    #     }

    #     assert actual[representation] == expected_result, f"{representation} representation failed."

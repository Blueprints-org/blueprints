"""Testing Formula 2.4 from NEN 9997-1+C2:2017: Chapter 2: Basis of geotechnical design."""

import pytest

from blueprints.codes.eurocode.nen_9997_1_c2_2017.chapter_2_basic_of_geotechnical_design.formula_2_4 import Form2Dot4DesignValueGeotechnicalParameter
from blueprints.validations import NegativeValueError


class TestForm2Dot4DesignValueGeotechnicalParameter:
    """Validation for formula 2.4 from NEN 9997-1+C2:2017."""

    def test_evaluation_lower_than(self) -> None:
        """Test the evaluation of the result."""
        assert Form2Dot4DesignValueGeotechnicalParameter(e_dst_d=0.2, e_stb_d=0.31, t_d=-0.1)

    def test_evaluation_equals(self) -> None:
        """Test the evaluation of the result."""
        assert Form2Dot4DesignValueGeotechnicalParameter(e_dst_d=0.2, e_stb_d=0.3, t_d=-0.1)

    def test_evaluation_greater_than(self) -> None:
        """Test the evaluation of the result."""
        assert not Form2Dot4DesignValueGeotechnicalParameter(e_dst_d=2.01, e_stb_d=1, t_d=1)

    def test_raise_error_if_negative_e_dst_d(self) -> None:
        """Test that a NegativeValueError is raised when a negative value is passed for E_dst;d."""
        with pytest.raises(NegativeValueError):
            bool(Form2Dot4DesignValueGeotechnicalParameter(e_dst_d=-1, e_stb_d=1, t_d=1))

    def test_raise_error_if_negative_e_stb_d(self) -> None:
        """Test that a NegativeValueError is raised when a negative value is passed for E_stb;d."""
        with pytest.raises(NegativeValueError):
            bool(Form2Dot4DesignValueGeotechnicalParameter(e_dst_d=1, e_stb_d=-1, t_d=1))

    def test_str(self) -> None:
        """Test the string representation of the formula."""
        assert isinstance(str(Form2Dot4DesignValueGeotechnicalParameter(e_dst_d=2.01, e_stb_d=1, t_d=1)), str)

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            ("complete", r"CHECK \to E_{dst;d} \leq E_{stb;d} + T_d \to 2.01 \leq 1.00 + 1.00 \to 2.01 \leq 2.00 \to \text{Not OK}"),
            ("short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = Form2Dot4DesignValueGeotechnicalParameter(e_dst_d=2.01, e_stb_d=1, t_d=1).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."

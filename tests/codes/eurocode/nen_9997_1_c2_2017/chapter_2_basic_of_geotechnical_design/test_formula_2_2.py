"""Testing Formula 2.2 from NEN 9997-1+C2:2017: Chapter 2: Basis of geotechnical design."""

import pytest

from blueprints.codes.eurocode.nen_9997_1_c2_2017.chapter_2_basic_of_geotechnical_design.formula_2_2 import Form2Dot2DesignValueGeotechnicalParameter
from blueprints.validations import LessOrEqualToZeroError


class TestForm2Dot2DesignValueGeotechnicalParameter:
    """Validation for formula 2.2 from NEN 9997-1+C2:2017."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        assert Form2Dot2DesignValueGeotechnicalParameter(x_k=25.0, gamma_m=1.45) == pytest.approx(expected=17.241, abs=0.001)

    def test_raise_error_if_negative_or_zero_gamma(self) -> None:
        """Test that a LessOrEqualToZeroError is raised when a negative or zero value is passed for gamma_m."""
        with pytest.raises(LessOrEqualToZeroError):
            Form2Dot2DesignValueGeotechnicalParameter(x_k=25.0, gamma_m=-1.0)

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            ("complete", r"X_d = \frac{X_{k}}{\gamma_M} = \frac{25.000}{1.450} = 17.241"),
            ("short", r"X_d = 17.241"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = Form2Dot2DesignValueGeotechnicalParameter(x_k=25.0, gamma_m=1.45).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."

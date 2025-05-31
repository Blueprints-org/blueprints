"""Testing sub-formula for 3.2 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_2 import SubForm3Dot2CoefficientTypeOfCementS


class TestSubForm3Dot2CoefficientTypeOfCementS:
    """Validation for formula 3.2 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example value 1
        cement_class = "R"  # str
        sub_form_3_2 = SubForm3Dot2CoefficientTypeOfCementS(cement_class=cement_class)
        # Expected result, manually calculated
        manually_result = 0.20
        assert sub_form_3_2 == pytest.approx(expected=manually_result, rel=1e-4)

        # Example value 2
        cement_class = "N"  # str
        sub_form_3_2 = SubForm3Dot2CoefficientTypeOfCementS(cement_class=cement_class)
        # Expected result, manually calculated
        manually_result = 0.25
        assert sub_form_3_2 == pytest.approx(expected=manually_result, rel=1e-4)

        # Example value 3
        cement_class = "S"  # str
        sub_form_3_2 = SubForm3Dot2CoefficientTypeOfCementS(cement_class=cement_class)
        # Expected result, manually calculated
        manually_result = 0.38
        assert sub_form_3_2 == pytest.approx(expected=manually_result, rel=1e-4)

    def test_raise_error_when_invalid_cement_class_is_given(self) -> None:
        """Test an invalid cement class."""
        # Example values
        cement_class = "V"  # str

        with pytest.raises(ValueError):
            SubForm3Dot2CoefficientTypeOfCementS(cement_class=cement_class)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"s \rightarrow \text{cement class} \rightarrow R \rightarrow 0.200",
            ),
            ("short", r"s \rightarrow 0.200"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        cement_class = "R"

        # Object to test
        form_7_3_latex = SubForm3Dot2CoefficientTypeOfCementS(cement_class=cement_class).latex()

        actual = {"complete": form_7_3_latex.complete, "short": form_7_3_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

"""Testing sub-formula for 3.4 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_4 import SubForm3Dot4CoefficientAgeConcreteAlpha


class TestSubForm3Dot4CoefficientAgeConcreteAlpha:
    """Validation for sub-formula 3.4 from EN 1992-1-1:2004."""

    def test_t_between_0_and_28(self) -> None:
        """Test the evaluation of the result."""
        # Example value 1
        t = 10  # days

        sub_form_3_4 = SubForm3Dot4CoefficientAgeConcreteAlpha(t=t)

        # Expected result, manually calculated
        manually_result = 1.0

        assert sub_form_3_4 == pytest.approx(expected=manually_result, rel=1e-4)

    def test_raise_error_when_t_lower_or_equal_to_0(self) -> None:
        """Test the evaluation of the result."""
        # Example value 1
        t = 0  # days

        with pytest.raises(ValueError):
            SubForm3Dot4CoefficientAgeConcreteAlpha(t=t)

    def test_t_higher_then_28(self) -> None:
        """Test the evaluation of the result."""
        # Example value 1
        t = 50  # days

        sub_form_3_4 = SubForm3Dot4CoefficientAgeConcreteAlpha(t=t)

        # Expected result, manually calculated
        manually_result = 2 / 3

        assert sub_form_3_4 == pytest.approx(expected=manually_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\alpha \rightarrow t \rightarrow 10.000 \rightarrow 1.000",
            ),
            ("short", r"\alpha \rightarrow 1.000"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        t = 10  # days

        # Object to test
        form_3_4_latex = SubForm3Dot4CoefficientAgeConcreteAlpha(t=t).latex()

        actual = {"complete": form_3_4_latex.complete, "short": form_3_4_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

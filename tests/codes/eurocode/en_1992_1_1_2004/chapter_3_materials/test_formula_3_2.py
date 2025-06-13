"""Testing formula 3.2 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_2 import Form3Dot2CoefficientDependentOfConcreteAge


class TestForm3Dot2CoefficientDependentOfConcreteAge:
    """Validation for formula 3.2 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        s = 0.25  # -
        t = 10  # days
        form_3_2 = Form3Dot2CoefficientDependentOfConcreteAge(s=s, t=t)

        # Expected result, manually calculated
        manually_calculated_result = 0.84507490

        assert form_3_2 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_t_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        s = 0.25  # -
        t = -10  # days

        with pytest.raises(ValueError):
            Form3Dot2CoefficientDependentOfConcreteAge(s=s, t=t)

    def test_raise_error_when_negative_s_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        s = -0.9  # -
        t = 10  # days

        with pytest.raises(ValueError):
            Form3Dot2CoefficientDependentOfConcreteAge(s=s, t=t)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\beta_{cc}(t) = \exp \left( s \cdot \left( 1 - \left( \frac{28}{t} \right) ^{1/2} \right) \right) = "
                r"\exp \left( 0.250 \cdot \left( 1 - \left( \frac{28}{10.000} \right) ^{1/2} \right) \right) = 0.845",
            ),
            ("short", r"\beta_{cc}(t) = 0.845"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        s = 0.25  # -
        t = 10  # days

        # Object to test
        form_3_2_latex = Form3Dot2CoefficientDependentOfConcreteAge(s=s, t=t).latex()

        actual = {"complete": form_3_2_latex.complete, "short": form_3_2_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

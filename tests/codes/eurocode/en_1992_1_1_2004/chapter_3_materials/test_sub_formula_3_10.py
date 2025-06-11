"""Testing sub-formula for 3.10 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_10 import SubForm3Dot10FictionalCrossSection


class TestSubForm3Dot10FictionalCrossSection:
    """Validation for sub-formula for 3.10 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        a_c = 42.5  # mm²
        u = 20.3  # mm
        sub_form_3_10 = SubForm3Dot10FictionalCrossSection(a_c=a_c, u=u)

        # Expected result, manually calculated
        manually_calculated_result = 4.187192

        assert sub_form_3_10 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_a_c_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        a_c = -42.5  # mm²
        u = 20.3  # mm

        with pytest.raises(ValueError):
            SubForm3Dot10FictionalCrossSection(a_c=a_c, u=u)

    def test_raise_error_when_negative_u_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        a_c = 42.5  # mm²
        u = -20.3  # mm

        with pytest.raises(ValueError):
            SubForm3Dot10FictionalCrossSection(a_c=a_c, u=u)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"h_0 = 2 \cdot A_c / u = 2 \cdot 42.50 / 20.30 = 4.19",
            ),
            ("short", r"h_0 = 4.19"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_c = 42.5  # mm²
        u = 20.3  # mm

        # Object to test
        form_3_10_sub_latex = SubForm3Dot10FictionalCrossSection(a_c=a_c, u=u).latex()

        actual = {"complete": form_3_10_sub_latex.complete, "short": form_3_10_sub_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

"""Testing formula 3.8 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_8 import Form3Dot8TotalShrinkage


class TestForm3Dot8TotalShrinkage:
    """Validation for formula 3.8 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        epsilon_cd = 0.25  # -
        epsilon_ca = 0.33  # -
        form_3_8 = Form3Dot8TotalShrinkage(epsilon_cd=epsilon_cd, epsilon_ca=epsilon_ca)

        # Expected result, manually calculated
        manually_calculated_result = 0.58

        assert form_3_8 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_2(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        epsilon_cd = -0.25  # -
        epsilon_ca = 0.33  # -
        form_3_8 = Form3Dot8TotalShrinkage(epsilon_cd=epsilon_cd, epsilon_ca=epsilon_ca)

        # Expected result, manually calculated
        manually_calculated_result = 0.08

        assert form_3_8 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\epsilon_{cs} = \epsilon_{cd} + \epsilon_{ca} = 0.250 + 0.330 = 0.580",
            ),
            ("short", r"\epsilon_{cs} = 0.580"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        epsilon_cd = 0.25  # -
        epsilon_ca = 0.33  # -

        # Object to test
        form_3_8_latex = Form3Dot8TotalShrinkage(epsilon_cd=epsilon_cd, epsilon_ca=epsilon_ca).latex()

        actual = {"complete": form_3_8_latex.complete, "short": form_3_8_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

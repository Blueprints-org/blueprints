"""Testing sub-formula 1 of 3.14 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_14 import SubForm3Dot14Eta


class TestSub1Form3Dot14Eta:
    """Validation for sub-formula 1 of 3.14 from EN 1992-1-1:2004."""

    def test_evaluation_1(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        epsilon_c = 0.16  # -
        epsilon_c1 = 0.43  # -

        sub_1_form_3_14 = SubForm3Dot14Eta(epsilon_c=epsilon_c, epsilon_c1=epsilon_c1)

        # Expected result, manually calculated
        manually_calculated_result = 0.37209

        assert sub_1_form_3_14 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_2(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        epsilon_c = 0.3  # -
        epsilon_c1 = 0.2  # -

        sub_1_form_3_14 = SubForm3Dot14Eta(epsilon_c=epsilon_c, epsilon_c1=epsilon_c1)

        # Expected result, manually calculated
        manually_calculated_result = 1.5

        assert sub_1_form_3_14 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\eta = \epsilon_c / \epsilon_{c1} = 0.160 / 0.430 = 0.372",
            ),
            ("short", r"\eta = 0.372"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        epsilon_c = 0.16  # -
        epsilon_c1 = 0.43  # -

        # Object to test
        form_3_14sub1_latex = SubForm3Dot14Eta(epsilon_c=epsilon_c, epsilon_c1=epsilon_c1).latex()

        actual = {"complete": form_3_14sub1_latex.complete, "short": form_3_14sub1_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

"""Testing formula 3.14 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_14 import Form3Dot14StressStrainForShortTermLoading


class TestForm3Dot14StressStrainForShortTermLoading:
    """Validation for formula 3.14 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        k = 0.38  # -
        eta = 0.88  # -

        form_3_14 = Form3Dot14StressStrainForShortTermLoading(k=k, eta=eta)

        # Expected result, manually calculated
        manually_calculated_result = 1.03383

        assert form_3_14 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_k_is_given(self) -> None:
        """Test formula raising error by a negative value."""
        # Example values
        k = -0.38  # -
        eta = 0.88  # -

        with pytest.raises(ValueError):
            Form3Dot14StressStrainForShortTermLoading(k=k, eta=eta)

    def test_raise_error_when_negative_eta_is_given(self) -> None:
        """Test formula raising error by a negative value."""
        # Example values
        k = 0.38  # -
        eta = -0.88  # -

        with pytest.raises(ValueError):
            Form3Dot14StressStrainForShortTermLoading(k=k, eta=eta)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\frac{\sigma_c}{f_{cm}} = \frac{k \cdot \eta - \eta^2}{1 + (k-2) \cdot \eta} = "
                r"\frac{0.380 \cdot 0.880 - 0.880^2}{1 + (0.380-2) \cdot 0.880} = 1.034",
            ),
            ("short", r"\frac{\sigma_c}{f_{cm}} = 1.034"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        k = 0.38  # -
        eta = 0.88

        # Object to test
        form_3_14_latex = Form3Dot14StressStrainForShortTermLoading(k=k, eta=eta).latex()

        actual = {"complete": form_3_14_latex.complete, "short": form_3_14_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

"""Testing formula 3.11 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_11 import Form3Dot11AutogeneShrinkage


class TestForm3Dot11AutogeneShrinkage:
    """Validation for formula 3.11 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        beta_as_t = 0.25  # -
        epsilon_ca_inf = 0.056  # -
        form_3_11 = Form3Dot11AutogeneShrinkage(beta_as_t=beta_as_t, epsilon_ca_inf=epsilon_ca_inf)

        # Expected result, manually calculated
        manually_calculated_result = 0.014

        assert form_3_11 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_beta_as_t_is_given(self) -> None:
        """Test formula raising error by a negative value."""
        # Example values
        beta_as_t = -0.25  # -
        epsilon_ca_inf = 0.056  # -

        with pytest.raises(ValueError):
            Form3Dot11AutogeneShrinkage(beta_as_t=beta_as_t, epsilon_ca_inf=epsilon_ca_inf)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\epsilon_{ca}(t) = \beta_{as}(t) \cdot \epsilon_{ca}(\infty) = 0.250 \cdot 0.056 = 0.014",
            ),
            ("short", r"\epsilon_{ca}(t) = 0.014"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        beta_as_t = 0.25  # -
        epsilon_ca_inf = 0.056  # -

        # Object to test
        form_3_11_latex = Form3Dot11AutogeneShrinkage(beta_as_t=beta_as_t, epsilon_ca_inf=epsilon_ca_inf).latex()

        actual = {"complete": form_3_11_latex.complete, "short": form_3_11_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

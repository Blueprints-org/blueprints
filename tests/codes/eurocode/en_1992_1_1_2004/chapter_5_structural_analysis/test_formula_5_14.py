"""Testing formula 5.14 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_14 import Form5Dot14SlendernessRatio
from blueprints.validations import LessOrEqualToZeroError


class TestForm5Dot14TransverseForceEffectBracingSystem:
    """Validation for formula 5.14 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        l_0 = 4.0  # M
        i = 2.0  # M

        # Object to test
        form_5_14 = Form5Dot14SlendernessRatio(l_0=l_0, i=i)

        # Expected result, manually calculated
        manually_calculated_result = 2.0  # -

        assert form_5_14 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("l_0", "i"),
        [
            (-4, 2),
            (4, -2),
        ],
    )
    def test_raise_error_when_negative_theta_i_is_given(
        self,
        l_0: float,
        i: float,
    ) -> None:
        """Test negative values for theta_i, n_a and n_b."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot14SlendernessRatio(l_0=l_0, i=i)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"λ = \frac{l_0}{i} = \frac{4.000}{2.000} = 2.000",
            ),
            ("short", r"λ = 2.000"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        l_0 = 4.0  # M
        i = 2.0  # M

        # Object to test
        form_5_14_latex = Form5Dot14SlendernessRatio(
            l_0=l_0,
            i=i,
        ).latex()

        actual = {
            "complete": form_5_14_latex.complete,
            "short": form_5_14_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."

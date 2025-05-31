"""Testing sub-formula 8.16 (α1) of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_16 import (
    SubForm8Dot16Alpha1,
)


class TestSubForm8Dot16Alpha1:
    """Validation for sub-formula 8.16 (α1) from EN 1992-1-1:2004."""

    def test_evaluation_gradual(self) -> None:
        """Test the evaluation of the result when release_type is gradual."""
        # example values
        release_type = "gradual"

        sub_form_8_16_alpha_1 = SubForm8Dot16Alpha1(release_type=release_type)

        # manually calculated result
        manually_calculated_result = 1  # [-]

        assert sub_form_8_16_alpha_1 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_sudden(self) -> None:
        """Test the evaluation of the result when release_type is sudden."""
        # example values
        release_type = "sudden"

        sub_form_8_16_alpha_1 = SubForm8Dot16Alpha1(release_type=release_type)

        # manually calculated result
        manually_calculated_result = 1.25

        assert sub_form_8_16_alpha_1 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_if_invalid_release_type(self) -> None:
        """Test that a ValueError is raised when an invalid value is passed for release_type."""
        release_type = "invalid"

        with pytest.raises(ValueError):
            SubForm8Dot16Alpha1(release_type=release_type)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (r"\alpha_1 \rightarrow release\;type \rightarrow gradual \rightarrow 1.00"),
            ),
            ("short", r"\alpha_1 \rightarrow 1.00"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # example values
        release_type = "gradual"

        # Object to test
        form_8_16_p1_latex = SubForm8Dot16Alpha1(release_type=release_type).latex()

        actual = {"complete": form_8_16_p1_latex.complete, "short": form_8_16_p1_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

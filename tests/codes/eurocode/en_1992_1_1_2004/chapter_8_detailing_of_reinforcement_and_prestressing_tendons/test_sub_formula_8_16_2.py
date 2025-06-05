"""Testing sub-formula 8.16 (α2) of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_16 import (
    SubForm8Dot16Alpha2,
)


class TestSubForm8Dot16Alpha2:
    """Validation for sub-formula 8.16 (α2) from EN 1992-1-1:2004."""

    def test_evaluation_circular(self) -> None:
        """Test the evaluation of the result when type_of_wire is circular."""
        # example values
        type_of_wire = "circular"

        sub_form_8_16_alpha_2 = SubForm8Dot16Alpha2(type_of_wire=type_of_wire)

        # manually calculated result
        manually_calculated_result = 0.25  # [-]

        assert sub_form_8_16_alpha_2 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_3_7_wire_strand(self) -> None:
        """Test the evaluation of the result when type_of_wire is 3_7_wire_strands."""
        # example values
        type_of_wire = "3_7_wire_strands"

        sub_form_8_16_alpha_2 = SubForm8Dot16Alpha2(type_of_wire=type_of_wire)

        # manually calculated result
        manually_calculated_result = 0.19

        assert sub_form_8_16_alpha_2 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_if_invalid_type_of_wire(self) -> None:
        """Test that a ValueError is raised when an invalid value is passed for type_of_wire."""
        type_of_wire = "invalid"

        with pytest.raises(ValueError):
            SubForm8Dot16Alpha2(type_of_wire=type_of_wire)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (r"\alpha_2 \rightarrow type\;of\;wire \rightarrow circular \rightarrow 0.25"),
            ),
            ("short", r"\alpha_2 \rightarrow 0.25"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # example values
        type_of_wire = "circular"

        # Object to test
        form_8_16_p2_latex = SubForm8Dot16Alpha2(type_of_wire=type_of_wire).latex()

        actual = {"complete": form_8_16_p2_latex.complete, "short": form_8_16_p2_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

"""Testing sub-formula 1 from 8.15 from EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_15 import (
    SubForm8Dot15EtaP1,
)


class TestSubForm8Dot15EtaP1:
    """Validation for sub-formula 1 from 8.15 from EN 1992-1-1:2004."""

    @pytest.mark.parametrize(
        ("type_of_wire", "expected"),
        [
            ("indented", 2.7),
            ("3_7_wire_strands", 3.2),
        ],
    )
    def test_evaluation(self, type_of_wire: str, expected: float) -> None:
        """Test the evaluation of the result."""
        # example values
        sub_form_8_15 = SubForm8Dot15EtaP1(
            type_of_wire=type_of_wire,
        )
        assert sub_form_8_15 == pytest.approx(expected=expected, rel=1e-4)

    def test_invalid_type_of_wire(self) -> None:
        """Test the evaluation of the result."""
        # example values
        type_of_wire = "invalid"
        with pytest.raises(ValueError):
            SubForm8Dot15EtaP1(
                type_of_wire=type_of_wire,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (r"\eta_{p1} \rightarrow type\;of\;wire \rightarrow indented \rightarrow 2.70"),
            ),
            ("short", r"\eta_{p1} \rightarrow 2.70"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # example values
        type_of_wire = "indented"

        # Object to test
        form_8_15_p1_latex = SubForm8Dot15EtaP1(type_of_wire=type_of_wire).latex()

        actual = {"complete": form_8_15_p1_latex.complete, "short": form_8_15_p1_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

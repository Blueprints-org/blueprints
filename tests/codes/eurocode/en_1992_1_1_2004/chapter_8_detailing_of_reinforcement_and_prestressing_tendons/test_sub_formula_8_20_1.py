"""Testing sub-formula for 8.20 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_20 import (
    SubForm8Dot20EtaP2,
)

class TestSubForm8Dot20EtaP2:
    """Validation for sub-formula 8.20 from EN 1992-1-1:2004."""


    def test_evaluation_indented(self) -> None:
        """Test the evaluation of the result when type_of_wire is indented."""
        # example values
        type_of_wire = "indented"

        sub_form_8_20_etaP2 = SubForm8Dot20EtaP2(type_of_wire=type_of_wire)

        # manually calculated result
        manually_calculated_result = 1.4  # [-]

        assert sub_form_8_20_etaP2 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_7_wire_strand(self) -> None:
        """Test the evaluation of the result when type_of_wire is 7_wire_strands."""
        # example values
        type_of_wire = "7_wire_strands"

        sub_form_8_20_etaP2 = SubForm8Dot20EtaP2(type_of_wire=type_of_wire)

        # manually calculated result
        manually_calculated_result = 1.2

        assert sub_form_8_20_etaP2 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_if_invalid_type_of_wire(self) -> None:
        """Test that a ValueError is raised when an invalid value is passed for type_of_wire."""
        type_of_wire = "invalid"

        with pytest.raises(ValueError):
            SubForm8Dot20EtaP2(type_of_wire=type_of_wire)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (r"\eta_{p2} \rightarrow type\;of\;wire \rightarrow indented \rightarrow 1.40"),
            ),
            (
                "complete_with_units",
                (r"\eta_{p2} \rightarrow type\;of\;wire \rightarrow indented \rightarrow 1.40"),
            ),
            ("short", r"\eta_{p2} \rightarrow 1.40"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # example values
        type_of_wire = "indented"

        # Object to test
        form_8_20_etaP2_latex = SubForm8Dot20EtaP2(type_of_wire=type_of_wire).latex()

        actual = {
            "complete": form_8_20_etaP2_latex.complete,
            "complete_with_units": form_8_20_etaP2_latex.complete_with_units,
            "short": form_8_20_etaP2_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."

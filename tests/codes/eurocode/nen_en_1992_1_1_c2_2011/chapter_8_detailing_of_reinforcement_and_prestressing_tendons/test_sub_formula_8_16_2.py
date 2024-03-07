"""Testing sub-formula 8.16 (α2) of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_16 import (
    SubForm8Dot16Alpha2,
)


class TestSubForm8Dot16Alpha2:
    """Validation for sub-formula 8.16 (α2) from NEN-EN 1992-1-1+C2:2011."""

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

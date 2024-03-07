"""Testing sub-formula 1 from 8.15 from NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_15 import (
    SubForm8Dot15EtaP1,
)


class TestSubForm8Dot15EtaP1:
    """Validation for sub-formula 1 from 8.15 from NEN-EN 1992-1-1+C2:2011."""

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

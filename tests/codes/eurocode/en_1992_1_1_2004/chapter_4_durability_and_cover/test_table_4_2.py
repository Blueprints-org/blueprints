"""Testing table 4.2 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover.table_4_2 import Table4Dot2MinimumCoverWithRegardToBond
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_14 import (
    Form8Dot14EquivalentDiameterBundledBars,
)
from blueprints.type_alias import MM
from blueprints.validations import LessOrEqualToZeroError


class TestTable4Dot2MinimumCoverWithRegardToBond:
    """Validation for table 4.2 from EN 1992-1-1:2004."""

    @pytest.mark.parametrize(
        ("diameter", "nominal_max_aggregate_size_greater_than_32_mm", "expected_result"),
        [
            (25, True, 30),
            (25, False, 25),
        ],
    )
    def test_evaluation(self, diameter: MM, nominal_max_aggregate_size_greater_than_32_mm: bool, expected_result: MM) -> None:
        """Test the evaluation of the result."""
        form_4_2 = Table4Dot2MinimumCoverWithRegardToBond(
            diameter=diameter,
            nominal_max_aggregate_size_greater_than_32_mm=nominal_max_aggregate_size_greater_than_32_mm,
        )

        assert form_4_2 == pytest.approx(expected=expected_result, rel=1e-4)

    def test_evaluation_using_form_8_14(self) -> None:
        """Test the evaluation of the result using formula 8.14 (Form8Dot14EquivalentDiameterBundledBars)."""
        form_4_2 = Table4Dot2MinimumCoverWithRegardToBond(
            diameter=Form8Dot14EquivalentDiameterBundledBars(diameter=20, n_b=4),
            nominal_max_aggregate_size_greater_than_32_mm=True,
        )

        expected_result = 45

        assert form_4_2 == pytest.approx(expected=expected_result, rel=1e-4)

    def test_raise_error_when_negative_diameter_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        diameter = -7
        nominal_max_aggregate_size_greater_than_32_mm = False

        with pytest.raises(LessOrEqualToZeroError):
            Table4Dot2MinimumCoverWithRegardToBond(
                diameter=diameter,
                nominal_max_aggregate_size_greater_than_32_mm=nominal_max_aggregate_size_greater_than_32_mm,
            )

    def test_raise_error_when_invalid_boolean_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        diameter = 20
        nominal_max_aggregate_size_greater_than_32_mm = 1

        with pytest.raises(TypeError) as exc_info:
            Table4Dot2MinimumCoverWithRegardToBond(
                diameter=diameter,
                nominal_max_aggregate_size_greater_than_32_mm=nominal_max_aggregate_size_greater_than_32_mm,  # type: ignore[arg-type]
            )

        assert str(exc_info.value) == "The parameter 'nominal_max_aggregate_size_greater_than_32_mm' must be a boolean."

    @pytest.mark.parametrize(
        ("nominal_max_aggregate_size_greater_than_32_mm", "representation", "expected_result"),
        [
            (True, "complete", r"c_{min,b} = \text{(equivalent) rebar diameter} + 5 = 20 + 5 = 25"),
            (True, "short", "c_{min,b} = 25"),
            (False, "complete", r"c_{min,b} = \text{(equivalent) rebar diameter} = 20 = 20"),
            (False, "short", "c_{min,b} = 20"),
        ],
    )
    def test_latex(self, nominal_max_aggregate_size_greater_than_32_mm: bool, representation: str, expected_result: str) -> None:
        """Test the latex implementation."""
        diameter = 20

        form = Table4Dot2MinimumCoverWithRegardToBond(
            diameter=diameter, nominal_max_aggregate_size_greater_than_32_mm=nominal_max_aggregate_size_greater_than_32_mm
        ).latex()

        actual = {
            "complete": form.complete,
            "short": form.short,
            "string": str(form),
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."

"""Testing formula 4.2 of EN 1993-1-8:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_8_2005.chapter_4_welded_connections.formula_4_2 import Form4Dot2CheckWeldedConnection
from blueprints.validations import NegativeValueError


class TestForm4Dot2CheckWeldedConnection:
    """Validation for formula 4.2 from EN 1993-1-8:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        fw_ed = 50.0
        fw_rd = 100.0

        # Object to test
        formula = Form4Dot2CheckWeldedConnection(fw_ed=fw_ed, fw_rd=fw_rd)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("fw_ed", "fw_rd"),
        [
            (-10.0, 100.0),  # fw_ed is negative
            (50.0, -100.0),  # fw_rd is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, fw_ed: float, fw_rd: float) -> None:
        """Test invalid values where inputs are negative."""
        with pytest.raises(NegativeValueError):
            Form4Dot2CheckWeldedConnection(fw_ed=fw_ed, fw_rd=fw_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to F_{w,Ed} \leq F_{w,Rd} \to 50.000 \leq 100.000 \to OK",
            ),
            (
                "complete_with_units",
                r"CHECK \to F_{w,Ed} \leq F_{w,Rd} \to 50.000 \ N \leq 100.000 \ N \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        fw_ed = 50.0
        fw_rd = 100.0

        # Object to test
        latex = Form4Dot2CheckWeldedConnection(fw_ed=fw_ed, fw_rd=fw_rd).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
            "complete_with_units": latex.complete_with_units,
        }

        assert expected == actual[representation], f"{representation} representation failed."

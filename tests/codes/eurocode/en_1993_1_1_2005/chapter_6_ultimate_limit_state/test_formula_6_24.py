"""Testing formula 6.24 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_24 import Form6Dot24TotalTorsionalMoment
from blueprints.validations import NegativeValueError


class TestForm6Dot24TotalTorsionalMoment:
    """Validation for formula 6.24 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        t_t_ed = 500.0
        t_w_ed = 300.0

        # Object to test
        formula = Form6Dot24TotalTorsionalMoment(t_t_ed=t_t_ed, t_w_ed=t_w_ed)

        # Expected result, manually calculated
        manually_calculated_result = 800.0  # Nmm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("t_t_ed", "t_w_ed"),
        [
            (-500.0, 300.0),  # t_t_ed is negative
            (500.0, -300.0),  # t_w_ed is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, t_t_ed: float, t_w_ed: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form6Dot24TotalTorsionalMoment(t_t_ed=t_t_ed, t_w_ed=t_w_ed)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"T_{Ed} = T_{t,Ed} + T_{w,Ed} = 500.000 + 300.000 = 800.000 \ Nmm",
            ),
            ("short", r"T_{Ed} = 800.000 \ Nmm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        t_t_ed = 500.0
        t_w_ed = 300.0

        # Object to test
        latex = Form6Dot24TotalTorsionalMoment(t_t_ed=t_t_ed, t_w_ed=t_w_ed).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

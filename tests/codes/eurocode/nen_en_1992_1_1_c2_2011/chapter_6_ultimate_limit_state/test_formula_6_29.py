"""Testing formula 6.29 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_29 import Form6Dot29CheckTorsionShearResistance
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot29CheckTorsionShearResistance:
    """Validation for formula 6.29 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        t_ed = 100.0  # Nm
        v_ed = 200.0  # N
        t_rd_max = 150.0  # Nm
        v_rd_max = 250.0  # N

        # Object to test
        formula = Form6Dot29CheckTorsionShearResistance(t_ed=t_ed, v_ed=v_ed, t_rd_max=t_rd_max, v_rd_max=v_rd_max)

        # Expected result, manually calculated
        expected_result = False

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("t_ed", "v_ed", "t_rd_max", "v_rd_max"),
        [
            (-100.0, 200.0, 150.0, 250.0),  # t_ed is negative
            (100.0, -200.0, 150.0, 250.0),  # v_ed is negative
            (100.0, 200.0, -150.0, 250.0),  # t_rd_max is negative
            (100.0, 200.0, 150.0, -250.0),  # v_rd_max is negative
            (100.0, 200.0, 0.0, 250.0),  # t_rd_max is zero
            (100.0, 200.0, 150.0, 0.0),  # v_rd_max is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, t_ed: float, v_ed: float, t_rd_max: float, v_rd_max: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot29CheckTorsionShearResistance(t_ed=t_ed, v_ed=v_ed, t_rd_max=t_rd_max, v_rd_max=v_rd_max)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \left( \frac{T_{Ed}}{T_{Rd,max}} + \frac{V_{Ed}}{V_{Rd,max}} \leq 1 \right) \to "
                r"\left( \frac{100.000}{150.000} + \frac{200.000}{250.000} \leq 1 \right) \to \text{Not OK}",
            ),
            ("short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        t_ed = 100.0  # Nm
        v_ed = 200.0  # N
        t_rd_max = 150.0  # Nm
        v_rd_max = 250.0  # N

        # Object to test
        latex = Form6Dot29CheckTorsionShearResistance(t_ed=t_ed, v_ed=v_ed, t_rd_max=t_rd_max, v_rd_max=v_rd_max).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

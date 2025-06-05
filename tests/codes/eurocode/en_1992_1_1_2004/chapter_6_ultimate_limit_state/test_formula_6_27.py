"""Testing formula 6.27 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_27 import Form6Dot27ShearForceInWall
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot27ShearForceInWall:
    """Validation for formula 6.27 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        tau_t_i_t_ef_i = 100.0
        z_i = 2.0

        # Object to test
        formula = Form6Dot27ShearForceInWall(tau_t_i_t_ef_i=tau_t_i_t_ef_i, z_i=z_i)

        # Expected result, manually calculated
        manually_calculated_result = 200.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("tau_t_i_t_ef_i", "z_i"),
        [
            (-100.0, 2.0),  # tau_t_i_t_ef_i is negative
            (100.0, -2.0),  # z_i is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, tau_t_i_t_ef_i: float, z_i: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot27ShearForceInWall(tau_t_i_t_ef_i=tau_t_i_t_ef_i, z_i=z_i)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"V_{Ed,i} = \tau_{t,i} t_{ef,i} \cdot z_{i} = 100.000 \cdot 2.000 = 200.000 \ N",
            ),
            ("short", r"V_{Ed,i} = 200.000 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        tau_t_i_t_ef_i = 100.0
        z_i = 2.0

        # Object to test
        latex = Form6Dot27ShearForceInWall(tau_t_i_t_ef_i=tau_t_i_t_ef_i, z_i=z_i).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

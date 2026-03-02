"""Testing formula 8.16 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2025.chapter_8_ultimate_limit_state.formula_8_16 import Form8Dot16NetDesignTensionResistance
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot16NetDesignTensionResistance:
    """Validation for formula 8.16 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_net = 5000.0  # mm^2
        f_y = 355.0  # MPa
        gamma_m0 = 1.0

        # Object to test
        formula = Form8Dot16NetDesignTensionResistance(a_net=a_net, f_y=f_y, gamma_m0=gamma_m0)

        # Expected result, manually calculated
        manually_calculated_result = 1775000.0  # N

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_net", "f_y", "gamma_m0"),
        [
            (-5000.0, 355.0, 1.0),  # a_net is negative
            (5000.0, -355.0, 1.0),  # f_y is negative
            (5000.0, 355.0, -1.0),  # gamma_m0 is negative
            (5000.0, 355.0, 0.0),  # gamma_m0 is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_net: float, f_y: float, gamma_m0: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot16NetDesignTensionResistance(a_net=a_net, f_y=f_y, gamma_m0=gamma_m0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"N_{net,Rd} = \frac{A_{net} \cdot f_y}{\gamma_{M0}} = "
                r"\frac{5000.000 \cdot 355.000}{1.000} = 1775000.000 \ N",
            ),
            ("short", r"N_{net,Rd} = 1775000.000 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_net = 5000.0  # mm^2
        f_y = 355.0  # MPa
        gamma_m0 = 1.0

        # Object to test
        latex = Form8Dot16NetDesignTensionResistance(a_net=a_net, f_y=f_y, gamma_m0=gamma_m0).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

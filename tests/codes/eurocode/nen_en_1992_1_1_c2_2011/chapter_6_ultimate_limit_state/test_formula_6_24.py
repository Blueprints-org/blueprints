"""Testing formula 6.24 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_24 import Form6Dot24DesignShearStress
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot24DesignShearStress:
    """Validation for formula 6.24 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        beta = 0.8
        v_ed = 100000.0
        z = 300.0
        b_i = 200.0

        # Object to test
        formula = Form6Dot24DesignShearStress(beta=beta, v_ed=v_ed, z=z, b_i=b_i)

        # Expected result, manually calculated
        manually_calculated_result = 4.0 / 3.0  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("beta", "v_ed", "z", "b_i"),
        [
            (-0.8, 100000.0, 300.0, 200.0),  # beta is negative
            (0.8, -100000.0, 300.0, 200.0),  # v_ed is negative
            (0.8, 100000.0, -300.0, 200.0),  # z is negative
            (0.8, 100000.0, 300.0, -200.0),  # b_i is negative
            (0.8, 100000.0, 0.0, 200.0),  # z is zero
            (0.8, 100000.0, 300.0, 0.0),  # b_i is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, beta: float, v_ed: float, z: float, b_i: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot24DesignShearStress(beta=beta, v_ed=v_ed, z=z, b_i=b_i)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"v_{Edi} = \beta \cdot \frac{V_{Ed}}{z \cdot b_{i}} = 0.800 \cdot \frac{100000.000}{300.000 \cdot 200.000} = 1.333 \ MPa",
            ),
            ("short", r"v_{Edi} = 1.333 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        beta = 0.8
        v_ed = 100000.0
        z = 300.0
        b_i = 200.0

        # Object to test
        latex = Form6Dot24DesignShearStress(beta=beta, v_ed=v_ed, z=z, b_i=b_i).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

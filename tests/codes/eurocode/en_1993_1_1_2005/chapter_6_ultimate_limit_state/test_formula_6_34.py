"""Testing formula 6.34 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_34 import Form6Dot34CheckAxialForceY
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot34CheckAxialForceY:
    """Validation for formula 6.34 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        n_ed = 50.0
        h_w = 200.0
        t_w = 10.0
        f_y = 355.0
        gamma_m0 = 1.0

        formula = Form6Dot34CheckAxialForceY(n_ed=n_ed, h_w=h_w, t_w=t_w, f_y=f_y, gamma_m0=gamma_m0)

        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("h_w", "t_w", "f_y", "gamma_m0"),
        [
            (-200.0, 10.0, 355.0, 1.0),  # h_w is negative
            (200.0, -10.0, 355.0, 1.0),  # t_w is negative
            (200.0, 10.0, -355.0, 1.0),  # f_y is negative
            (200.0, 10.0, 355.0, -1.0),  # gamma_m0 is negative
            (200.0, 10.0, 355.0, 0.0),  # gamma_m0 is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, h_w: float, t_w: float, f_y: float, gamma_m0: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot34CheckAxialForceY(n_ed=50.0, h_w=h_w, t_w=t_w, f_y=f_y, gamma_m0=gamma_m0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to N_{Ed} \leq \frac{0.5 \cdot h_{w} \cdot t_{w} \cdot f_{y}}{\gamma_{M0}} \to "
                r"50.000 \leq \frac{0.5 \cdot 200.000 \cdot 10.000 \cdot 355.000}{1.000} \to OK",
            ),
            (
                "complete_with_units",
                r"CHECK \to N_{Ed} \leq \frac{0.5 \cdot h_{w} \cdot t_{w} \cdot f_{y}}{\gamma_{M0}} \to "
                r"50.000 \ N \leq \frac{0.5 \cdot 200.000 \ mm \cdot 10.000 \ mm \cdot 355.000 \ MPa}{1.000} \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        n_ed = 50.0
        h_w = 200.0
        t_w = 10.0
        f_y = 355.0
        gamma_m0 = 1.0

        latex = Form6Dot34CheckAxialForceY(n_ed=n_ed, h_w=h_w, t_w=t_w, f_y=f_y, gamma_m0=gamma_m0).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

"""Testing formula 6.16 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_16 import Form6Dot16CheckFlangeWithFastenerHoles
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot16CheckFlangeWithFastenerHoles:
    """Validation for formula 6.16 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_f_net = 100.0
        f_u = 400.0
        gamma_m2 = 1.1
        a_f = 120.0
        f_y = 250.0
        gamma_m0 = 1.0

        # Object to test
        formula = Form6Dot16CheckFlangeWithFastenerHoles(a_f_net=a_f_net, f_u=f_u, gamma_m2=gamma_m2, a_f=a_f, f_y=f_y, gamma_m0=gamma_m0)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("a_f_net", "f_u", "gamma_m2", "a_f", "f_y", "gamma_m0"),
        [
            (-100.0, 400.0, 1.1, 120.0, 250.0, 1.0),  # a_f_net is negative
            (100.0, -400.0, 1.1, 120.0, 250.0, 1.0),  # f_u is negative
            (100.0, 400.0, -1.1, 120.0, 250.0, 1.0),  # gamma_m2 is negative
            (100.0, 400.0, 1.1, -120.0, 250.0, 1.0),  # a_f is negative
            (100.0, 400.0, 1.1, 120.0, -250.0, 1.0),  # f_y is negative
            (100.0, 400.0, 1.1, 120.0, 250.0, -1.0),  # gamma_m0 is negative
            (100.0, 400.0, 0.0, 120.0, 250.0, 1.0),  # gamma_m2 is zero
            (100.0, 400.0, 1.1, 120.0, 250.0, 0.0),  # gamma_m0 is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self, a_f_net: float, f_u: float, gamma_m2: float, a_f: float, f_y: float, gamma_m0: float
    ) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot16CheckFlangeWithFastenerHoles(a_f_net=a_f_net, f_u=f_u, gamma_m2=gamma_m2, a_f=a_f, f_y=f_y, gamma_m0=gamma_m0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \left( \frac{A_{f,net} \cdot 0.9 \cdot f_{u}}{\gamma_{M2}} \geq \frac{A_{f} \cdot f_{y}}{\gamma_{M0}} \right) \to "
                r"\left( \frac{100.000 \cdot 0.9 \cdot 400.000}{1.100} \geq \frac{120.000 \cdot 250.000}{1.000} \right) \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_f_net = 100.0
        f_u = 400.0
        gamma_m2 = 1.1
        a_f = 120.0
        f_y = 250.0
        gamma_m0 = 1.0

        # Object to test
        latex = Form6Dot16CheckFlangeWithFastenerHoles(a_f_net=a_f_net, f_u=f_u, gamma_m2=gamma_m2, a_f=a_f, f_y=f_y, gamma_m0=gamma_m0).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

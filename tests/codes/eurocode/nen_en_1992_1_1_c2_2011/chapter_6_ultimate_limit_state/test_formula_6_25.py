"""Testing formula 6.25 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_25 import Form6Dot25DesignShearResistance
from blueprints.validations import GreaterThan90Error, LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot25DesignShearResistance:
    """Validation for formula 6.25 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        c = 0.5
        mu = 0.6
        f_ctd = 2.0
        sigma_n = 1.0
        a_s = 1000.0
        a_i = 200000.0
        f_yd = 500.0
        alpha = 30.0
        nu = 0.9
        f_cd = 30.0

        # Object to test
        formula = Form6Dot25DesignShearResistance(
            c=c, mu=mu, f_ctd=f_ctd, sigma_n=sigma_n, a_s=a_s, a_i=a_i, f_yd=f_yd, alpha=alpha, nu=nu, f_cd=f_cd
        )

        # Expected result, manually calculated
        manually_calculated_result = 4.51506350946  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("c", "mu", "f_ctd", "sigma_n", "a_s", "a_i", "f_yd", "alpha", "nu", "f_cd"),
        [
            (-0.5, 0.6, 2.0, 1.0, 1000.0, 200000.0, 500.0, 30.0, 0.9, 30.0),  # c is negative
            (0.5, -0.6, 2.0, 1.0, 1000.0, 200000.0, 500.0, 30.0, 0.9, 30.0),  # mu is negative
            (0.5, 0.6, -2.0, 1.0, 1000.0, 200000.0, 500.0, 30.0, 0.9, 30.0),  # f_ctd is negative
            (0.5, 0.6, 2.0, -1.0, 1000.0, 200000.0, 500.0, 30.0, 0.9, 30.0),  # sigma_n is negative
            (0.5, 0.6, 2.0, 1.0, -1000.0, 200000.0, 500.0, 30.0, 0.9, 30.0),  # a_s is negative
            (0.5, 0.6, 2.0, 1.0, 1000.0, -200000.0, 500.0, 30.0, 0.9, 30.0),  # a_i is negative
            (0.5, 0.6, 2.0, 1.0, 1000.0, 200000.0, -500.0, 30.0, 0.9, 30.0),  # f_yd is negative
            (0.5, 0.6, 2.0, 1.0, 1000.0, 200000.0, 500.0, -30.0, 0.9, 30.0),  # alpha is negative
            (0.5, 0.6, 2.0, 1.0, 1000.0, 200000.0, 500.0, 30.0, -0.9, 30.0),  # nu is negative
            (0.5, 0.6, 2.0, 1.0, 1000.0, 200000.0, 500.0, 30.0, 0.9, -30.0),  # f_cd is negative
            (0.5, 0.6, 2.0, 1.0, 1000.0, 0.0, 500.0, 30.0, 0.9, 30.0),  # a_i is zero
            (0.5, 0.6, 2.0, 1.0, 1000.0, 200000.0, 500.0, 100.0, 0.9, 30.0),  # alpha is greater than 90
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self, c: float, mu: float, f_ctd: float, sigma_n: float, a_s: float, a_i: float, f_yd: float, alpha: float, nu: float, f_cd: float
    ) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError, GreaterThan90Error)):
            Form6Dot25DesignShearResistance(c=c, mu=mu, f_ctd=f_ctd, sigma_n=sigma_n, a_s=a_s, a_i=a_i, f_yd=f_yd, alpha=alpha, nu=nu, f_cd=f_cd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"v_{Rdi} = \min \left( c \cdot f_{ctd} + \mu \cdot \sigma_{n} + \frac{A_{s}}{A_{i}} \cdot "
                r"f_{yd} \cdot (\mu \cdot \sin(\alpha) + \cos(\alpha)); 0.5 \cdot \nu \cdot f_{cd} \right) = "
                r"\min \left( 0.500 \cdot 2.000 + 0.600 \cdot 1.000 + \frac{1000.000}{200000.000} \cdot 500.000 \cdot "
                r"(0.600 \cdot \sin(30.000) + \cos(30.000)); 0.5 \cdot 0.900 \cdot 30.000 \right) = 4.515 \ MPa",
            ),
            ("short", r"v_{Rdi} = 4.515 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        c = 0.5
        mu = 0.6
        f_ctd = 2.0
        sigma_n = 1.0
        a_s = 1000.0
        a_i = 200000.0
        f_yd = 500.0
        alpha = 30.0
        nu = 0.9
        f_cd = 30.0

        # Object to test
        latex = Form6Dot25DesignShearResistance(
            c=c, mu=mu, f_ctd=f_ctd, sigma_n=sigma_n, a_s=a_s, a_i=a_i, f_yd=f_yd, alpha=alpha, nu=nu, f_cd=f_cd
        ).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

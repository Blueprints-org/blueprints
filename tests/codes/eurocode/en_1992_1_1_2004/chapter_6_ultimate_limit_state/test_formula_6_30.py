"""Testing formula 6.30 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_30 import Form6Dot30DesignTorsionalResistanceMoment
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot30DesignTorsionalResistanceMoment:
    """Validation for formula 6.30 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        nu = 0.6
        alpha_cw = 1.0
        f_cd = 30.0
        a_k = 1000.0
        t_ef_i = 200.0
        theta = 45.0

        # Object to test
        formula = Form6Dot30DesignTorsionalResistanceMoment(nu=nu, alpha_cw=alpha_cw, f_cd=f_cd, a_k=a_k, t_ef_i=t_ef_i, theta=theta)

        # Expected result, manually calculated
        manually_calculated_result = 3600000.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("nu", "alpha_cw", "f_cd", "a_k", "t_ef_i", "theta"),
        [
            (-0.6, 1.0, 30.0, 1000.0, 200.0, 45.0),  # nu is negative
            (0.6, -1.0, 30.0, 1000.0, 200.0, 45.0),  # alpha_cw is negative
            (0.6, 1.0, -30.0, 1000.0, 200.0, 45.0),  # f_cd is negative
            (0.6, 1.0, 30.0, -1000.0, 200.0, 45.0),  # a_k is negative
            (0.6, 1.0, 30.0, 1000.0, -200.0, 45.0),  # t_ef_i is negative
            (0.6, 1.0, 30.0, 1000.0, 200.0, -45.0),  # theta is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self, nu: float, alpha_cw: float, f_cd: float, a_k: float, t_ef_i: float, theta: float
    ) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot30DesignTorsionalResistanceMoment(nu=nu, alpha_cw=alpha_cw, f_cd=f_cd, a_k=a_k, t_ef_i=t_ef_i, theta=theta)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"T_{Rd,max} = 2 \cdot \nu \cdot \alpha_{cw} \cdot f_{cd} \cdot A_{k} \cdot t_{ef,i} \cdot \sin(\theta) \cdot \cos(\theta) = "
                r"2 \cdot 0.600 \cdot 1.000 \cdot 30.000 \cdot 1000.000 \cdot 200.000 \cdot \sin(45.000) \cdot \cos(45.000) = 3600000.000 "
                r"\ Nmm",
            ),
            ("short", r"T_{Rd,max} = 3600000.000 \ Nmm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        nu = 0.6
        alpha_cw = 1.0
        f_cd = 30.0
        a_k = 1000.0
        t_ef_i = 200.0
        theta = 45.0

        # Object to test
        latex = Form6Dot30DesignTorsionalResistanceMoment(nu=nu, alpha_cw=alpha_cw, f_cd=f_cd, a_k=a_k, t_ef_i=t_ef_i, theta=theta).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

"""Testing formula 5.3 of EN 1993-5:2007."""

import pytest

from blueprints.codes.eurocode.en_1993_5_2007.chapter_5_ultimate_limit_states.formula_5_3 import Form5Dot3DesignMomentResistanceClass3
from blueprints.validations import LessOrEqualToZeroError


class TestForm5Dot3DesignMomentResistanceClass3:
    """Validation for formula 5.3 from EN 1993-5:2007."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        beta_b = 0.5  # Dimensionless
        w_el = 20  # MM3
        f_y = 200  # MPA
        gamma_m_0 = 0.8  # Dimensionless
        form = Form5Dot3DesignMomentResistanceClass3(
            beta_b=beta_b,
            w_el=w_el,
            f_y=f_y,
            gamma_m_0=gamma_m_0,
        )

        # Expected result, manually calculated
        expected = 0.0025  # KNM

        assert form == pytest.approx(expected)

    @pytest.mark.parametrize(
        ("beta_b", "w_el", "f_y", "gamma_m_0"),
        [
            (-0.5, 1, 1, 1),  # beta_b is negative
            (0, 1, 1, 1),  # beta_b is zero
            (1, -0.5, 1, 1),  # w_el is negative
            (1, 0, 1, 1),  # w_el is zero
            (1, 1, -0.5, 1),  # f_y is negative
            (1, 1, 0, 1),  # f_y is zero
            (1, 1, 1, -0.5),  # gamma_m_0 is negative
            (1, 1, 1, 0),  # gamma_m_0 is zero
        ],
    )
    def test_raise_error_when_negative_or_zero_is_given(self, beta_b: float, w_el: float, f_y: float, gamma_m_0: float) -> None:
        """Test a negative and zero value for parameters beta_b, w_el, f_y, gamma_m_0."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot3DesignMomentResistanceClass3(beta_b=beta_b, w_el=w_el, f_y=f_y, gamma_m_0=gamma_m_0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"M_{c,Rd} = \beta_B W_{el} f_y / \gamma_{M0} = 0.5 \cdot 20 \cdot 200 / 0.8 / 1000000 = 0.00",
            ),
            ("short", r"M_{c,Rd} = 0.00"),
            (
                "string",
                r"M_{c,Rd} = \beta_B W_{el} f_y / \gamma_{M0} = 0.5 \cdot 20 \cdot 200 / 0.8 / 1000000 = 0.00",
            ),
        ],
    )
    def test_latex_output(self, representation: str, expected: str) -> None:
        """Test the latex implementation."""
        beta_b = 0.5  # Dimensionless
        w_el = 20  # MM3
        f_y = 200  # MPA
        gamma_m_0 = 0.8  # Dimensionless

        form_5_2_latex = Form5Dot3DesignMomentResistanceClass3(
            beta_b=beta_b,
            w_el=w_el,
            f_y=f_y,
            gamma_m_0=gamma_m_0,
        ).latex()

        actual = {
            "complete": form_5_2_latex.complete,
            "short": form_5_2_latex.short,
            "string": str(form_5_2_latex),
        }

        assert actual[representation] == expected, f"{representation} representation failed."

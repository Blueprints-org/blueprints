"""Testing formula 5.5 of EN 1993-5:2007."""

import pytest

from blueprints.codes.eurocode.en_1993_5_2007.chapter_5_ultimate_limit_states.formula_5_5 import Form5Dot5PlasticShearResistance
from blueprints.validations import LessOrEqualToZeroError


class TestForm5Dot5PlasticShearResistance:
    """Validation for formula 5.5 from EN 1993-5:2007."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        a_v = 200  # MM2
        f_y = 100  # MPA
        gamma_m_0 = 0.5  # DIMENSIONLESS
        form = Form5Dot5PlasticShearResistance(a_v=a_v, f_y=f_y, gamma_m_0=gamma_m_0)

        # Expected result, manually calculated
        expected = 23.0940  # KN

        assert form == pytest.approx(expected)

    @pytest.mark.parametrize(
        ("a_v", "f_y", "gamma_m_0"),
        [
            (-0.5, 100, 0.5),  # a_v is negative
            (0, 100, 0.5),  # a_v is zero
            (200, -100, 0.5),  # f_y is negative
            (200, 0, 0.5),  # f_y is zero
            (200, 100, -0.5),  # gamma_m_0 is negative
            (200, 100, 0),  # gamma_m_0 is zero
        ],
    )
    def test_raise_error_when_negative_or_zero_n_t_rd_is_given(self, a_v: float, f_y: float, gamma_m_0: float) -> None:
        """Test a negative and zero value for parameters a_v, f_y and gamma_m_0."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot5PlasticShearResistance(a_v=a_v, f_y=f_y, gamma_m_0=gamma_m_0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"V_{pl,Rd} = \frac{A_v f_y}{\sqrt{3} \gamma_{M0}} = \frac{200 \cdot 100}{\sqrt{3} \cdot 0.5} = 23.09",
            ),
            ("short", r"V_{pl,Rd} = 23.09"),
            (
                "string",
                r"V_{pl,Rd} = \frac{A_v f_y}{\sqrt{3} \gamma_{M0}} = \frac{200 \cdot 100}{\sqrt{3} \cdot 0.5} = 23.09",
            ),
        ],
    )
    def test_latex_output(self, representation: str, expected: str) -> None:
        """Test the latex implementation."""
        a_v = 200  # MM2
        f_y = 100  # MPA
        gamma_m_0 = 0.5  # DIMENSIONLESS

        form = Form5Dot5PlasticShearResistance(
            a_v=a_v,
            f_y=f_y,
            gamma_m_0=gamma_m_0,
        ).latex()

        actual = {
            "complete": form.complete,
            "short": form.short,
            "string": str(form),
        }

        assert actual[representation] == expected, f"{representation} representation failed."

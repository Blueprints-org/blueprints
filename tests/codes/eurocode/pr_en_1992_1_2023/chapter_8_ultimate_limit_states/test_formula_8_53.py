"""Testing formula 8.53 of prEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.pr_en_1992_1_2023.chapter_8_ultimate_limit_states.formula_8_53 import (
    Form8Dot53TensileChordLimitForIntermediateSupportOrConcentratedLoads,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot53TensileChordLimitForIntermediateSupportOrConcentratedLoads:
    """Validation for formula 8.53 from prEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        m_ed_max = 120e6  # Nmm
        z = 300.0  # mm
        n_ed = 10000.0  # N

        formula = Form8Dot53TensileChordLimitForIntermediateSupportOrConcentratedLoads(m_ed_max=m_ed_max, z=z, n_ed=n_ed)
        manually_calculated_result = m_ed_max / z + n_ed / 2

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("m_ed_max", "z", "n_ed"),
        [
            (-120e6, 300.0, 10000.0),  # m_ed_max negative
            (120e6, 300.0, -10000.0),  # n_ed negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, m_ed_max: float, z: float, n_ed: float) -> None:
        """Test negative values for m_ed_max, n_ed."""
        with pytest.raises(NegativeValueError):
            Form8Dot53TensileChordLimitForIntermediateSupportOrConcentratedLoads(m_ed_max=m_ed_max, z=z, n_ed=n_ed)

    @pytest.mark.parametrize(
        "z",
        [0.0, -300.0],
    )
    def test_raise_error_when_z_is_zero_or_negative(self, z: float) -> None:
        """Test zero and negative values for z."""
        m_ed_max = 120e6
        n_ed = 10000.0
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot53TensileChordLimitForIntermediateSupportOrConcentratedLoads(m_ed_max=m_ed_max, z=z, n_ed=n_ed)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"F_{td,max} = \frac{M_{Ed,max}}{z} + \frac{N_{Ed}}{2} = \frac{120000000.000}{300.000} + \frac{"
                r"10000.000}{2} = 405000.000 \ N",
            ),
            (
                "short",
                r"F_{td,max} = 405000.000 \ N",
            ),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        m_ed_max = 120e6
        z = 300.0
        n_ed = 10000.0

        latex = Form8Dot53TensileChordLimitForIntermediateSupportOrConcentratedLoads(m_ed_max=m_ed_max, z=z, n_ed=n_ed).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation]

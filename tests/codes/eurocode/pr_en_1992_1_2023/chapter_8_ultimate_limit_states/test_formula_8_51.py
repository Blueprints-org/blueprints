"""Testing formula 8.51 of prEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.pr_en_1992_1_2023.chapter_8_ultimate_limit_states.formula_8_51 import Form8Dot51TensileChordForceDueToShear
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot51TensileChordForceDueToShear:
    """Validation for formula 8.51 from prEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        m_ed = 120e6  # Nmm
        z = 300.0  # mm
        n_vd = 2000.0  # N
        n_ed = 10000.0  # N

        formula = Form8Dot51TensileChordForceDueToShear(m_ed=m_ed, z=z, n_vd=n_vd, n_ed=n_ed)
        manually_calculated_result = 120e6 / 300.0 + (2000.0 + 10000.0) / 2  # N

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("m_ed", "z", "n_vd", "n_ed"),
        [
            (-120000.0, 300.0, 20000.0, 10000.0),  # m_ed negative
            (120000.0, 300.0, -20000.0, 10000.0),  # n_vd negative
            (120000.0, 300.0, 20000.0, -10000.0),  # n_ed negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, m_ed: float, z: float, n_vd: float, n_ed: float) -> None:
        """Test negative values for m_ed, z, n_vd, n_ed."""
        with pytest.raises(NegativeValueError):
            Form8Dot51TensileChordForceDueToShear(m_ed=m_ed, z=z, n_vd=n_vd, n_ed=n_ed)

    @pytest.mark.parametrize(
        "z",
        [0.0, -300.0],
    )
    def test_raise_error_when_z_is_zero_or_negative(self, z: float) -> None:
        """Test zero and negative values for z."""
        m_ed = 120e6
        n_vd = 2000.0
        n_ed = 10000.0
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot51TensileChordForceDueToShear(m_ed=m_ed, z=z, n_vd=n_vd, n_ed=n_ed)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"F_{td} = \frac{M_{Ed}}{z} + \frac{N_{Vd} + N_{Ed}}{2} = \frac{120000000.000}{300.000} + \frac{"
                r"2000.000 + 10000.000}{2} = 406000.000 \ N",
            ),
            (
                "complete_with_units",
                r"F_{td} = \frac{M_{Ed}}{z} + \frac{N_{Vd} + N_{Ed}}{2} = \frac{120000000.000 \ Nmm}{300.000 \ mm} + "
                r"\frac{2000.000 \ N + 10000.000 \ N}{2} = 406000.000 \ N",
            ),
            (
                "short",
                r"F_{td} = 406000.000 \ N",
            ),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        m_ed = 120e6
        z = 300.0
        n_vd = 2000.0
        n_ed = 10000.0

        latex = Form8Dot51TensileChordForceDueToShear(m_ed=m_ed, z=z, n_vd=n_vd, n_ed=n_ed).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation]

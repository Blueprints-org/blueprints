"""Testing formula 8.52 of prEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.pr_en_1992_1_2023.chapter_8_ultimate_limit_states.formula_8_52 import Form8Dot52CompressiveChordForceDueToShear
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot52CompressiveChordForceDueToShear:
    """Validation for formula 8.52 from prEN 1992-1-1-2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        m_ed = 120e6  # Nmm
        z = 300.0        # mm
        n_vd = 2000.0   # N
        n_ed = 10000.0   # N

        formula = Form8Dot52CompressiveChordForceDueToShear(m_ed=m_ed, z=z, n_vd=n_vd, n_ed=n_ed)
        manually_calculated_result = 120e6 / 300.0 - (2000.0 + 10000.0) / 2  # N

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        "m_ed, z, n_vd, n_ed",
        [
            (-120e6, 300.0, 2000.0, 10000.0),  # m_ed negative
            (500000.0, 300.0, -2000.0, 10000.0),  # n_vd negative
            (500000.0, 300.0, 2000.0, -10000.0),  # n_ed negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, m_ed, z, n_vd, n_ed) -> None:
        """Test negative values for m_ed, n_vd, n_ed."""
        with pytest.raises(NegativeValueError):
            Form8Dot52CompressiveChordForceDueToShear(m_ed=m_ed, z=z, n_vd=n_vd, n_ed=n_ed)

    @pytest.mark.parametrize(
        "z",
        [0.0, -300.0],
    )
    def test_raise_error_when_z_is_zero_or_negative(self, z) -> None:
        """Test zero and negative values for z."""
        m_ed = 120e6
        n_vd = 2000.0
        n_ed = 10000.0
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot52CompressiveChordForceDueToShear(m_ed=m_ed, z=z, n_vd=n_vd, n_ed=n_ed)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"F_{cd} = \frac{M_{Ed}}{z} - \frac{N_{Vd} + N_{Ed}}{2} = \frac{120000000.000}{300.000} - \frac{2000.000 + 10000.000}{2} = 394000.000 \ N",
            ),
            (
                "short",
                r"F_{cd} = 394000.000 \ N",
            ),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        m_ed = 120e6
        z = 300.0
        n_vd = 2000.0
        n_ed = 10000.0

        latex = Form8Dot52CompressiveChordForceDueToShear(m_ed=m_ed, z=z, n_vd=n_vd, n_ed=n_ed).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation]

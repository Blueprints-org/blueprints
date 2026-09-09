"""Testing formulas 8.5, 8.6, 8.7 and 8.8 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_5_6_7_8 import (
    Form8Dot5To8DesignMomentsForOrthogonalReinforcement,
)


class TestForm8Dot5To8DesignMomentsForOrthogonalReinforcement:
    """Validation for formulas 8.5, 8.6, 8.7 and 8.8 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("is_x_direction", "is_primed", "expected"),
        [
            (True, False, 60e6),  # formula (8.5): m_edx + |m_edxy|
            (False, False, 40e6),  # formula (8.6): m_edy + |m_edxy|
            (True, True, -40e6),  # formula (8.7): -m_edx + |m_edxy|
            (False, True, -20e6),  # formula (8.8): -m_edy + |m_edxy|
        ],
    )
    def test_evaluation(self, is_x_direction: bool, is_primed: bool, expected: float) -> None:
        """Tests the evaluation of the result."""
        formula = Form8Dot5To8DesignMomentsForOrthogonalReinforcement(
            m_edx=50e6, m_edy=30e6, m_edxy=10e6, is_x_direction=is_x_direction, is_primed=is_primed
        )
        assert formula == pytest.approx(expected=expected, rel=1e-4)

    def test_evaluation_negative_torsional_moment(self) -> None:
        """Tests that only the magnitude of the torsional moment is used."""
        formula = Form8Dot5To8DesignMomentsForOrthogonalReinforcement(m_edx=50e6, m_edy=30e6, m_edxy=-10e6, is_x_direction=True, is_primed=False)
        assert formula == pytest.approx(expected=60e6, rel=1e-4)

    @pytest.mark.parametrize(
        ("is_x_direction", "is_primed", "expected"),
        [
            (
                True,
                False,
                (
                    r"m_{Rdx} = m_{Edx} + \left|m_{Edxy}\right| = "
                    r"50000000.000 + \left|10000000.000\right| = 60000000.000 \ Nmm"
                ),
            ),
            (
                False,
                False,
                (
                    r"m_{Rdy} = m_{Edy} + \left|m_{Edxy}\right| = "
                    r"30000000.000 + \left|10000000.000\right| = 40000000.000 \ Nmm"
                ),
            ),
            (
                True,
                True,
                (
                    r"m_{Rdx}' = -m_{Edx} + \left|m_{Edxy}\right| = "
                    r"-50000000.000 + \left|10000000.000\right| = -40000000.000 \ Nmm"
                ),
            ),
            (
                False,
                True,
                (
                    r"m_{Rdy}' = -m_{Edy} + \left|m_{Edxy}\right| = "
                    r"-30000000.000 + \left|10000000.000\right| = -20000000.000 \ Nmm"
                ),
            ),
        ],
    )
    def test_latex_complete(self, is_x_direction: bool, is_primed: bool, expected: str) -> None:
        """Test the complete latex representation of the formula for all four cases."""
        latex = Form8Dot5To8DesignMomentsForOrthogonalReinforcement(
            m_edx=50e6, m_edy=30e6, m_edxy=10e6, is_x_direction=is_x_direction, is_primed=is_primed
        ).latex()

        assert latex.complete == expected

    def test_latex_complete_with_units(self) -> None:
        """Test the complete_with_units latex representation of the formula."""
        latex = Form8Dot5To8DesignMomentsForOrthogonalReinforcement(m_edx=50e6, m_edy=30e6, m_edxy=10e6, is_x_direction=True, is_primed=False).latex()

        assert latex.complete_with_units == (
            r"m_{Rdx} = m_{Edx} + \left|m_{Edxy}\right| = "
            r"50000000.000 \ Nmm + \left|10000000.000 \ Nmm\right| = 60000000.000 \ Nmm"
        )

    def test_latex_short(self) -> None:
        """Test the short latex representation of the formula."""
        latex = Form8Dot5To8DesignMomentsForOrthogonalReinforcement(m_edx=50e6, m_edy=30e6, m_edxy=10e6, is_x_direction=True, is_primed=False).latex()

        assert latex.short == r"m_{Rdx} = 60000000.000 \ Nmm"

"""Testing formula 8.64 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_64 import (
    Form8Dot64ShearStressResistanceWithTransverseBending,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot64ShearStressResistanceWithTransverseBending:
    """Validation for formula 8.64 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("m_ed", "expected"),
        [
            # a quarter of the bending resistance, so tau_rd times the root of three quarters
            (25000.0, 2.598076211353316),
            # three quarters of it, where the reduction is already a halving
            (75000.0, 1.5),
            # without transverse bending the resistance is untouched
            (0.0, 3.0),
            # at the bending resistance the root vanishes and no shear resistance is left
            (100000.0, 0.0),
        ],
    )
    def test_evaluation(self, m_ed: float, expected: float) -> None:
        """Tests the evaluation of the result, including both ends of the range of the root."""
        # Create object to test
        formula = Form8Dot64ShearStressResistanceWithTransverseBending(tau_rd=3.0, m_ed=m_ed, m_rd=100000.0)

        # Perform test by assert
        assert formula == pytest.approx(expected=expected, rel=1e-4)

    @pytest.mark.parametrize(
        ("tau_rd", "m_ed", "m_rd"),
        [
            (-3.0, 25000.0, 100000.0),  # tau_rd is negative
            (3.0, -25000.0, 100000.0),  # m_ed is negative
            # a transverse bending moment above the bending resistance leaves no real square root
            (3.0, 150000.0, 100000.0),
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, tau_rd: float, m_ed: float, m_rd: float) -> None:
        """Test if error is raised for parameters, or a radicand, that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot64ShearStressResistanceWithTransverseBending(tau_rd=tau_rd, m_ed=m_ed, m_rd=m_rd)

    @pytest.mark.parametrize(
        ("tau_rd", "m_ed", "m_rd"),
        [
            (3.0, 25000.0, -100000.0),  # m_rd is negative
            (3.0, 25000.0, 0.0),  # m_rd is zero
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero(self, tau_rd: float, m_ed: float, m_rd: float) -> None:
        """Test if error is raised for parameters that are not allowed to be zero or less."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot64ShearStressResistanceWithTransverseBending(tau_rd=tau_rd, m_ed=m_ed, m_rd=m_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\tau_{Rdm} = \tau_{Rd} \cdot \sqrt{1 - \frac{m_{Ed}}{m_{Rd}}} = "
                r"3.000 \cdot \sqrt{1 - \frac{25000.000}{100000.000}} = 2.598 \ MPa",
            ),
            (
                "complete_with_units",
                r"\tau_{Rdm} = \tau_{Rd} \cdot \sqrt{1 - \frac{m_{Ed}}{m_{Rd}}} = "
                r"3.000 \ MPa \cdot \sqrt{1 - \frac{25000.000 \ Nmm/mm}{100000.000 \ Nmm/mm}} = 2.598 \ MPa",
            ),
            ("short", r"\tau_{Rdm} = 2.598 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        test_latex = Form8Dot64ShearStressResistanceWithTransverseBending(tau_rd=3.0, m_ed=25000.0, m_rd=100000.0).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]

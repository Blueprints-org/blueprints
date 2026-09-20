"""Testing formula 8.2 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_2 import (
    Form8Dot2CheckBiaxialBending,
)
from blueprints.validations import LessOrEqualToZeroError


class TestForm8Dot2CheckBiaxialBending:
    """Validation for formula 8.2 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("m_edz", "expected"),
        [
            (100e6, True),  # the biaxial bending criterion is satisfied
            (190e6, False),  # the biaxial bending criterion is not satisfied
        ],
    )
    def test_evaluation(self, m_edz: float, expected: bool) -> None:
        """Tests the evaluation of the result."""
        formula = Form8Dot2CheckBiaxialBending(m_edz=m_edz, m_rdz_n=200e6, m_edy=50e6, m_rdy_n=150e6, a_n=1.5)
        assert bool(formula) is expected

    def test_evaluation_negative_moments(self) -> None:
        """Tests that only the magnitude of the moments is used."""
        formula = Form8Dot2CheckBiaxialBending(m_edz=-100e6, m_rdz_n=200e6, m_edy=-50e6, m_rdy_n=150e6, a_n=1.5)
        assert bool(formula) is True

    @pytest.mark.parametrize(
        ("m_rdz_n", "m_rdy_n"),
        [
            (-200e6, 150e6),  # m_rdz_n is negative
            (0.0, 150e6),  # m_rdz_n is zero
            (200e6, -150e6),  # m_rdy_n is negative
            (200e6, 0.0),  # m_rdy_n is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, m_rdz_n: float, m_rdy_n: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot2CheckBiaxialBending(m_edz=100e6, m_rdz_n=m_rdz_n, m_edy=50e6, m_rdy_n=m_rdy_n, a_n=1.5)

    @pytest.mark.parametrize(
        ("m_edz", "representation", "expected"),
        [
            (
                100e6,
                "complete",
                (
                    r"CHECK \to \left(\frac{\left|M_{Edz}\right|}{M_{Rdz,N}}\right)^{a_N} + "
                    r"\left(\frac{\left|M_{Edy}\right|}{M_{Rdy,N}}\right)^{a_N} \leq 1.0 \to "
                    r"\left(\frac{\left|100000000.000\right|}{200000000.000}\right)^{1.500} + "
                    r"\left(\frac{\left|50000000.000\right|}{150000000.000}\right)^{1.500} \leq 1.0 \to OK"
                ),
            ),
            (
                100e6,
                "complete_with_units",
                (
                    r"CHECK \to \left(\frac{\left|M_{Edz}\right|}{M_{Rdz,N}}\right)^{a_N} + "
                    r"\left(\frac{\left|M_{Edy}\right|}{M_{Rdy,N}}\right)^{a_N} \leq 1.0 \to "
                    r"\left(\frac{\left|100000000.000 \ Nmm\right|}{200000000.000 \ Nmm}\right)^{1.500} + "
                    r"\left(\frac{\left|50000000.000 \ Nmm\right|}{150000000.000 \ Nmm}\right)^{1.500} \leq 1.0 \to OK"
                ),
            ),
            (100e6, "short", r"CHECK \to OK"),
            (190e6, "short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, m_edz: float, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = Form8Dot2CheckBiaxialBending(m_edz=m_edz, m_rdz_n=200e6, m_edy=50e6, m_rdy_n=150e6, a_n=1.5).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

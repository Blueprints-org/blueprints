"""Tests for formula 11.1 from prEN 1995-1-1: Chapter 11 - Connections."""

import pytest

from blueprints.codes.eurocode.pren_1995_1_1_2023.chapter_11_connections.formula_11_1 import Form11Dot1AxialTensileResistance
from blueprints.validations import LessOrEqualToZeroError


class TestForm11Dot1AxialTensileResistance:
    """Validation for formula 11.1 from prEN 1995-1-1."""

    @pytest.mark.parametrize(
        ("k_mod", "gamma_r", "f_pull_k", "f_w_k", "expected"),
        [
            (0.55, 1.3, 15, 1, 6.35),
            (1.10, 1.3, 15, 1, 12.69),
            (0.55, 1.3, 1, 15, 6.35),
            (1.10, 1.3, 1, 15, 12.69),
        ],
    )
    def test_evaluation(self, k_mod: float, gamma_r: float, f_pull_k: float, f_w_k: float, expected: float) -> None:
        """Test the evaluation of the result."""
        form = Form11Dot1AxialTensileResistance(k_mod=k_mod, gamma_r=gamma_r, f_pull_k=f_pull_k, f_w_k=f_w_k)
        assert form == pytest.approx(expected, rel=1e-3)

    @pytest.mark.parametrize(
        ("k_mod", "gamma_r", "f_pull_k", "f_w_k"),
        [
            (-1.0, 1.2, 10.0, 10.0),
            (1.0, -1.2, 10.0, 10.0),
            (1.0, 1.2, -10.0, 10.0),
            (1.0, 1.2, 10.0, -10.0),
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero(self, k_mod: float, gamma_r: float, f_pull_k: float, f_w_k: float) -> None:
        """Test values that are less than or equal to zero raise error."""
        with pytest.raises(LessOrEqualToZeroError):
            Form11Dot1AxialTensileResistance(k_mod=k_mod, gamma_r=gamma_r, f_pull_k=f_pull_k, f_w_k=f_w_k)

    @pytest.mark.parametrize(
        ("k_mod", "gamma_r", "f_pull_k", "f_w_k", "representation", "expected"),
        [
            (
                0.9,
                1.2,
                15,
                12,
                "complete",
                r"F_{ax,t,d} = \frac{k_{mod}}{\gamma_R} \cdot \max  \left \{ \begin{array}{c}F_{pull,k} \\ F_{w,k} \end{array}}"
                r" = \frac{0.90}{1.20} \cdot \max  \left \{ \begin{array}{c}15.00 \\ 12.00 \end{array}} = 11.25 kN",
            ),
            (0.9, 1.2, 15, 12, "short", r"F_{ax,t,d} = 11.25 kN"),
        ],
    )
    def test_latex(self, k_mod: float, gamma_r: float, f_pull_k: float, f_w_k: float, representation: str, expected: str) -> None:
        """Test the LaTeX representation of the formula."""
        form_latex = Form11Dot1AxialTensileResistance(k_mod=k_mod, gamma_r=gamma_r, f_pull_k=f_pull_k, f_w_k=f_w_k).latex()

        actual = {
            "complete": form_latex.complete,
            "short": form_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."

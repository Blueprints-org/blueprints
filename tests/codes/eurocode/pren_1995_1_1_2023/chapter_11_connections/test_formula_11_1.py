"""Tests for formula 11.1 from prEN 1995-1-1: Chapter 11 - Connections."""

import pytest
from pytest import approx

from blueprints.codes.eurocode.pren_1995_1_1_2023.chapter_11_connections.formula_11_1 import Form11Dot1AxialTensileResistance
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm11Dot1AxialTensileResistance:
    """Validation for formula 11.1 from prEN 1995-1-1."""

    @pytest.mark.parametrize(
        ("k_mod", "gamma_r", "f_pull_k", "f_w_k", "expected"),
        [
            (0.55, 1.3, 15, 1, 6.388),
            (1.10, 1.3, 15, 1, 6.388),
            (0.55, 1.3, 1, 15, 6.388),
            (1.10, 1.3, 1, 15, 12.777),
        ],
    )
    def test_evaluation(
        self, k_mod: float, gamma_r: float, f_pull_k: float, f_w_k: float, expected: float
    ) -> None:
        """Test the evaluation of the result."""
        form = Form11Dot1AxialTensileResistance(
            k_mod=k_mod, gamma_r=gamma_r, f_pull_k=f_pull_k, f_w_k=f_w_k
        )
        assert form.result == approx(expected, rel=1e-3)

    @pytest.mark.parametrize(
        ("k_mod", "gamma_r", "f_pull_k", "f_w_k"),
        [
            (-1.0, 1.2, 10.0, 10.0),
            (1.0, -1.2, 10.0, 10.0),
            (1.0, 1.2, -10.0, 10.0),
            (1.0, 1.2, 10.0, -10.0),
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero(
        self, k_mod: float, gamma_r: float, f_pull_k: float, f_w_k: float
    ) -> None:
        """Test values that are less than or equal to zero for critical parameters."""
        with pytest.raises(LessOrEqualToZeroError):
            Form11Dot1AxialTensileResistance(
                k_mod=k_mod, gamma_r=gamma_r, f_pull_k=f_pull_k, f_w_k=f_w_k
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"F_{ax,t,d} = \frac{k_{mod}}{\gamma_R} \cdot \max \left \{ \begin{array}{c}F_{pull,k} \\ F_{w,k} \end{array} \right \} "
                r"= \frac{0.90}{1.20} \cdot \max(15.00, 12.00) = 11.25",
            ),
            ("short", r"F_{ax,t,d} = 11.25"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the LaTeX representation of the formula."""
        # Example values
        k_mod = 0.9
        gamma_r = 1.2
        f_pull_k = 15.0
        f_w_k = 12.0

        # Object to test
        form_latex = Form11Dot1AxialTensileResistance(
            k_mod=k_mod, gamma_r=gamma_r, f_pull_k=f_pull_k, f_w_k=f_w_k
        ).latex()

        actual = {
            "complete": form_latex.complete,
            "short": form_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."

"""Testing formula 5.13N of NEN-EN 1992-1-1+C2:2011."""

import math
import unittest

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_5_structural_analysis.formula_5_13n import (
    Form5Dot13NSlendernessCriterion,
    SubForm5Dot13NOmegaMechanicalReinforcementRatio,
    SubForm5Dot13NRelativeNormalForce,
    SubForm5Dot13NRmMomentRatio,
)


class TestForm5Dot13NSlendernessCriterion(unittest.TestCase):
    """Validation for formula 5.13N from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluate(self) -> None:
        """Tests the evaluation of the result."""
        phi_eff = 2.0
        omega = SubForm5Dot13NOmegaMechanicalReinforcementRatio(1000, 500, 2000, 30)
        rm = SubForm5Dot13NRmMomentRatio(10, 20)
        n = SubForm5Dot13NRelativeNormalForce(500, 2000, 30)

        formula = Form5Dot13NSlendernessCriterion(phi_eff, omega, rm, n)
        expected = 20 * (1 / (1 + 0.2 * phi_eff)) * (1000 * 500 / (2000 * 30)) * (1.7 - (10 / 20)) / math.sqrt(500 / (2000 * 30))

        assert formula == pytest.approx(expected=expected, rel=1e-3)

    def test_latex(self) -> None:
        """Test the latex representation of the formula."""
        phi_eff = 2.0
        omega = SubForm5Dot13NOmegaMechanicalReinforcementRatio(1000, 500, 2000, 30)
        rm = SubForm5Dot13NRmMomentRatio(10, 20)
        n = SubForm5Dot13NRelativeNormalForce(500, 2000, 30)

        formula = Form5Dot13NSlendernessCriterion(phi_eff, omega, rm, n)
        latex = formula.latex()

        assert latex.return_symbol == r"\lambda_{lim}"
        assert latex.equation == r"20 \cdot A \cdot B \cdot C / \sqrt{n}"
        assert latex.numeric_equation == rf"20 \cdot {formula.calculate_a(phi_eff)} \cdot {omega} \cdot " rf"{formula.calculate_c(rm)} / \sqrt{{{n}}}"
        assert latex.comparison_operator_label == "="


class TestSubForm5Dot13NOmegaMechanicalReinforcementRatio(unittest.TestCase):
    """Validation for formula 5.13N Omega sub-formula from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluate(self) -> None:
        """Tests the evaluation of the result."""
        formula = SubForm5Dot13NOmegaMechanicalReinforcementRatio(1000, 500, 2000, 30)
        result = formula
        assert result == pytest.approx(expected=(1000 * 500) / (2000 * 30), rel=1e-3)

    def test_latex(self) -> None:
        """Test the latex representation of the formula."""
        formula = SubForm5Dot13NOmegaMechanicalReinforcementRatio(1000, 500, 2000, 30)
        latex = formula.latex()
        assert latex.return_symbol == r"\omega"
        assert latex.equation == r"\frac{A_s \cdot f_{yd}}{A_c \cdot f_{cd}}"
        assert latex.numeric_equation == r"\frac{1000 \cdot 500}{2000 \cdot 30}"
        assert latex.comparison_operator_label == "="


class TestSubForm5Dot13NRelativeNormalForce(unittest.TestCase):
    """Validation for formula 5.13N Relative Normal Force sub-formula from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluate(self) -> None:
        """Tests the evaluation of the result."""
        formula = SubForm5Dot13NRelativeNormalForce(500, 2000, 30)
        result = formula
        assert result == pytest.approx(expected=500 / (2000 * 30), rel=1e-3)

    def test_latex(self) -> None:
        """Test the latex representation of the formula."""
        formula = SubForm5Dot13NRelativeNormalForce(500, 2000, 30)
        latex = formula.latex()
        assert latex.return_symbol == r"n"
        assert latex.equation == r"\frac{N_{Ed}}{A_c \cdot f_{cd}}"
        assert latex.numeric_equation == r"\frac{500}{2000 \cdot 30}"
        assert latex.comparison_operator_label == "="


class TestSubForm5Dot13NRmMomentRatio(unittest.TestCase):
    """Validation for formula 5.13N Rm Moment Ratio sub-formula from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluate(self) -> None:
        """Tests the evaluation of the result."""
        formula = SubForm5Dot13NRmMomentRatio(10, 20)
        result = formula
        assert result == pytest.approx(expected=10 / 20, rel=1e-3)

    def test_latex(self) -> None:
        """Test the latex representation of the formula."""
        formula = SubForm5Dot13NRmMomentRatio(10, 20)
        latex = formula.latex()
        assert latex.return_symbol == r"rm"
        assert latex.equation == r"\frac{M_{01}}{M_{02}}"
        assert latex.numeric_equation == r"\frac{10}{20}"
        assert latex.comparison_operator_label == "="


class TestForm5Dot13NSlendernessCriterionStaticMethods(unittest.TestCase):
    """Tests for the static methods of Form5Dot13NSlendernessCriterion."""

    def test_calculate_a(self) -> None:
        """Test the calculate_a method."""
        assert Form5Dot13NSlendernessCriterion.calculate_a(0.5) == 1 / (1 + 0.2 * 0.5)
        assert Form5Dot13NSlendernessCriterion.calculate_a(None) == 0.7

    def test_calculate_b(self) -> None:
        """Test the calculate_b method."""
        assert Form5Dot13NSlendernessCriterion.calculate_b(0.3) == 0.3
        assert Form5Dot13NSlendernessCriterion.calculate_b(None) == 1.1

    def test_calculate_c(self) -> None:
        """Test the calculate_c method."""
        assert Form5Dot13NSlendernessCriterion.calculate_c(0.2) == 1.7 - 0.2
        assert Form5Dot13NSlendernessCriterion.calculate_c(None) == 0.7

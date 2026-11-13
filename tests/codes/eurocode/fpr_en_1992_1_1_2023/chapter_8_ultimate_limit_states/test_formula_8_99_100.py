"""Testing formulas 8.99 and 8.100 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_99_100 import (
    Form8Dot99To100CoefficientAccountingForAxialForces,
)
from blueprints.validations import LessOrEqualToZeroError


class TestForm8Dot99To100CoefficientAccountingForAxialForces:
    """Validation for formulas 8.99 and 8.100 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("k_n", "is_axial_force_compressive", "expected"),
        [
            (1.158982, True, 1.158982),  # compressive axial force, formula (8.99)
            (1.158982, False, 0.862826),  # tensile axial force, formula (8.100)
        ],
    )
    def test_evaluation(self, k_n: float, is_axial_force_compressive: bool, expected: float) -> None:
        """Tests the evaluation of the result."""
        formula = Form8Dot99To100CoefficientAccountingForAxialForces(k_n=k_n, is_axial_force_compressive=is_axial_force_compressive)

        assert formula == pytest.approx(expected=expected, rel=1e-4)

    @pytest.mark.parametrize(
        ("k_n", "is_axial_force_compressive"),
        [
            (-1.158982, True),  # k_n is negative
            (0.0, True),  # k_n is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, k_n: float, is_axial_force_compressive: bool) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot99To100CoefficientAccountingForAxialForces(k_n=k_n, is_axial_force_compressive=is_axial_force_compressive)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"k_{pp} = \begin{cases} k_N & \text{if compressive axial force} \\ 1/k_N & \text{if tensile axial force} \end{cases} = "
                    r"\begin{cases} 1.159 & \text{if compressive axial force} \\ 1/1.159 & \text{if tensile axial force} \end{cases} = 1.159 \ -"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"k_{pp} = \begin{cases} k_N & \text{if compressive axial force} \\ 1/k_N & \text{if tensile axial force} \end{cases} = "
                    r"\begin{cases} 1.159 & \text{if compressive axial force} \\ 1/1.159 & \text{if tensile axial force} \end{cases} = 1.159 \ -"
                ),
            ),
            ("short", r"k_{pp} = 1.159 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        k_n = 1.158982
        is_axial_force_compressive = True

        # Object to test
        latex = Form8Dot99To100CoefficientAccountingForAxialForces(k_n=k_n, is_axial_force_compressive=is_axial_force_compressive).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

"""Formula 8.99 and 8.100 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form8Dot99To100CoefficientAccountingForAxialForces(Formula):
    r"""Class representing formulas 8.99 and 8.100 for the calculation of the coefficient [$k_{pp}$] accounting
    for axial forces, by which the punching shear gradient enhancement coefficient [$k_{pb}$] of Formula (8.96)
    may be multiplied for slabs with axial forces and for prestressed slabs.
    """

    label = "8.99/8.100"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        k_n: DIMENSIONLESS,
        is_axial_force_compressive: bool,
    ) -> None:
        r"""[$k_{pp}$] Coefficient accounting for the presence of axial forces [$-$].

        FprEN 1992-1-1:2023 (E) art. 8.4.3(4) - Formula (8.99) and (8.100)

        Parameters
        ----------
        k_n : DIMENSIONLESS
            [$k_N$] Factor accounting for axial forces and prestressing, according to Formula (8.101) or, for
            prestressed slabs with eccentric tendons, Formula (8.103) [$-$].
        is_axial_force_compressive : bool
            True for compressive axial forces (e.g. prestressing), which selects Formula (8.99). False for
            tensile axial forces, which selects Formula (8.100).
        """
        super().__init__()
        self.k_n = k_n
        self.is_axial_force_compressive = is_axial_force_compressive

    @staticmethod
    def _evaluate(
        k_n: DIMENSIONLESS,
        is_axial_force_compressive: bool,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(k_n=k_n)

        if is_axial_force_compressive:
            return k_n
        return 1 / k_n

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formulas 8.99 and 8.100."""
        _equation: str = r"\begin{cases} k_N & \text{if compressive axial force} \\ 1/k_N & \text{if tensile axial force} \end{cases}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"k_N": f"{self.k_n:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"k_N": f"{self.k_n:.{n}f}",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"k_{pp}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )

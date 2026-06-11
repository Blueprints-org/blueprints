"""Formula NB.NB.7 from NEN-EN 1993-1-1:2006: Chapter NB.NB - Reduction factor k_red."""

from blueprints.codes.eurocode.national_annex.nl.nen_en_1993_1_1_2006 import NEN_EN_1993_1_1_2006_A1_2014_NB_2016
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS


class FormNBDotNB7ReductionFactorKred(Formula):
    r"""Class representing formula NB.NB.7 for the calculation of [$k_{red}$]."""

    label = "NB.NB.7"
    source_document = NEN_EN_1993_1_1_2006_A1_2014_NB_2016

    def __init__(self) -> None:
        r"""[$k_{red}$] Reduction factor dependent on the degree of deformation of the beam cross-section with regard to beam length [-].

        NEN-EN 1993-1-1:2006 art.NB.NB.4.2(2) - Formula (NB.NB.7)

        Notes
        -----
        This formula applies when h / t_w ≤ 75.
        """
        super().__init__()

    @staticmethod
    def _evaluate() -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        return 1.0

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula NB.NB.7."""
        _equation: str = r"1"
        _numeric_equation: str = r"1"
        _numeric_equation_with_units: str = r"1"
        return LatexFormula(
            return_symbol=r"k_{red}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )

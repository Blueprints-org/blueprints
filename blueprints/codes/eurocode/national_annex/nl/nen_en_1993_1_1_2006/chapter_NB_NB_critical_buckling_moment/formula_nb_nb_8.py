"""Formula NB.NB.8 from NEN-EN 1993-1-1:2006: Chapter NB.NB - Reduction factor k_red."""

from blueprints.codes.eurocode.national_annex.nl.nen_en_1993_1_1_2006 import NEN_EN_1993_1_1_2006_A1_2014_NB_2016
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_negative


class FormNBDotNB8ReductionFactorKred(Formula):
    r"""Class representing formula NB.NB.8 for the calculation of [$k_{red}$]."""

    label = "NB.NB.8"
    source_document = NEN_EN_1993_1_1_2006_A1_2014_NB_2016

    def __init__(
        self,
        alpha: DIMENSIONLESS,
    ) -> None:
        r"""[$k_{red}$] Reduction factor dependent on the degree of deformation of the beam cross-section with regard to beam length [-].

        NEN-EN 1993-1-1:2006 art.NB.NB.4.2(2) - Formula (NB.NB.8)

        Parameters
        ----------
        alpha : DIMENSIONLESS
            [$\alpha$] Parameter dependent on beam dimensions; for calculating [$\alpha$] applies NB.NB.4.2 [-].

        Notes
        -----
        This formula applies when h / t_w > 75 and α ≤ 5,000.
        """
        super().__init__()
        self.alpha = alpha

    @staticmethod
    def _evaluate(
        alpha: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(alpha=alpha)
        if alpha > 5000:
            raise ValueError(f"alpha must be ≤ 5000 for this formula to be valid. Got alpha={alpha}")

        return min(((-5.4e-5 * alpha) + 1.03), 1.0)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula NB.NB.8."""
        _equation: str = r"\min\left(\left(\left(-5.4 \cdot 10^{-5} \cdot \alpha\right) + 1.03\right), 1\right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\alpha": f"{self.alpha:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = _numeric_equation
        return LatexFormula(
            return_symbol=r"k_{red}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )

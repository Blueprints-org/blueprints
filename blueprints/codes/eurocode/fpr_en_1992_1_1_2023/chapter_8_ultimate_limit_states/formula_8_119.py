"""Formula 8.119 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, DIMENSIONLESS
from blueprints.utils.math_helpers import cot
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form8Dot119StrengthReductionFactorCrossedByTieRefined(Formula):
    """Class representing formula 8.119 for the calculation of the strength reduction factor for compression
    fields and struts crossed or deviated by a tie at an angle, as an alternative to formulas (8.115) to (8.118).
    """

    label = "8.119"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        theta_cs: DEG,
    ) -> None:
        r"""[$\nu$] Strength reduction factor for compression fields and struts crossed or deviated by a tie at an
        angle [$-$].

        FprEN 1992-1-1:2023 (E) art. 8.5.2(4) - Formula (8.119)

        Parameters
        ----------
        theta_cs : DEG
            [$\theta_{cs}$] Smallest angle between the strut representing the resultant of the compression field
            and any of the ties that cross with the strut, as defined in Figure 8.26 [$degrees$].
        """
        super().__init__()
        self.theta_cs = theta_cs

    @staticmethod
    def _evaluate(
        theta_cs: DEG,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(theta_cs=theta_cs)
        cot_theta_cs = cot(theta_cs)
        return 1 / (1.11 + 0.22 * cot_theta_cs**2)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.119."""
        _equation: str = r"\frac{1}{1.11 + 0.22 \cdot \left(\cot(\theta_{cs})\right)^2}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\theta_{cs}": f"{self.theta_cs:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\theta_{cs}": rf"{self.theta_cs:.{n}f} ^\circ",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"\nu",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )

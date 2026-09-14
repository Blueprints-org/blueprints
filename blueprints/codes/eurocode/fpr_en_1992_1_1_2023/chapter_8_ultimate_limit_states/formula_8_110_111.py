"""Formula 8.110 and 8.111 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot110To111CoefficientForPunchingShearReinforcingSystem(Formula):
    r"""Class representing formulas 8.110 and 8.111 for the calculation of the coefficient [$\eta_{sys}$]
    accounting for the performance of punching shear reinforcing systems, unless the National Annex gives
    different values.

    The standard writes each branch as an expression bounded from below by [$1,0$], which is implemented as
    the maximum of the two.
    """

    label = "8.110/8.111"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        b_0: MM,
        d_v: MM,
        is_stud: bool,
    ) -> None:
        r"""[$\eta_{sys}$] Coefficient accounting for the performance of punching shear reinforcing systems
        [$-$].

        FprEN 1992-1-1:2023 (E) art. 8.4.4(5), NOTE - Formula (8.110) and (8.111)

        Parameters
        ----------
        b_0 : MM
            [$b_0$] Length of the perimeter at the face of the supporting area, see Formula (8.96) [$mm$].
        d_v : MM
            [$d_v$] Shear-resisting effective depth of the slab according to Formula (8.91) [$mm$].
        is_stud : bool
            True for shear reinforcement in the form of studs, which selects Formula (8.110). False for shear
            reinforcement in the form of links and stirrups, which selects Formula (8.111).
        """
        super().__init__()
        self.b_0 = b_0
        self.d_v = d_v
        self.is_stud = is_stud

    @staticmethod
    def _evaluate(
        b_0: MM,
        d_v: MM,
        is_stud: bool,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(b_0=b_0)
        raise_if_less_or_equal_to_zero(d_v=d_v)

        base = 0.70 if is_stud else 0.50
        return max(base + 0.63 * (b_0 / d_v) ** (1 / 4), 1.0)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formulas 8.110 and 8.111."""
        _equation: str = (
            r"\begin{cases} \max\left(0.70 + 0.63 \cdot \left(\frac{b_0}{d_v}\right)^{\frac{1}{4}}, 1.0\right) & "
            r"\text{if studs} \\ \max\left(0.50 + 0.63 \cdot \left(\frac{b_0}{d_v}\right)^{\frac{1}{4}}, 1.0\right) & "
            r"\text{if links and stirrups} \end{cases}"
        )
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"b_0": f"{self.b_0:.{n}f}",
                r"d_v": f"{self.d_v:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"b_0": rf"{self.b_0:.{n}f} \ mm",
                r"d_v": rf"{self.d_v:.{n}f} \ mm",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\eta_{sys}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )

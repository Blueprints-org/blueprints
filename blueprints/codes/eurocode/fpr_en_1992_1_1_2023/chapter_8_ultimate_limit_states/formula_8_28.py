"""Formula 8.28 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot28LongitudinalReinforcementRatio(Formula):
    r"""Class representing formula 8.28 for the calculation of the longitudinal tensile reinforcement ratio.

    Which effective depth belongs here is not settled by the standard. The "where" list is shared between
    Formulas (8.27) and (8.28) and says that [$d$] may be refined according to 8.2.2(3) and 8.2.2(4), while both
    of those paragraphs name Formula (8.27) alone: (3) replaces [$d$] in Formula (8.27) by the mechanical shear
    span [$a_v$], and (4) multiplies [$d$] in Formula (8.27) or [$a_v$] in Formula (8.29) by [$k_{vp}$].
    Neither mentions (8.28).

    This class therefore takes the unrefined effective depth. A caller who reads the shared list the other way
    can pass the refined value instead, and should be aware that it then also enters (8.27) through
    [$\rho_l$].
    """

    label = "8.28"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, a_sl: MM2, b_w: MM, d: MM) -> None:
        r"""[$\rho_l$] Longitudinal tensile reinforcement ratio [$-$].

        FprEN 1992-1-1:2023 (E) art 8.2.2 (2) - Formula (8.28)

        Parameters
        ----------
        a_sl : MM2
            [$A_{sl}$] Effective area of tensile reinforcement at the distance [$d$] beyond the section considered,
            see Figure 8.7 [$mm^2$].
        b_w : MM
            [$b_w$] Width of the cross-section of linear members. The width [$b_w$] for cross-sections with variable width
            and for circular cross-sections is defined in 8.2.3(9) [$mm$].
        d : MM
            [$d$] Effective depth [$d_{nom}$]. The value [$d$] may be refined according to 8.2.2(3) and 8.2.2(4) for
            non-slender members and members with axial force [$mm$].
        """
        super().__init__()
        self.a_sl = a_sl
        self.b_w = b_w
        self.d = d

    @staticmethod
    def _evaluate(a_sl: MM2, b_w: MM, d: MM) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_sl=a_sl)
        raise_if_less_or_equal_to_zero(b_w=b_w, d=d)

        return a_sl / (b_w * d)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.28."""
        _equation: str = r"\frac{A_{sl}}{b_w \cdot d}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"A_{sl}": f"{self.a_sl:.{n}f}",
                r"b_w": f"{self.b_w:.{n}f}",
                r"\cdot d": rf"\cdot {self.d:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"A_{sl}": rf"{self.a_sl:.{n}f} \ mm^2",
                r"b_w": rf"{self.b_w:.{n}f} \ mm",
                r"\cdot d": rf"\cdot {self.d:.{n}f} \ mm",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\rho_l",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )

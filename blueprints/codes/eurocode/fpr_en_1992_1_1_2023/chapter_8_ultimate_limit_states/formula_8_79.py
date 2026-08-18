"""Formula 8.79 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MM2, MPA, NMM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot79TorsionalShearStressInWall(Formula):
    r"""Class representing formula 8.79 for the calculation of the torsional shear stress in a wall element of a
    section subject to a torsional moment.

    It applies to closed thin-walled sections and solid sections, for which 8.3.2(1) allows warping torsion to be
    ignored. Solid sections are first modelled as equivalent thin-walled sections according to 8.3.1(2).

    The stress follows from the Bredt shear flow, so it is constant over the effective thickness of the wall and
    the same for every wall of a section with a constant effective thickness.
    """

    label = "8.79"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        t_ed: NMM,
        a_k: MM2,
        t_eff_i: MM,
    ) -> None:
        r"""[$\tau_{t,i}$] Torsional shear stress in wall [$i$] [$MPa$].

        FprEN 1992-1-1:2023 (E) art. 8.3.2(2) - Formula (8.79)

        Parameters
        ----------
        t_ed : NMM
            [$T_{Ed}$] Torsional moment the section is subject to. The standard introduces this symbol in the text
            of 8.3.2(2) and not in the "where" list below the formula. Pass its magnitude, so that the resulting
            shear stress is the one to be compared with the torsional resistance [$Nmm$].
        a_k : MM2
            [$A_k$] Area enclosed by the centre-lines of the connecting walls, including inner hollow areas
            [$mm^2$].
        t_eff_i : MM
            [$t_{eff,i}$] Effective wall thickness. It may be taken as [$A/u$], but should not be taken as less
            than twice the distance between the outer concrete surface and the centre of the longitudinal
            reinforcement. For hollow sections the actual thickness is an upper limit. Here [$A$] is the total area
            of the cross-section, including inner hollow areas, and [$u$] is the outer perimeter of the
            cross-section [$mm$].
        """
        super().__init__()
        self.t_ed = t_ed
        self.a_k = a_k
        self.t_eff_i = t_eff_i

    @staticmethod
    def _evaluate(
        t_ed: NMM,
        a_k: MM2,
        t_eff_i: MM,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(t_ed=t_ed)
        raise_if_less_or_equal_to_zero(a_k=a_k, t_eff_i=t_eff_i)

        return t_ed / (2 * a_k * t_eff_i)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.79."""
        _equation: str = r"\frac{T_{Ed}}{2 \cdot A_k \cdot t_{eff,i}}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"T_{Ed}": f"{self.t_ed:.{n}f}",
                r"A_k": f"{self.a_k:.{n}f}",
                r"t_{eff,i}": f"{self.t_eff_i:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"T_{Ed}": rf"{self.t_ed:.{n}f} \ Nmm",
                r"A_k": rf"{self.a_k:.{n}f} \ mm^2",
                r"t_{eff,i}": rf"{self.t_eff_i:.{n}f} \ mm",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"\tau_{t,i}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )

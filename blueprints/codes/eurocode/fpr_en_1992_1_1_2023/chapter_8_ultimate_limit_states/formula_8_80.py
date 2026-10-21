"""Formula 8.80 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MPA, N
from blueprints.validations import raise_if_negative


class Form8Dot80ShearForceInWallDueToTorsion(Formula):
    r"""Class representing formula 8.80 for the calculation of the shear force in a wall element due to torsion.

    It turns the torsional shear stress of Formula (8.79) into the shear force acting on the wall, which is what
    the shear rules of 8.2 need in order to design that wall.

    The standard prints no "where" list under this formula. The symbols come from Formula (8.79) and from
    Figure 8.16.
    """

    label = "8.80"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        tau_t_i: MPA,
        t_eff_i: MM,
        z_i: MM,
    ) -> None:
        r"""[$V_{Ed,i}$] Shear force in wall element [$i$] due to torsion [$N$].

        FprEN 1992-1-1:2023 (E) art. 8.3.2(3) - Formula (8.80)

        Parameters
        ----------
        tau_t_i : MPA
            [$\tau_{t,i}$] Torsional shear stress in wall [$i$], refer to Formula (8.79) [$MPa$].
        t_eff_i : MM
            [$t_{eff,i}$] Effective wall thickness, refer to Formula (8.79) [$mm$].
        z_i : MM
            [$z_i$] Side length of wall element [$i$], measured along the centre-line of that wall between the
            intersections with the centre-lines of the adjacent walls, see Figure 8.16 [$mm$].
        """
        super().__init__()
        self.tau_t_i = tau_t_i
        self.t_eff_i = t_eff_i
        self.z_i = z_i

    @staticmethod
    def _evaluate(
        tau_t_i: MPA,
        t_eff_i: MM,
        z_i: MM,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(tau_t_i=tau_t_i, t_eff_i=t_eff_i, z_i=z_i)

        return tau_t_i * t_eff_i * z_i

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.80."""
        _equation: str = r"\tau_{t,i} \cdot t_{eff,i} \cdot z_i"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{t,i}": f"{self.tau_t_i:.{n}f}",
                r"t_{eff,i}": f"{self.t_eff_i:.{n}f}",
                r"z_i": f"{self.z_i:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{t,i}": rf"{self.tau_t_i:.{n}f} \ MPa",
                r"t_{eff,i}": rf"{self.t_eff_i:.{n}f} \ mm",
                r"z_i": rf"{self.z_i:.{n}f} \ mm",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"V_{Ed,i}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="N",
        )

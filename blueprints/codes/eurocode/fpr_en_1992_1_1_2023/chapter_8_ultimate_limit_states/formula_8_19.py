"""Formula 8.19 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MPA, N_MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot19AverageShearStressPlanarMembers(Formula):
    """Class representing formula 8.19 for the calculation of the average shear stress over the cross-section
    of planar members in regions without geometric discontinuities.
    """

    label = "8.19"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, v_ed: N_MM, z: MM) -> None:
        r"""[$\tau_{Ed}$] Average shear stress over the cross-section area in regions of members without geometric discontinuities [$MPa$].

        FprEN 1992-1-1:2023 (E) art 8.2.1 (3) - Formula (8.19)

        Parameters
        ----------
        v_ed : N_MM
            [$v_{Ed}$] Design shear force per unit width in planar members [$N/mm$]. Note that this is the lower case
            [$v_{Ed}$] of planar members, not the shear force [$V_{Ed}$] in [$N$] used in Formula (8.18).
        z : MM
            [$z$] Lever arm for the shear stress calculation defined as [$z = 0.9 \cdot d$], where [$d$] refers to the
            centroid of tensile reinforcement [$mm$].
        """
        super().__init__()
        self.v_ed = v_ed
        self.z = z

    @staticmethod
    def _evaluate(v_ed: N_MM, z: MM) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(v_ed=v_ed)
        raise_if_less_or_equal_to_zero(z=z)
        return v_ed / z

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.19."""
        _equation: str = r"\frac{v_{Ed}}{z}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={r"v_{Ed}": f"{self.v_ed:.{n}f}", r"z": f"{self.z:.{n}f}"},
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"v_{Ed}": rf"{self.v_ed:.{n}f} \ N/mm",
                r"z": rf"{self.z:.{n}f} \ mm",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\tau_{Ed}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )

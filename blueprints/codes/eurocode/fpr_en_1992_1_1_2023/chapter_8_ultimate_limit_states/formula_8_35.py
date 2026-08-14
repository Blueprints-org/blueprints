"""Formula 8.35 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot35MaximumShearStressResistance(Formula):
    """Class representing formula 8.35 for the calculation of the upper bound of the shear stress resistance
    used in Formula (8.32).
    """

    label = "8.35"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, tau_rdc_0: MPA, a_cs_0: MM, d: MM) -> None:
        r"""[$\tau_{Rdc,max}$] Maximum shear stress resistance [$MPa$].

        FprEN 1992-1-1:2023 (E) art 8.2.2 (5) - Formula (8.35)

        The printed upper bound of [$2.7 \cdot \tau_{Rdc,0}$] is implemented as a minimum.

        Parameters
        ----------
        tau_rdc_0 : MPA
            [$\tau_{Rdc,0}$] Design value of the shear stress resistance without the effect of compressive
            normal forces according to Formula (8.33), see Form8Dot33ShearStressResistanceWithoutAxialForce [$MPa$].
        a_cs_0 : MM
            [$a_{cs,0}$] Effective shear span determined according to Formula (8.30), without considering in
            [$M_{Ed}$] and [$V_{Ed}$] the effect of prestressing or external load that produces the compressive
            axial force [$mm$].
        d : MM
            [$d$] Effective depth [$mm$].
        """
        super().__init__()
        self.tau_rdc_0 = tau_rdc_0
        self.a_cs_0 = a_cs_0
        self.d = d

    @staticmethod
    def _evaluate(tau_rdc_0: MPA, a_cs_0: MM, d: MM) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        # Zero is refused for all of these. For the ones that sit in a denominator that is a reading of the
        # standard. For a_cs_0 it is also a reading, one step removed: Formula (8.30) defines the effective
        # shear span as at least the effective depth, so it cannot be zero. For the rest it is an addition made
        # here, so that the same quantity is not admitted in one formula of this clause and refused in the next.
        raise_if_negative(tau_rdc_0=tau_rdc_0)
        raise_if_less_or_equal_to_zero(a_cs_0=a_cs_0, d=d)

        return min(2.15 * tau_rdc_0 * (a_cs_0 / d) ** (1 / 6), 2.7 * tau_rdc_0)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.35."""
        _equation: str = (
            r"\min\left(2.15 \cdot \tau_{Rdc,0} \cdot \left(\frac{a_{cs,0}}{d}\right)^{\frac{1}{6}}, "
            r"2.7 \cdot \tau_{Rdc,0}\right)"
        )
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{Rdc,0}": f"{self.tau_rdc_0:.{n}f}",
                r"a_{cs,0}": f"{self.a_cs_0:.{n}f}",
                r"{d}": "{" + f"{self.d:.{n}f}" + "}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{Rdc,0}": rf"{self.tau_rdc_0:.{n}f} \ MPa",
                r"a_{cs,0}": rf"{self.a_cs_0:.{n}f} \ mm",
                r"{d}": "{" + rf"{self.d:.{n}f} \ mm" + "}",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\tau_{Rdc,max}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )

"""Formula 8.57 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, DIMENSIONLESS, MM, MPA, NMM
from blueprints.utils.math_helpers import cot
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot57AdditionalBendingMoment(Formula):
    """Class representing formula 8.57 for the calculation of the additional bending moment to be added to the
    design bending moment in the support region.
    """

    label = "8.57"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        tau_ed: MPA,
        rho_w: DIMENSIONLESS,
        f_ywd: MPA,
        theta: DEG,
        z: MM,
        b_w: MM,
        a: MM,
        x: MM,
    ) -> None:
        r"""[$\Delta M_{Ed}$] Additional bending moment to be added to [$M_{Ed}$] for use in Formulae (8.51)
        and (8.52) [$Nmm$].

        FprEN 1992-1-1:2023 (E) art 8.2.3 (12) - Formula (8.57)

        The standard adds this moment in addition to the axial tensile force [$N_{Vd}$] due to shear according
        to Formula (8.50). Note that the result carries a sign: it is negative where the investigated
        cross-section lies beyond half the distance to the concentrated force, and also where the average shear
        stress falls below the contribution of the shear reinforcement. Neither case is bounded by the standard,
        so neither is clamped here.

        Parameters
        ----------
        tau_ed : MPA
            [$\tau_{Ed}$] Average shear stress over the cross-section according to Formula (8.18) [$MPa$].
        rho_w : DIMENSIONLESS
            [$\rho_w$] Shear reinforcement ratio according to Formula (8.43) [$-$].
        f_ywd : MPA
            [$f_{ywd}$] Design value of the yield strength of the shear reinforcement. For compression field
            inclinations with [$\cot\theta < 1$] the standard requires it to be replaced by the stress
            [$\sigma_{swd}$] according to Formula (8.56), see Form8Dot56StressInShearReinforcement. That stress
            carries no printed lower bound and is negative over much of its range, so this argument is not
            guarded against negative values [$MPa$].
        theta : DEG
            [$\theta$] Inclination of the compression field in the web [$degrees$].
        z : MM
            [$z$] Lever arm for the shear calculation, which may be assumed as in 8.2.1(3) [$mm$].
        b_w : MM
            [$b_w$] Width of the web of the cross-section [$mm$].
        a : MM
            [$a$] Distance between the axis of the support and the concentrated force, see Figure 8.11 a). This
            is not the same quantity as the shear span [$a_v = z \cdot \cot\beta_{incl}$] of Formula (8.55),
            which the two share only where the load happens to sit at that distance [$mm$].
        x : MM
            [$x$] Distance between the support and the investigated cross-section [$mm$].
        """
        super().__init__()
        self.tau_ed = tau_ed
        self.rho_w = rho_w
        self.f_ywd = f_ywd
        self.theta = theta
        self.z = z
        self.b_w = b_w
        self.a = a
        self.x = x

    @staticmethod
    def _evaluate(
        tau_ed: MPA,
        rho_w: DIMENSIONLESS,
        f_ywd: MPA,
        theta: DEG,
        z: MM,
        b_w: MM,
        a: MM,
        x: MM,
    ) -> NMM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(tau_ed=tau_ed, rho_w=rho_w, z=z, b_w=b_w, a=a, x=x)
        raise_if_less_or_equal_to_zero(theta=theta)

        return (tau_ed - rho_w * f_ywd * cot(theta)) * z * b_w * (a / 2 - x)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.57."""
        _equation: str = (
            r"\left(\tau_{Ed} - \rho_w \cdot f_{ywd} \cdot \cot(\theta)\right) "
            r"\cdot z \cdot b_w \cdot \left(\frac{a}{2} - x\right)"
        )
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{Ed}": f"{self.tau_ed:.{n}f}",
                r"\rho_w": f"{self.rho_w:.{n}f}",
                r"f_{ywd}": f"{self.f_ywd:.{n}f}",
                r"\theta": f"{self.theta:.{n}f}",
                r"\cdot z \cdot": rf"\cdot {self.z:.{n}f} \cdot",
                r"b_w": f"{self.b_w:.{n}f}",
                r"\frac{a}{2}": r"\frac{" + f"{self.a:.{n}f}" + r"}{2}",
                r"- x\right)": rf"- {self.x:.{n}f}\right)",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{Ed}": rf"{self.tau_ed:.{n}f} \ MPa",
                r"\rho_w": f"{self.rho_w:.{n}f}",
                r"f_{ywd}": rf"{self.f_ywd:.{n}f} \ MPa",
                r"\theta": rf"{self.theta:.{n}f} ^\circ",
                r"\cdot z \cdot": rf"\cdot {self.z:.{n}f} \ mm \cdot",
                r"b_w": rf"{self.b_w:.{n}f} \ mm",
                r"\frac{a}{2}": r"\frac{" + rf"{self.a:.{n}f} \ mm" + r"}{2}",
                r"- x\right)": rf"- {self.x:.{n}f} \ mm\right)",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\Delta M_{Ed}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="Nmm",
        )

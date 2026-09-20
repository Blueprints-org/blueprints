"""Formula 8.104 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form8Dot104PunchingShearStressResistanceWithShearReinforcement(Formula):
    r"""Class representing formula 8.104 for the calculation of the shear stress resistance of planar members
    with shear reinforcement subjected to concentrated forces.

    The standard writes this as an expression bounded from below by [$\rho_w \cdot f_{ywd}$], which is
    implemented as the maximum of the two.
    """

    label = "8.104"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        eta_c: DIMENSIONLESS,
        tau_rd_c: MPA,
        eta_s: DIMENSIONLESS,
        rho_w: DIMENSIONLESS,
        f_ywd: MPA,
    ) -> None:
        r"""[$\tau_{Rd,cs}$] Shear stress resistance of planar members with shear reinforcement subjected to
        concentrated forces [$MPa$].

        FprEN 1992-1-1:2023 (E) art. 8.4.4(1) - Formula (8.104)

        Parameters
        ----------
        eta_c : DIMENSIONLESS
            [$\eta_c$] Strength reduction coefficient for shear resistance [$\tau_{Rd,c}$] according to
            Formula (8.105), see Form8Dot105StrengthReductionCoefficientForShearResistance [$-$].
        tau_rd_c : MPA
            [$\tau_{Rd,c}$] Punching shear stress resistance of slabs without shear reinforcement according to
            Formula (8.94) [$MPa$].
        eta_s : DIMENSIONLESS
            [$\eta_s$] Strength reduction coefficient for the contribution of the shear reinforcement
            according to Formula (8.106), see Form8Dot106StrengthReductionCoefficientForShearReinforcement
            [$-$].
        rho_w : DIMENSIONLESS
            [$\rho_w$] Shear reinforcement ratio at the investigated control perimeter according to
            Formula (8.107), see Form8Dot107ShearReinforcementRatio [$-$].
        f_ywd : MPA
            [$f_{ywd}$] Design yield strength of the shear reinforcement [$MPa$].
        """
        super().__init__()
        self.eta_c = eta_c
        self.tau_rd_c = tau_rd_c
        self.eta_s = eta_s
        self.rho_w = rho_w
        self.f_ywd = f_ywd

    @staticmethod
    def _evaluate(
        eta_c: DIMENSIONLESS,
        tau_rd_c: MPA,
        eta_s: DIMENSIONLESS,
        rho_w: DIMENSIONLESS,
        f_ywd: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(eta_c=eta_c, tau_rd_c=tau_rd_c, eta_s=eta_s, rho_w=rho_w, f_ywd=f_ywd)

        return max(eta_c * tau_rd_c + eta_s * rho_w * f_ywd, rho_w * f_ywd)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.104."""
        _equation: str = r"\max\left(\eta_c \cdot \tau_{Rd,c} + \eta_s \cdot \rho_w \cdot f_{ywd}, \rho_w \cdot f_{ywd}\right)"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\eta_c": f"{self.eta_c:.{n}f}",
                r"\tau_{Rd,c}": f"{self.tau_rd_c:.{n}f}",
                r"\eta_s": f"{self.eta_s:.{n}f}",
                r"\rho_w": f"{self.rho_w:.{n}f}",
                r"f_{ywd}": f"{self.f_ywd:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\eta_c": f"{self.eta_c:.{n}f}",
                r"\tau_{Rd,c}": rf"{self.tau_rd_c:.{n}f} \ MPa",
                r"\eta_s": f"{self.eta_s:.{n}f}",
                r"\rho_w": f"{self.rho_w:.{n}f}",
                r"f_{ywd}": rf"{self.f_ywd:.{n}f} \ MPa",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\tau_{Rd,cs}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )

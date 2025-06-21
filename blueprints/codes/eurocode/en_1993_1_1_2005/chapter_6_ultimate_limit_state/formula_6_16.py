"""Formula 6.16 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM2, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot16CheckFlangeWithFastenerHoles(Formula):
    r"""Class representing formula 6.16 for the test of the stresses where there are fastener holes in the tension flange."""

    label = "6.16"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        a_f_net: MM2,
        f_u: MPA,
        gamma_m2: DIMENSIONLESS,
        a_f: MM2,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
    ) -> None:
        r"""Test the stresses where there are fastener holes in the tension flange.

        EN 1993-1-1:2005 art.6.2.5(4) - Formula (6.16)

        Parameters
        ----------
        a_f_net : MM2
            [$A_{f,net}$] Net area of the flange with fastener holes [mm^2].
        f_u : MPA
            [$f_{u}$] Ultimate tensile strength of the material [MPa].
        gamma_m2 : DIMENSIONLESS
            [$\gamma_{M2}$] Partial safety factor for ultimate limit state [-].
        a_f : MM2
            [$A_{f}$] Gross area of the flange [mm^2].
        f_y : MPA
            [$f_{y}$] Yield strength of the material [MPa].
        gamma_m0 : DIMENSIONLESS
            [$\gamma_{M0}$] Partial safety factor for yield strength [-].
        """
        super().__init__()
        self.a_f_net = a_f_net
        self.f_u = f_u
        self.gamma_m2 = gamma_m2
        self.a_f = a_f
        self.f_y = f_y
        self.gamma_m0 = gamma_m0

    @staticmethod
    def _evaluate(
        a_f_net: MM2,
        f_u: MPA,
        gamma_m2: DIMENSIONLESS,
        a_f: MM2,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(gamma_m2=gamma_m2, gamma_m0=gamma_m0)
        raise_if_negative(a_f_net=a_f_net, f_u=f_u, a_f=a_f, f_y=f_y)

        return (a_f_net * 0.9 * f_u / gamma_m2) >= (a_f * f_y / gamma_m0)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.16."""
        _equation: str = r"\left( \frac{A_{f,net} \cdot 0.9 \cdot f_{u}}{\gamma_{M2}} \geq \frac{A_{f} \cdot f_{y}}{\gamma_{M0}} \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A_{f,net}": f"{self.a_f_net:.{n}f}",
                r"f_{u}": f"{self.f_u:.{n}f}",
                r"\gamma_{M2}": f"{self.gamma_m2:.{n}f}",
                r"A_{f}": f"{self.a_f:.{n}f}",
                r"f_{y}": f"{self.f_y:.{n}f}",
                r"\gamma_{M0}": f"{self.gamma_m0:.{n}f}",
            },
            False,
        )

        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="\\to",
            unit="",
        )

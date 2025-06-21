"""Formula 6.7 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot7DesignUltimateResistanceNetCrossSection(Formula):
    r"""Class representing formula 6.7 for the calculation of [$N_{t,Rd}$]."""

    label = "6.7"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        a_net: MM2,
        f_u: MPA,
        gamma_m2: DIMENSIONLESS,
    ) -> None:
        r"""[$N_{u,Rd}$] Calculation of the design tension resistance [$N$].

        EN 1993-1-1:2005 art.6.2.3(2) - Formula (6.7)

        Parameters
        ----------
        a_net : MM2
            [$A_{net}$] Net cross-sectional area at holes for fasteners [$mm^2$].
        f_u : MPA
            [$f_u$] Ultimate tensile strength of the material [$N/mm^2$].
        gamma_m2 : DIMENSIONLESS
            [$\gamma_{M2}$] Partial safety factor for resistance of cross-sections in tension to fracture.
        """
        super().__init__()
        self.a_net = a_net
        self.f_u = f_u
        self.gamma_m2 = gamma_m2

    @staticmethod
    def _evaluate(
        a_net: MM2,
        f_u: MPA,
        gamma_m2: DIMENSIONLESS,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_net=a_net, f_u=f_u)
        raise_if_less_or_equal_to_zero(gamma_m2=gamma_m2)

        return 0.9 * a_net * f_u / gamma_m2

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.7."""
        _equation: str = r"0.9 \cdot \frac{A_{net} \cdot f_u}{\gamma_{M2}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A_{net}": f"{self.a_net:.{n}f}",
                r"f_u": f"{self.f_u:.{n}f}",
                r"\gamma_{M2}": f"{self.gamma_m2:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"N_{u,Rd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="N",
        )

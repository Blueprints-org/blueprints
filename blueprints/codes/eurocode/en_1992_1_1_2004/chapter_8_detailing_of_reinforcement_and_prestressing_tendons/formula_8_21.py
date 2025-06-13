"""Formula 8.21 from EN 1992-1-1:2004: Chapter 8: Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MM, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot21AnchorageLength(Formula):
    r"""Class representing formula 8.21 for the calculation of anchorage length [$l_{bpd}$] [$mm$].

    EN 1992-1-1:2004 art.8.10.2.3(4) - Formula (8.21)

    Parameters
    ----------
    l_pt2 : MM
        [$l_{pt2}$] is the upper design value of transmission length, see 8.10.2.2 (3) [$mm$].
    alpha_2 : DIMENSIONLESS
        [$\alpha_{2}$] as defined in 8.10.2.2 (2) [$-$].
    diameter : MM
        [$Ø$] Diameter of the tendon [$mm$].
    sigma_pd : MPA
        [$\sigma_{pd}$] Is the tendon stress corresponding to the force described in art.8.10.2.3(1) [$MPa$].
    sigma_pminf : MPA
        [$\sigma_{pm\infty}$] is the prestress after all losses [$MPa$].
    f_bpd : MPA
        [$f_{bpd}$] Bond strength for anchorage in the ultimate limit state [$MPa$].
    """

    label = "8.21"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        l_pt2: MM,
        alpha_2: DIMENSIONLESS,
        diameter: MM,
        sigma_pd: MPA,
        sigma_pminf: MPA,
        f_bpd: MPA,
    ) -> None:
        super().__init__()
        self.l_pt2 = l_pt2
        self.alpha_2 = alpha_2
        self.diameter = diameter
        self.sigma_pd = sigma_pd
        self.sigma_pminf = sigma_pminf
        self.f_bpd = f_bpd

    @staticmethod
    def _evaluate(l_pt2: MM, alpha_2: DIMENSIONLESS, diameter: MM, sigma_pd: MPA, sigma_pminf: MPA, f_bpd: MPA) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(l_pt2=l_pt2, alpha_2=alpha_2, diameter=diameter, sigma_pd=sigma_pd, sigma_pminf=sigma_pminf)
        raise_if_less_or_equal_to_zero(f_bpd=f_bpd)
        return l_pt2 + alpha_2 * diameter * (sigma_pd - sigma_pminf) / f_bpd

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.21."""
        return LatexFormula(
            return_symbol=r"l_{bpd}",
            result=f"{self:.{n}f}",
            equation=r"l_{pt2} + \alpha_{2} \cdot Ø \cdot \frac{\sigma_{pd} - \sigma_{pm\infty}}{f_{bpd}}",
            numeric_equation=rf"{self.l_pt2:.{n}f} + {self.alpha_2:.{n}f} \cdot {self.diameter:.{n}f} \cdot \frac{{{self.sigma_pd:.{n}f} - "
            rf"{self.sigma_pminf:.{n}f}}}{{{self.f_bpd:.{n}f}}}",
            comparison_operator_label="=",
        )

"""Formula 6.4 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MM, MM3, MM4, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot4ShearResistance(Formula):
    r"""Class representing formula 6.4 for the calculation of the shear resistance in regions uncracked in bending, [$V_{Rd,c}$]."""

    label = "6.4"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        i: MM4,
        b_w: MM,
        s: MM3,
        f_ctd: MPA,
        alpha_l: DIMENSIONLESS,
        sigma_cp: MPA,
    ) -> None:
        r"""[$V_{Rd,c}$] Shear resistance in regions uncracked in bending [$kN$].

        NEN-EN 1992-1-1+C2:2011 art.6.2.2(2) - Formula (6.4)

        Parameters
        ----------
        i : MM4
            [$I$] Second moment of area [$mm^4$].
        b_w : MM
            [$b_w$] Width of the cross-section at the centroidal axis, see equation 6.16 and 6.17 [$mm$].
        s : MM3
            [$S$] First moment of area above and about the centroidal axis [$mm^3$].
        f_ctd : MPA
            [$f_{ctd}$] Design tensile strength of concrete [$MPa$].
        alpha_l : DIMENSIONLESS
            [$\alpha_l$] [$l_x / l_{pt2} \leq 1.0$] for pretensioned tendons, [$1.0$] for other types of prestressing [$-$].
        sigma_cp : MPA
            [$\sigma_{cp}$] Concrete compressive stress at the centroidal axis due to axial loading and/or prestressing [$MPa$].
        """
        super().__init__()
        self.i = i
        self.b_w = b_w
        self.s = s
        self.f_ctd = f_ctd
        self.alpha_l = alpha_l
        self.sigma_cp = sigma_cp

    @staticmethod
    def _evaluate(
        i: MM4,
        b_w: MM,
        s: MM3,
        f_ctd: MPA,
        alpha_l: DIMENSIONLESS,
        sigma_cp: MPA,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            i=i,
            b_w=b_w,
            s=s,
            f_ctd=f_ctd,
            alpha_l=alpha_l,
            sigma_cp=sigma_cp,
        )
        raise_if_less_or_equal_to_zero(s=s)

        return i * b_w / s * (f_ctd**2 + alpha_l * sigma_cp * f_ctd) ** 0.5

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.4."""
        return LatexFormula(
            return_symbol=r"V_{Rd,c}",
            result=f"{self:.3f}",
            equation=r"\frac{I \cdot b_w}{S} \cdot \sqrt{(f_{ctd})^2 + \alpha_l \cdot \sigma_{cp} \cdot f_{ctd}}",
            numeric_equation=rf"\frac{{{self.i:.3f} \cdot {self.b_w:.3f}}}{{{self.s:.3f}}} \cdot "
            rf"\sqrt{{({self.f_ctd:.3f})^2 + {self.alpha_l:.3f} \cdot {self.sigma_cp:.3f} \cdot {self.f_ctd:.3f}}}",
            comparison_operator_label="=",
            unit="N",
        )

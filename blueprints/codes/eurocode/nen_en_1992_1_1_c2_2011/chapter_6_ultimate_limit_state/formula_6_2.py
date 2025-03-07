"""Formula 6.2a from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MM, MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot2ShearResistance(Formula):
    r"""Class representing formula 6.2a for the calculation of the design value for the shear resistance, [$V_{Rd,c}$]."""

    label = "6.2ab"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        c_rd_c: DIMENSIONLESS,
        k: DIMENSIONLESS,
        rho_l: DIMENSIONLESS,
        f_ck: MPA,
        k_1: DIMENSIONLESS,
        sigma_cp: MPA,
        b_w: MM,
        d: MM,
        v_min: N,
    ) -> None:
        r"""[$V_{Rd,c}$] Design value for the shear resistance [$kN$].

        NEN-EN 1992-1-1+C2:2011 art.6.2.2(1) - Formula (6.2a)

        Parameters
        ----------
        c_rd_c : DIMENSIONLESS
            [$C_{Rd,c}$] Coefficient for shear strength [$-$].
        k : DIMENSIONLESS
            [$k$] Size effect factor [$-$].
        rho_l : DIMENSIONLESS
            [$\rho_l$] Longitudinal reinforcement ratio [$-$].
        f_ck : MPA
            [$f_{ck}$] Characteristic compressive strength of concrete [$MPa$].
        k_1 : DIMENSIONLESS
            [$k_1$] Coefficient for concrete [$-$].
        sigma_cp : MPA
            [$\sigma_{cp}$] Compressive stress in the concrete [$MPa$].
        b_w : MM
            [$b_w$] Width of the web [$mm$].
        d : MM
            [$d$] Effective depth [$mm$].
        v_min : N
            [$v_{min}$] shear capacity without rebar [$N$].
        """
        super().__init__()
        self.c_rd_c = c_rd_c
        self.k = k
        self.rho_l = rho_l
        self.f_ck = f_ck
        self.k_1 = k_1
        self.sigma_cp = sigma_cp
        self.b_w = b_w
        self.d = d
        self.v_min = v_min

    @staticmethod
    def _evaluate(
        c_rd_c: DIMENSIONLESS,
        k: DIMENSIONLESS,
        rho_l: DIMENSIONLESS,
        f_ck: MPA,
        k_1: DIMENSIONLESS,
        sigma_cp: MPA,
        b_w: MM,
        d: MM,
        v_min: N,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            c_rd_c=c_rd_c,
            k=k,
            rho_l=rho_l,
            f_ck=f_ck,
            k_1=k_1,
            sigma_cp=sigma_cp,
            b_w=b_w,
            d=d,
            v_min=v_min,
        )
        result_62a = (c_rd_c * k * (100 * rho_l * f_ck) ** (1 / 3) + k_1 * sigma_cp) * b_w * d
        result_62b = (v_min + k_1 * sigma_cp) * b_w * d

        return max(result_62a, result_62b)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.2."""
        return LatexFormula(
            return_symbol=r"V_{Rd,c}",
            result=f"{self:.3f}",
            equation=r"\max(C_{Rd,c} \cdot k \cdot \left(100 \cdot \rho_l \cdot f_{ck}\right)^{1/3} + k_1 \cdot "
            r"\sigma_{cp}, v_{min} + k_1 \cdot \sigma_{cp}) \cdot b_w \cdot d",
            numeric_equation=rf"\max({self.c_rd_c:.3f} \cdot {self.k:.3f} \cdot \left(100 \cdot {self.rho_l:.3f} "
            rf"\cdot {self.f_ck:.3f}\right)^{{1/3}} + {self.k_1:.3f} \cdot {self.sigma_cp:.3f}, {self.v_min:.3f} + "
            rf"{self.k_1:.3f} \cdot {self.sigma_cp:.3f}) \cdot {self.b_w:.3f} \cdot {self.d:.3f}",
            comparison_operator_label="=",
            unit="N",
        )


class Form6Dot2aSub1ThicknessFactor(Formula):
    r"""Class representing formula 6.2a for k, the thickness factor, [$k$]."""

    label = "6.2aSub1"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        d: MM,
    ) -> None:
        r"""[$k$] factor to take thickness into account [$kN$].

        NEN-EN 1992-1-1+C2:2011 art.6.2.2(1) - Formula (6.2a)

        Parameters
        ----------
        d : MM
            [$d$] Effective depth [$mm$].
        """
        super().__init__()
        self.d = d

    @staticmethod
    def _evaluate(
        d: MM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(d=d)

        return min(1 + (200 / d) ** 0.5, 2.0)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.2a Sub 1."""
        return LatexFormula(
            return_symbol=r"k",
            result=f"{self:.3f}",
            equation=r"\min(1 + \sqrt{\frac{200}{d}}, 2.0)",
            numeric_equation=rf"\min(1 + \sqrt{{\frac{{200}}{{{self.d:.3f}}}}}, 2.0)",
            comparison_operator_label="=",
            unit="-",
        )


class Form6Dot2aSub2RebarRatio(Formula):
    r"""Class representing formula 6.2a for the tensile rebar ratio, [$\rho_l$]."""

    label = "6.2aSub2"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        a_sl: MM2,
        b_w: MM,
        d: MM,
    ) -> None:
        r"""[$\rho_l$] Tensile rebar ratio [$-$].

        NEN-EN 1992-1-1+C2:2011 art.6.2.2(1) - Formula (6.2a)

        Parameters
        ----------
        a_sl : MM2
            [$A_{sl}$] Area of tensile reinforcement [$mm^2$].
        b_w : MM
            [$b_w$] Width of the web [$mm$].
        d : MM
            [$d$] Effective depth [$mm$].
        """
        super().__init__()
        self.A_sl = a_sl
        self.b_w = b_w
        self.d = d

    @staticmethod
    def _evaluate(
        a_sl: MM2,
        b_w: MM,
        d: MM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_sl=a_sl)
        raise_if_less_or_equal_to_zero(b_w=b_w, d=d)

        return min(a_sl / (b_w * d), 0.02)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.2a Sub 2."""
        return LatexFormula(
            return_symbol=r"\rho_l",
            result=f"{self:.3f}",
            equation=r"\min( \frac{A_{sl}}{b_w \cdot d}, 0.02)",
            numeric_equation=rf"\min( \frac{{{self.A_sl:.3f}}}{{{self.b_w:.3f} \cdot {self.d:.3f}}}, 0.02)",
            comparison_operator_label="=",
            unit="-",
        )

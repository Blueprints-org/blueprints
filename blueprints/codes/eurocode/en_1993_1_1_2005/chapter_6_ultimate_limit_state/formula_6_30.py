"""Formula 6.30 from NEN-EN 1993-1-1+A1:2016: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM3, MPA, NMM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot30ReducedPlasticResistanceMoment(Formula):
    r"""Class representing formula 6.30 for the calculation of [$M_{y,V,Rd}$]."""

    label = "6.30"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        w_pl_y: MM3,
        rho: DIMENSIONLESS,
        h_w: MM,
        t_w: MM,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
        m_y_c_rd: NMM,
    ) -> None:
        r"""[$M_{y,V,Rd}$] Reduced design plastic resistance moment [$Nmm$].

        NEN-EN 1993-1-1+A1:2016 art.6.2.8(5) - Formula (6.30)

        Parameters
        ----------
        w_pl_y : MM3
            [$W_{pl,y}$] Plastic section modulus about the y-axis [$mm^3$].
        rho : DIMENSIONLESS
            [$\rho$] Shear force ratio (see 6.2.8 (3) or equation 6.29 (rho)) [-].
        h_w : MM
            [$h_w$] Web height [$mm$].
        t_w : MM
            [$t_w$] Web thickness [$mm$].
        f_y : MPA
            [$f_y$] Yield strength of the material [$MPa$].
        gamma_m0 : DIMENSIONLESS
            [$\gamma_{M0}$] Partial safety factor for resistance of cross-sections [-].
        m_y_c_rd : NMM
            [$M_{y,c,Rd}$] Design resistance moment, obtained from 6.2.5(2) [$Nmm$].
        """
        super().__init__()
        self.w_pl_y = w_pl_y
        self.rho = rho
        self.h_w = h_w
        self.t_w = t_w
        self.f_y = f_y
        self.gamma_m0 = gamma_m0
        self.m_y_c_rd = m_y_c_rd

    @staticmethod
    def _evaluate(
        w_pl_y: MM3,
        rho: DIMENSIONLESS,
        h_w: MM,
        t_w: MM,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
        m_y_c_rd: NMM,
    ) -> NMM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(w_pl_y=w_pl_y, rho=rho, h_w=h_w, f_y=f_y, m_y_c_rd=m_y_c_rd)
        raise_if_less_or_equal_to_zero(gamma_m0=gamma_m0, t_w=t_w)

        a_w = h_w * t_w
        m_y_v_rd = (w_pl_y - (rho * a_w**2) / (4 * t_w)) * f_y / gamma_m0
        return min(m_y_v_rd, m_y_c_rd)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.30."""
        _equation: str = (
            r"\min\left(\frac{\left[W_{pl,y} - \frac{\rho \cdot (h_w \cdot t_w)^2}{4 \cdot t_w}\right] \cdot f_y}{\gamma_{M0}}, M_{y,c,Rd}\right)"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"W_{pl,y}": f"{self.w_pl_y:.{n}f}",
                r"\rho": f"{self.rho:.{n}f}",
                r"h_w": f"{self.h_w:.{n}f}",
                r"t_w": f"{self.t_w:.{n}f}",
                r"f_y": f"{self.f_y:.{n}f}",
                r"\gamma_{M0}": f"{self.gamma_m0:.{n}f}",
                r"M_{y,c,Rd}": f"{self.m_y_c_rd:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"W_{pl,y}": rf"{self.w_pl_y:.{n}f} \ mm^3",
                r"\rho": rf"{self.rho:.{n}f}",
                r"h_w": rf"{self.h_w:.{n}f} \ mm",
                r"t_w": rf"{self.t_w:.{n}f} \ mm",
                r"f_y": rf"{self.f_y:.{n}f} \ MPa",
                r"\gamma_{M0}": rf"{self.gamma_m0:.{n}f}",
                r"M_{y,c,Rd}": rf"{self.m_y_c_rd:.{n}f} \ Nmm",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"M_{y,V,Rd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="Nmm",
        )

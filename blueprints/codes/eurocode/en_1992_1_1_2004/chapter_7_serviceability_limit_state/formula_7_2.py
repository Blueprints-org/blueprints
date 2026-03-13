"""Formula 7.2 and 7.2sub1 from EN 1992-1-1:2004: Chapter 7 - Serviceability Limit State."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MPA
from blueprints.validations import raise_if_negative


class Form7Dot2StressDistributionCoefficient(Formula):
    r"""Class representing formula 7.2 for the calculation of [$k_c$]."""

    label = "7.2"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        sigma_c: MPA,
        k_1: DIMENSIONLESS,
        h: MM,
        f_ct_eff: MPA,
    ) -> None:
        r"""[$k_c$] Calculation of the coefficient for stress distribution for bending or bending combined with axial forces.

        EN 1992-1-1:2004 art.7.3.2(2) - Formula (7.2)

        Parameters
        ----------
        sigma_c : MPA
            [$\sigma_c$] Compressive stress in the concrete, according to 7.4 [$MPa$].
        k_1 : DIMENSIONLESS
            [$k_1$] Coefficient considering the effects of axial forces on the stress distribution, according to 7.2sub1 [$-$].
        h : MM
            [$h$] Overall depth of the section [$mm$].
        f_ct_eff : MPA
            [$f_{ct,eff}$] Mean value of the tensile strength of the concrete effective at the time when the
            cracks may first be expected to occur [$MPa$].
        """
        super().__init__()
        self.sigma_c = sigma_c
        self.k_1 = k_1
        self.h = h
        self.f_ct_eff = f_ct_eff

    @staticmethod
    def _evaluate(
        sigma_c: MPA,
        k_1: DIMENSIONLESS,
        h: MM,
        f_ct_eff: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(sigma_c=sigma_c, k_1=k_1, h=h, f_ct_eff=f_ct_eff)

        h_star = h if h < 1000 else 1000
        return min(0.4 * (1 - (sigma_c / (k_1 * (h / h_star) * f_ct_eff))), 1)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 7.2."""
        _equation: str = (
            r"min\left(0.4 \cdot \left(1 - \frac{\sigma_c}{k_1 \cdot \left(\frac{ h}{min( h, 1000)}\right) \cdot f_{ct,eff}}\right), 1\right)"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\sigma_c": f"{self.sigma_c:.{n}f}",
                r"k_1": f"{self.k_1:.{n}f}",
                r" h": f" {self.h:.{n}f}",
                r"f_{ct,eff}": f"{self.f_ct_eff:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"k_c",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="-",
        )


class Form7Dot2Sub1AxialForceCoefficient(Formula):
    r"""Class representing formula 7.2sub1 for the calculation of [$k_1$] factor."""

    label = "7.2sub1"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        n_ed: MPA,
        h: MM,
    ) -> None:
        r"""[$k_1$] Calculation of the coefficient for stress distribution for bending or bending combined with axial forces.

        EN 1992-1-1:2004 art.7.3.2(2) - Formula (7.2sub1)

        Parameters
        ----------
        n_ed : MPA
            [$N_{Ed}$] Axial force at the serviceability limit state acting on the part of the cross-section
            under consideration (compressive force positive). [$N_{Ed}$] should be determined considering the characteristic
            values of prestress and axial forces under the relevant combination of actions.
        h : MM
            [$h$] Overall depth of the section [$mm$].
        """
        super().__init__()
        self.n_ed = n_ed
        self.h = h

    @staticmethod
    def _evaluate(
        n_ed: MPA,
        h: MM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(h=h)

        h_star = h if h < 1000 else 1000
        return 1.5 if n_ed > 0 else 2 * h_star / (3 * h)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 7.2sub1."""
        _equation: str = r"\begin{cases} 1.5 & \text{if } N_{Ed} > 0 \\ \frac{2 \cdot min(h, 1000)}{3 \cdot h} & \text{if } N_{Ed} \le 0 \end{cases}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "N_{Ed}": f"{self.n_ed:.{n}f}",
                "h": f"{self.h:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"k_1",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="-",
        )

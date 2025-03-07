"""Formula 6.11a/b/cN from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form6Dot11abcNCompressionChordCoefficient(Formula):
    r"""Class representing formula 6.11a/b/cN for the calculation of the coefficient taking account of the state of the stress in
    the compression chord.
    """

    label = "6.11a/b/cN"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        sigma_cp: MPA,
        f_cd: MPA,
    ) -> None:
        r"""[$\alpha_{cw}$] Coefficient taking account of the state of the stress in the compression chord [$-$].

        NEN-EN 1992-1-1+C2:2011 art.6.2.3(3) - Formula (6.11.aN, 6.11.bN, and 6.11.cN)

        Parameters
        ----------
        sigma_cp : MPA
            [$\sigma_{cp}$] Mean compressive stress, measured positive, due to the design axial force [$MPa$].
        f_cd : MPA
            [$f_{cd}$] Design value of concrete compressive strength [$MPa$].
        """
        super().__init__()
        self.sigma_cp = sigma_cp
        self.f_cd = f_cd

    @staticmethod
    def _evaluate(
        sigma_cp: MPA,
        f_cd: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(f_cd=f_cd, sigma_cp=sigma_cp)

        if 0 < sigma_cp <= 0.25 * f_cd:
            return 1 + sigma_cp / f_cd
        if 0.25 * f_cd < sigma_cp <= 0.5 * f_cd:
            return 1.25
        return 2.5 * (1 - sigma_cp / f_cd)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.11a/b/cN."""
        return LatexFormula(
            return_symbol=r"\alpha_{cw}",
            result=f"{self:.3f}",
            equation=r"\begin{cases} 1 + \frac{\sigma_{cp}}{f_{cd}} & \text{if } 0 \lt \sigma_{cp} \leq 0.25 f_{cd} \\ "
            r"1.25 & \text{if } 0.25 f_{cd} \lt \sigma_{cp} \leq 0.5 f_{cd} \\ "
            r"2.5 \left(1 - \frac{\sigma_{cp}}{f_{cd}}\right) & \text{if } \sigma_{cp} \gt 0.5 f_{cd} \end{cases}",
            numeric_equation=rf"\begin{{cases}} 1 + \frac{{{self.sigma_cp:.3f}}}{{{self.f_cd:.3f}}} & \text{{if }} 0 \lt {self.sigma_cp:.3f} "
            rf"\leq 0.25 \cdot {self.f_cd:.3f} \\ 1.250 & \text{{if }} 0.25 \cdot {self.f_cd:.3f} \lt {self.sigma_cp:.3f} \leq "
            rf"0.5 \cdot {self.f_cd:.3f} \\ 2.5 \left(1 - \frac{{{self.sigma_cp:.3f}}}{{{self.f_cd:.3f}}}\right) & "
            rf"\text{{if }} {self.sigma_cp:.3f} \gt 0.5 \cdot {self.f_cd:.3f} \end{{cases}}",
            comparison_operator_label="=",
            unit="-",
        )

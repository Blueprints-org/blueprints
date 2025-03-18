"""Formula 5.28 and 6.5 from NEN-EN 1992-1-1+C2:2011: Chapter 5 and 6 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MM, MPA, N
from blueprints.validations import raise_if_negative


class Form6Dot5ShearForceCheck(Formula):
    r"""Class representing formula 6.5 for the shear force check, [$V_{Ed}$]."""

    label = "6.5"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        v_ed: N,
        b_w: MM,
        d: MM,
        nu: DIMENSIONLESS,
        f_cd: MPA,
    ) -> None:
        r"""[$V_{Ed}$] Shear force check [$N$].

        NEN-EN 1992-1-1+C2:2011 art.6.2.2(6) - Formula (6.5)

        Parameters
        ----------
        v_ed : N
            [$V_{Ed}$] Design value of shear force [$N$].
        b_w : MM
            [$b_w$] Width of the web [$mm$].
        d : MM
            [$d$] Effective depth [$mm$].
        nu : DIMENSIONLESS
            [$\nu$] Strength reduction factor for concrete cracked in shear [$-$].
        f_cd : MPA
            [$f_{cd}$] Design value of concrete compressive strength [$MPa$].
        """
        super().__init__()
        self.v_ed = v_ed
        self.b_w = b_w
        self.d = d
        self.nu = nu
        self.f_cd = f_cd

    @staticmethod
    def _evaluate(
        v_ed: N,
        b_w: MM,
        d: MM,
        nu: DIMENSIONLESS,
        f_cd: MPA,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            v_ed=v_ed,
            b_w=b_w,
            d=d,
            nu=nu,
            f_cd=f_cd,
        )
        return v_ed <= 0.5 * b_w * d * nu * f_cd

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.38a."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=r"V_{Ed} \leq 0.5 \cdot b_w \cdot d \cdot \nu \cdot f_{cd}",
            numeric_equation=rf"{self.v_ed:.3f} \leq 0.5 \cdot {self.b_w:.3f} \cdot {self.d:.3f} \cdot {self.nu:.3f} \cdot {self.f_cd:.3f}",
            comparison_operator_label="\\to",
            unit="",
        )

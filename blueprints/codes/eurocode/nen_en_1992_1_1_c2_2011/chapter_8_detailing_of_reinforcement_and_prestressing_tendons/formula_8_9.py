"""Formula 8.9 from NEN-EN 1992-1-1+C2:2011: Chapter 8: Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import KN, MM, MM2, MPA
from blueprints.unit_conversion import N_TO_KN
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter(Formula):
    """Class representing the formula 8.9 for the calculation of the anchorage capacity of a welded cross bar for nominal bar diameters smaller
    than 12 mm.
    """

    label = "8.9"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_wd: KN,
        diameter_t: MM,
        diameter_l: MM,
        a_s: MM2,
        f_cd: MPA,
    ) -> None:
        r"""[$F_{btd}$] Anchorage capacity of a welded cross bar for nominal bar diameters smaller than 12 mm [$kN$].

        NEN-EN 1992-1-1+C2:2011 art.8.6(5) - formula 8.9

        Parameters
        ----------
        f_wd : KN
            [$F_{wd}$] Design shear strength of weld (specified as a factor times [$A_{s} \cdot f_{yd}$]; say [$0.5 \cdot A_{s} \cdot f_{yd}$]
            where [$A_{s}$] is the cross-section of the anchored bar and [$f_{yd}$] is its design yield strength)  [$kN$].
        diameter_t : MM
            [$ø_{t}$] Diameter of the transverse bar [$mm$].

            Note: [$ø_{t} \leq 12$] [$mm$].
        diameter_l : MM
            [$ø_{l}$] Diameter of the bar to be anchored [$mm$].

            Note: [$ø_{l} \leq 12$] [$mm$].
        a_s : MM2
            [$A_{s}$] Cross-section of the anchored bar [$mm^{2}$].
        f_cd : MPA
            [$f_{cd}$] Design compressive strength of concrete [$MPa$].
        """
        super().__init__()
        self.f_wd = f_wd
        self.diameter_t = diameter_t
        self.diameter_l = diameter_l
        self.a_s = a_s
        self.f_cd = f_cd

    @staticmethod
    def _evaluate(
        f_wd: KN,
        diameter_t: MM,
        diameter_l: MM,
        a_s: MM2,
        f_cd: MPA,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            f_wd=f_wd,
            diameter_t=diameter_t,
            a_s=a_s,
            f_cd=f_cd,
        )
        raise_if_less_or_equal_to_zero(diameter_l=diameter_l)
        return min(f_wd, N_TO_KN * 16 * a_s * f_cd * (diameter_t / diameter_l))

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 8.9."""
        return LatexFormula(
            return_symbol=r"F_{btd}",
            result=f"{self:.2f}",
            equation=r"\min \left( F_{wd}, 16 \cdot A_s \cdot f_{cd} \cdot \frac{Ø_t}{Ø_l} \right)",
            numeric_equation=(
                rf"\min \left( {self.f_wd:.2f}, 1000 \cdot 16 \cdot {self.a_s:.2f} \cdot {self.f_cd:.2f} \cdot "
                rf"\frac{{{self.diameter_t:.2f}}}{{{self.diameter_l:.2f}}} \right)"
            ),
            comparison_operator_label="=",
        )

"""Formula 8.9 from EN 1992-1-1:2004: Chapter 8: Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import KN, MM, MM2, MPA
from blueprints.unit_conversion import N_TO_KN
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter(Formula):
    """Class representing the formula 8.9 for the calculation of the anchorage capacity of a welded cross bar for nominal bar diameters smaller
    than 12 mm.
    """

    label = "8.9"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        f_wd: KN,
        diameter_t: MM,
        diameter_l: MM,
        a_s: MM2,
        f_cd: MPA,
    ) -> None:
        r"""[$F_{btd}$] Anchorage capacity of a welded cross bar for nominal bar diameters smaller than 12 mm [$kN$].

        EN 1992-1-1:2004 art.8.6(5) - formula 8.9

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

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula 8.9."""
        _equation: str = r"\min \left( F_{wd}, 16 \cdot A_s \cdot f_{cd} \cdot \frac{Ø_t}{Ø_l} \right)"
        _numeric_equation: str = (
            rf"\min \left( {self.f_wd:.{n}f}, 1000 \cdot 16 \cdot {self.a_s:.{n}f} \cdot {self.f_cd:.{n}f} \cdot "
            rf"\frac{{{self.diameter_t:.{n}f}}}{{{self.diameter_l:.{n}f}}} \right)"
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"F_{wd}": rf"{self.f_wd:.{n}f} \ kN",
                r"A_s": rf"{self.a_s:.{n}f} \ mm^2",
                r"f_{cd}": rf"{self.f_cd:.{n}f} \ MPa",
                r"Ø_t": rf"{self.diameter_t:.{n}f} \ mm",
                r"Ø_l": rf"{self.diameter_l:.{n}f} \ mm",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"F_{btd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="kN",
        )

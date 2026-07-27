"""Formula 8.1 from EN 1992-1-1:2004: Chapter 8 Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import KN, MM, MPA
from blueprints.unit_conversion import KN_TO_N
from blueprints.validations import raise_if_negative


class Form8Dot1RequiredMinimumMandrelDiameter(Formula):
    """Class representing formula 8.1 for the calculation of the required minimum mandrel diameter if it needs to be checked to avoid
    concrete failure.
    """

    label = "8.1"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        f_bt: KN,
        a_b: MM,
        diameter: MM,
        f_cd: MPA,
    ) -> None:
        r"""[$\Ø_{m,min}$] minimum mandrel diameter if it needs to be checked to avoid concrete failure [$MM$].

        EN 1992-1-1:2004 art.8.3(3) - Formula (8.1)

        Parameters
        ----------
        f_bt: KN
            [$F_{bt}$] Tensile force from ultimate loads in a bar or group of bars in contact at the start of a bend  [$kN$].
        a_b: MM
            [$a_b$] Half of the centre-to-centre distance between bars (or groups of bars) perpendicular
            to the plane of the bend for a given bar (or group of bars in contact).
            For a bar or group of bars adjacent to the face of the member, [$a_b$] should be taken as the cover plus [$\Ø/2$] [$mm$].
        diameter: MM
            [$\Ø$] Diameter of reinforcing bar [$mm$].
        f_cd: MPA
            [$f_{cd}$] Design value of concrete compressive stress [$MPa$].
            Note: The value of [$f_{cd}$] should not be taken greater than that for concrete class C55/67.
        """
        super().__init__()
        self.f_bt = f_bt
        self.a_b = a_b
        self.diameter = diameter
        self.f_cd = f_cd

    @staticmethod
    def _evaluate(
        f_bt: KN,
        a_b: MM,
        diameter: MM,
        f_cd: MPA,
    ) -> MM:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(
            f_bt=f_bt,
            a_b=a_b,
            diameter=diameter,
            f_cd=f_cd,
        )
        return f_bt * KN_TO_N * ((1 / a_b) + 1 / (2 * diameter)) / f_cd

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.1."""
        _equation: str = r"\frac{F_{bt} \cdot \left( \frac{1}{a_b} + \frac{1}{2 \cdot Ø} \right) }{f_{cd}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"F_{bt}": f"{self.f_bt:.{n}f} \cdot 1000",
                r"a_b": f"{self.a_b:.{n}f}",
                r"Ø": f"{self.diameter:.{n}f}",
                r"f_{cd}": f"{self.f_cd:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"F_{bt}": rf"{self.f_bt:.{n}f} \ kN \cdot 1000",
                r"a_b": rf"{self.a_b:.{n}f} \ mm",
                r"Ø": rf"{self.diameter:.{n}f} \ mm",
                r"f_{cd}": rf"{self.f_cd:.{n}f} \ MPa",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"Ø_{m,min}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="mm",
        )

if __name__ == "__main__":
    my_form = Form8Dot1RequiredMinimumMandrelDiameter(
        f_bt=80,
        a_b=200,
        diameter=16,
        f_cd=30,
    )
    latex = my_form.latex()
    print(latex.complete_with_units)
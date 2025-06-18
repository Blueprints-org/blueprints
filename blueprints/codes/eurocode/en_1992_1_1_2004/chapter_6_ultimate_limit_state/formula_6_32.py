"""Formula 6.32 from EN 1992-1-1:2004: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


class Form6Dot32EffectiveDepthSlab(Formula):
    r"""Class representing formula 6.32 for the calculation of the effective depth of the slab, [$d_{eff}$]."""

    label = "6.32"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        d_y: MM,
        d_z: MM,
    ) -> None:
        r"""[$d_{eff}$] Effective depth of the slab [$mm$].

        EN 1992-1-1:2004 art.6.4.2(1) - Formula (6.32)

        Parameters
        ----------
        d_y : MM
            [$d_{y}$] Effective depth of the reinforcement in the y-direction [$mm$].
        d_z : MM
            [$d_{z}$] Effective depth of the reinforcement in the z-direction [$mm$].
        """
        super().__init__()
        self.d_y = d_y
        self.d_z = d_z

    @staticmethod
    def _evaluate(
        d_y: MM,
        d_z: MM,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(d_y=d_y, d_z=d_z)
        return (d_y + d_z) / 2

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.32."""
        return LatexFormula(
            return_symbol=r"d_{eff}",
            result=f"{self:.{n}f}",
            equation=r"\frac{d_{y} + d_{z}}{2}",
            numeric_equation=rf"\frac{{{self.d_y:.{n}f} + {self.d_z:.{n}f}}}{{2}}",
            comparison_operator_label="=",
            unit="mm",
        )

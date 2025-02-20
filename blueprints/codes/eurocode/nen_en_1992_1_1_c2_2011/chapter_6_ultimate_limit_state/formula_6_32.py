"""Formula 6.32 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


class Form6Dot32EffectiveDepthSlab(Formula):
    r"""Class representing formula 6.32 for the calculation of the effective depth of the slab, [$d_{eff}$]."""

    label = "6.32"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        d_y: MM,
        d_z: MM,
    ) -> None:
        r"""[$d_{eff}$] Effective depth of the slab [$mm$].

        NEN-EN 1992-1-1+C2:2011 art.6.4.2(1) - Formula (6.32)

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

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.32."""
        return LatexFormula(
            return_symbol=r"d_{eff}",
            result=f"{self:.3f}",
            equation=r"\frac{d_{y} + d_{z}}{2}",
            numeric_equation=rf"\frac{{{self.d_y:.3f} + {self.d_z:.3f}}}{{2}}",
            comparison_operator_label="=",
            unit="mm",
        )

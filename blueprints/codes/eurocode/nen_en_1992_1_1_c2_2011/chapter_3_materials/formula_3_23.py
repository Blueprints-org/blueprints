"""Formula 3.23 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM, MPA


class Form3Dot23FlexuralTensileStrength(Formula):
    """Class representing formula 3.23 for the calculation of the mean flexural tensile strength of reinforced concrete members."""

    label = "3.23"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        h: MM,
        f_ctm: MPA,
    ) -> None:
        r"""[$f_{ctm,fl}$] Mean flexural tensile strength of reinforced concrete members  [$MPa$].

        NEN-EN 1992-1-1+C2:2011 art.3.1.8(1) - Formula (3.23)

        Parameters
        ----------
        h : MM
            [${h}$] Total member depth [mm].
        f_ctm : MPA
            [${f_{ctm}}$] Mean axial tensile strength following from table 3.1 [$MPa$].

        Returns
        -------
        None
        """
        super().__init__()
        self.h = h
        self.f_ctm = f_ctm

    @staticmethod
    def _evaluate(
        h: MM,
        f_ctm: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        if h < 0:
            raise ValueError(f"Invalid h: {h}. h cannot be negative")
        if f_ctm < 0:
            raise ValueError(f"Invalid f_ctm: {f_ctm}. f_ctm cannot be negative")
        return max((1.6 - h / 1000) * f_ctm, f_ctm)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 3.23."""
        return LatexFormula(
            return_symbol=r"f_{ctm,fl}",
            result=f"{self:.3f}",
            equation=r"\max \left[ (1.6 - h/1000) \cdot f_{ctm} ; f_{ctm} \right]",
            numeric_equation=rf"\max \left[ (1.6 - {self.h:.3f}/1000) \cdot {self.f_ctm:.3f} ; {self.f_ctm:.3f} \right]",
            comparison_operator_label="=",
        )

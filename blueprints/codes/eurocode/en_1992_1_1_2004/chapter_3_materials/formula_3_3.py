"""Formula 3.3 from EN 1992-1-1:2004: Chapter 3 - Materials."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MPA


class Form3Dot3AxialTensileStrengthFromTensileSplittingStrength(Formula):
    """Class representing formula 3.3 for the approximated axial tensile strength, [$f_{ct}$], determined by tensile splitting strength."""

    label = "3.3"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        f_ct_sp: MPA,
    ) -> None:
        r"""[$f_{ct}$] The approximated axial tensile strength when tensile strength is determined as coefficient
        which is dependent of the age of concrete [$MPa$].

        EN 1992-1-1:2004 art.3.1.2(8) - Formula (3.3)

        Parameters
        ----------
        f_ct_sp : MPA
            [$f_{ct,sp}$] Tensile strength determined by tensile splitting strength [$MPa$].

        Returns
        -------
        None
        """
        super().__init__()
        self.f_ct_sp = f_ct_sp

    @staticmethod
    def _evaluate(
        f_ct_sp: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        if f_ct_sp < 0:
            raise ValueError(f"Negative f_ct_sp: {f_ct_sp}. f_ct_sp cannot be negative")
        return 0.9 * f_ct_sp

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 3.3."""
        return LatexFormula(
            return_symbol=r"f_{ct}",
            result=f"{self:.{n}f}",
            equation=r"0.9 \cdot f_{ct,sp}",
            numeric_equation=rf"0.9 \cdot {self.f_ct_sp:.{n}f}",
            comparison_operator_label="=",
        )

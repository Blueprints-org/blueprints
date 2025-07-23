"""Formula 3.8 from EN 1992-1-1:2004: Chapter 3 - Materials."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS


class Form3Dot8TotalShrinkage(Formula):
    """Class representing formula 3.8 for the calculation of the total shrinkage."""

    label = "3.8"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        epsilon_cd: DIMENSIONLESS,
        epsilon_ca: DIMENSIONLESS,
    ) -> None:
        r"""[$\epsilon_{cs}$] The total shrinkage [-].

        EN 1992-1-1:2004 art.3.1.4(6) - Formula (3.8)

        Parameters
        ----------
        epsilon_cd : DIMENSIONLESS
            [$\epsilon_{cd}$] Drying shrinkage [$-$].
        epsilon_ca : DIMENSIONLESS
            [$\epsilon_{ca}$] Autogene shrinkage [$-$].

        Returns
        -------
        None
        """
        super().__init__()
        self.epsilon_cd = epsilon_cd
        self.epsilon_ca = epsilon_ca

    @staticmethod
    def _evaluate(
        epsilon_cd: DIMENSIONLESS,
        epsilon_ca: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        return epsilon_cd + epsilon_ca

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 3.8."""
        return LatexFormula(
            return_symbol=r"\epsilon_{cs}",
            result=f"{self:.{n}f}",
            equation=r"\epsilon_{cd} + \epsilon_{ca}",
            numeric_equation=rf"{self.epsilon_cd:.{n}f} + {self.epsilon_ca:.{n}f}",
            comparison_operator_label="=",
        )

"""Formula 3.27 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA


class Form3Dot27IncreasedStrainLimitValue(Formula):
    """Class representing formula 3.27 for the calculation of the increased strain limit value due to enclosed concrete."""

    label = "3.27"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_ck: MPA,
        sigma_2: MPA,
        epsilon_cu2: DIMENSIONLESS,
    ) -> None:
        r"""[$\epsilon_{cu2,c}$] Increased strain limit value due to enclosed concrete. [$-$].

        NEN-EN 1992-1-1+C2:2011 art.3.1.9(2) - Formula (3.27)

        Parameters
        ----------
        f_ck : MPA
            [$f_{ck}$] Characteristic compressive strength [$MPa$]
        sigma_2 : MPA
            [$\sigma_{2}$] Effective compressive stress in transverse direction [$MPa$]
        epsilon_cu2 : DIMENSIONLESS
            [$\epsilon_{cu2}$] Strain limit value [$-$]

        Returns
        -------
        None
        """
        super().__init__()
        self.f_ck = f_ck
        self.sigma_2 = sigma_2
        self.epsilon_cu2 = epsilon_cu2

    @staticmethod
    def _evaluate(
        f_ck: MPA,
        sigma_2: MPA,
        epsilon_cu2: DIMENSIONLESS,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        if f_ck < 0:
            raise ValueError(f"Invalid f_ck: {f_ck}. f_ck cannot be negative")
        return epsilon_cu2 + 0.2 * sigma_2 / f_ck

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 3.27."""
        return LatexFormula(
            return_symbol=r"\epsilon_{cu2,c}",
            result=f"{self:.3f}",
            equation=r"\epsilon_{cu2} + 0.2 \cdot \sigma_2 / f_{ck}",
            numeric_equation=rf"{self.epsilon_cu2:.3f} + 0.2 \cdot {self.sigma_2:.3f} / {self.f_ck:.3f}",
            comparison_operator_label="=",
        )

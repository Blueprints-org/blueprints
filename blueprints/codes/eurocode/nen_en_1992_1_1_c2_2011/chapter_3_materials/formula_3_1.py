"""Formula 3.1 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form3Dot1EstimationConcreteCompressiveStrength(Formula):
    r"""Class representing formula 3.1 for the estimation of the concrete compressive strength, [$f_{cm}(t)$], after t days
    with an average temperature of 20 degrees Celsius.
    """

    label = "3.1"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        beta_cc_t: DIMENSIONLESS,
        f_cm: MPA,
    ) -> None:
        r"""[$f_{cm}(t)$] The estimated concrete compressive strength [$MPa$].

        NEN-EN 1992-1-1+C2:2011 art.3.1.2(6) - Formula (3.1)

        Parameters
        ----------
        beta_cc_t : DIMENSIONLESS
            [$\beta_{cc}(t)$] Coefficient dependent of the age of concrete [$-$].
        f_cm : MPA
            [$f_{cm}$] Average concrete compressive strength on day 28 based on table 3.1 [$MPa$].

        Returns
        -------
        None
        """
        super().__init__()
        self.beta_cc_t = beta_cc_t
        self.f_cm = f_cm

    @staticmethod
    def _evaluate(
        beta_cc_t: DIMENSIONLESS,
        f_cm: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(beta_cc_t=beta_cc_t, f_cm=f_cm)
        return beta_cc_t * f_cm

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 3.1."""
        return LatexFormula(
            return_symbol=r"f_{cm}(t)",
            result=f"{self:.3f}",
            equation=r"\beta_{cc}(t) \cdot f_{cm}",
            numeric_equation=rf"{self.beta_cc_t:.3f} \cdot {self.f_cm:.3f}",
            comparison_operator_label="=",
        )

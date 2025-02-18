"""Formula 8.13 from NEN-EN 1992-1-1+C2:2011: Chapter 8: Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MM2
from blueprints.validations import raise_if_negative


class Form8Dot13AdditionalShearReinforcement(Formula):
    """Class representing formula 8.13 for the calculation of the minimum additional shear reinforcement in the anchorage zones where transverse
    compression is not present for straight anchorage lengths, in the direction perpendicular to the tension face.
    """

    label = "8.13"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        a_s: MM2,
        n_2: DIMENSIONLESS,
    ) -> None:
        r"""[$A_{sh}$] Minimum additional shear reinforcement in the anchorage zones where transverse compression is not present for straight
        anchorage lengths, in the direction perpendicular to the tension face [$mm^2$].

        NEN-EN 1992-1-1+C2:2011 art.8.8(6) - Formula (8.12)

        Parameters
        ----------
        a_s: MM2
            [$A_{s}$] Cross sectional area of reinforcement [$mm^2$].
        n_2: DIMENSIONLESS
            [$n_{2}$] Number of bars anchored in each layer [$-$].
        """
        super().__init__()
        self.a_s = a_s
        self.n_2 = n_2

    @staticmethod
    def _evaluate(
        a_s: MM2,
        n_2: DIMENSIONLESS,
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_s=a_s, n_2=n_2)
        return 0.25 * a_s * n_2

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 8.13."""
        return LatexFormula(
            return_symbol=r"A_{sv}",
            result=f"{self:.2f}",
            equation=r"0.25 \cdot A_s \cdot n_2",
            numeric_equation=rf"0.25 \cdot {self.a_s:.2f} \cdot {self.n_2:.2f}",
            comparison_operator_label="=",
        )

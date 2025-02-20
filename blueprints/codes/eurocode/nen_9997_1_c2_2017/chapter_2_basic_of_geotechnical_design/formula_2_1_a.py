"""Formula 2.1a from NEN 9997-1+C2:2017: Chapter 2: Basis of geotechnical design."""

from blueprints.codes.eurocode.nen_9997_1_c2_2017 import NEN_9997_1_C2_2017
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_negative


class Form2Dot1aDesignValueLoad(Formula):
    """Class representing formula 2.1a for the calculation of the design value [$F_{d}$] of actions."""

    label = "2.1a"
    source_document = NEN_9997_1_C2_2017

    def __init__(self, gamma_f: DIMENSIONLESS, f_rep: DIMENSIONLESS) -> None:
        r"""[$F_{d}$] Design value of actions.

        NEN 9997-1+C2:2017 art.2.4.6.1(2) - (Formula 2.1a)

        Parameters
        ----------
        gamma_f : DIMENSIONLESS
            [$\gamma_{F}$] partial factor for actions for persistent and transient situations defined in annex A [$-$].
        f_rep : DIMENSIONLESS
            [$F_{rep}$] Representative value of actions.

            Use your own implementation for this value or use :class:`Form2Dot1bRepresentativeValue`.
        """
        super().__init__()
        self.gamma_f = gamma_f
        self.f_rep = f_rep

    @staticmethod
    def _evaluate(
        gamma_f: DIMENSIONLESS,
        f_rep: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(gamma_f=gamma_f)
        return gamma_f * f_rep

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 2.1a."""
        return LatexFormula(
            return_symbol=r"F_d",
            result=f"{self:.2f}",
            equation=r"\gamma_F \cdot F_{rep}",
            numeric_equation=rf"{self.gamma_f:.2f} \cdot {self.f_rep:.2f}",
            comparison_operator_label="=",
        )

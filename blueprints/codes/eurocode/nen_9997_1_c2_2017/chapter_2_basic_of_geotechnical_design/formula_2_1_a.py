"""Formula 2.1a from NEN 9997-1+C2:2017: Chapter 2: Basis of geotechnical design."""

from blueprints.codes.eurocode.nen_9997_1_c2_2017 import NEN_9997_1_C2_2017
from blueprints.codes.formula import Formula
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_negative


class Form2Dot1aDesignValueLoad(Formula):
    """Class representing formula 2.1a for the calculation of the design value :math:`F_{d}` of actions."""

    label = "2.1a"
    source_document = NEN_9997_1_C2_2017

    def __init__(self, gamma_f: DIMENSIONLESS, f_rep: float) -> None:
        """[:math:`F_{d}`] Design value of actions.

        NEN 9997-1+C2:2017 art.2.4.6.1(2) - (Formula 2.1a)

        Parameters
        ----------
        gamma_f : DIMENSIONLESS
            [:math:`γ_{F}`] partial factor for actions for persistent and transient situations defined in annex A [-].
        f_rep : float
            [:math:`F_{rep}`] Representative value of actions.

            Use your own implementation for this value or use :class:`Form2Dot1bRepresentativeValue`.
        """
        super().__init__()
        self.gamma_f = gamma_f
        self.f_rep = f_rep

    @staticmethod
    def _evaluate(
        gamma_f: DIMENSIONLESS,
        f_rep: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(gamma_f=gamma_f)
        return gamma_f * f_rep

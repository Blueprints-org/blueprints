"""Formula 3.16 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import MPA


class Form3Dot16DesignValueTensileStrength(Formula):
    """Class representing formula 3.16 for the calculation of the concrete tensile strength design value."""

    label = "3.16"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        alpha_ct: float,
        f_ctk_0_05: MPA,
        gamma_c: float,
    ) -> None:
        """[fcd] Design value concrete tensile strength [MPa].

        NEN-EN 1992-1-1+C2:2011 art.3.1.6(2) - Formula (3.16)

        Parameters
        ----------
        alpha_ct : float
            [αct] Coefficient taking long term effects on tensile strength into account and unfavorable effect due to positioning loading [-]
            See national appendix. Recommended value: 1.0
        f_ctk_0_05 : MPA
            [fctk,0,05] Characteristic tensile strength 5% [MPa].
        gamma_c : float
            [γc] Partial safety factor concrete, see 2.4.2.4 [-].

        Returns
        -------
        None
        """
        super().__init__()
        self.alpha_ct = alpha_ct
        self.f_ctk_0_05 = f_ctk_0_05
        self.gamma_c = gamma_c

    @staticmethod
    def _evaluate(
        alpha_ct: float,
        f_ctk_0_05: MPA,
        gamma_c: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        if alpha_ct < 0:
            raise ValueError(f"Invalid alpha_ct: {alpha_ct}. alpha_ct cannot be negative")
        if f_ctk_0_05 < 0:
            raise ValueError(f"Invalid f_ctk_0_05: {f_ctk_0_05}. f_ctk_0_05 cannot be negative")
        if gamma_c <= 0:
            raise ValueError(f"Invalid gamma_c: {gamma_c}. gamma_c cannot be negative or zero")
        return alpha_ct * f_ctk_0_05 / gamma_c

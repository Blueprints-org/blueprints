"""Formula 3.26 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import MPA


class Form3Dot26IncreasedStrainAtMaxStrength(Formula):
    """Class representing formula 3.26 for the calculation of the increased strain at the maximum strength due to enclosed concrete."""

    label = "3.26"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_ck: MPA,
        f_ck_c: MPA,
        epsilon_c2: float,
    ) -> None:
        """[εc2,c] Increased strain at the maximum strength due to enclosed concrete. [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.9(2) - Formula (3.26)

        Parameters
        ----------
        f_ck : MPA
            [fck] Characteristic compressive strength [MPa]
        f_ck_c : MPA
            [fck,c] Increased characteristic compressive strength due to enclosed concrete [MPa].
            See classes Form3Dot24IncreasedCharacteristicCompressiveStrength and/or Form3Dot25IncreasedCharacteristicCompressiveStrength
        epsilon_c2 : float
            [εc2] Strain at maximum strength [-]

        Returns
        -------
        None
        """
        super().__init__()
        self.f_ck = f_ck
        self.f_ck_c = f_ck_c
        self.epsilon_c2 = epsilon_c2

    @staticmethod
    def _evaluate(
        f_ck: MPA,
        f_ck_c: MPA,
        epsilon_c2: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        if f_ck < 0:
            raise ValueError(f"Invalid f_ck: {f_ck}. f_ck cannot be negative")
        if f_ck_c < 0:
            raise ValueError(f"Invalid f_ck_c: {f_ck_c}. f_ck_c cannot be negative")
        return epsilon_c2 * (f_ck_c / f_ck) ** 2

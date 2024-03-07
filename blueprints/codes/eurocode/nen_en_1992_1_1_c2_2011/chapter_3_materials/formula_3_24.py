"""Formula 3.24 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import MPA


class Form3Dot24IncreasedCharacteristicCompressiveStrength(Formula):
    """Class representing formula 3.24 for the calculation of the increased characteristic compressive strength due to enclosed concrete."""

    label = "3.24"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_ck: MPA,
        sigma_2: MPA,
    ) -> None:
        """[fck,c] Increased characteristic compressive strength due to enclosed concrete [MPa].

        NEN-EN 1992-1-1+C2:2011 art.3.1.9(2) - Formula (3.24)

        Parameters
        ----------
        f_ck : MPA
            [fck] Characteristic compressive strength [MPa]
        sigma_2 : MPA
            [σ2] Effective compressive stress in transverse direction [MPa]
            σ2 <= 0.05 * fck

        Returns
        -------
        None
        """
        super().__init__()
        self.f_ck = f_ck
        self.sigma_2 = sigma_2

    @staticmethod
    def _evaluate(
        f_ck: MPA,
        sigma_2: MPA,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        if f_ck < 0:
            raise ValueError(f"Invalid f_ck: {f_ck}. f_ck cannot be negative")
        if sigma_2 > 0.05 * f_ck:
            raise ValueError(f"Invalid sigma_2: {sigma_2}. Try using Form3Dot25IncreasedCharacteristicCompressiveStrength class.")
        return f_ck * (1.000 + 5.0 * sigma_2 / f_ck)

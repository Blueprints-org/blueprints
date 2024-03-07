"""Formula 3.18 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import MPA


class Form3Dot18CompressiveStressConcrete(Formula):
    """Class representing formula 3.18 for the calculation of compressive stress in concrete using stress-strain diagram of figure 3.3."""

    label = "3.18"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_cd: MPA,
    ) -> None:
        """[σc] Compressive stress in concrete using stress-strain diagram of figure 3.3 [MPa].

        NEN-EN 1992-1-1+C2:2011 art.3.1.7(1) - Formula (3.18)

        Parameters
        ----------
        f_cd : MPA
            [fcd] Design value compressive strength concrete [MPa].

        Returns
        -------
        None
        """
        super().__init__()
        self.f_cd = f_cd

    @staticmethod
    def _evaluate(
        f_cd: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        if f_cd < 0:
            raise ValueError(f"Invalid f_cd: {f_cd}. f_cd cannot be negative")
        return f_cd

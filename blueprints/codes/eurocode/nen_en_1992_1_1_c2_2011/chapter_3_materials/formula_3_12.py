"""Formula 3.12 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import MPA


class Form3Dot12AutogeneShrinkageInfinity(Formula):
    """Class representing formula 3.12, which calculates the autogene shrinkage at infinity."""

    source_document = NEN_EN_1992_1_1_C2_2011
    label = "3.12"

    def __init__(
        self,
        f_ck: MPA,
    ) -> None:
        """[εca(∞)] Autogene shrinkage at infinity [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.4(6) - Formula (3.12)

        Parameters
        ----------
        f_ck : MPA
            [fck] Compressive strength concrete [MPa].

        Returns
        -------
        None
        """
        super().__init__()
        self.f_ck = f_ck

    @staticmethod
    def _evaluate(
        f_ck: MPA,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        if f_ck < 0:
            raise ValueError(f"Invalid f_ck: {f_ck}. f_ck cannot be negative")
        return 2.5 * (f_ck - 10) * 10**-6

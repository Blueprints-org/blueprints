"""Sub-formula 3.28, 3.29 and 3.30 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import MPA


class SubForm3Dot282930Mu(Formula):
    """Class representing sub-formula for 3.28, 3.29 and 3.30 for the calculation of μ."""

    label = "3.28 - 3.29 - 3.30"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        sigma_pi: MPA,
        f_pk: MPA,
    ) -> None:
        """[μ] Ratio between initial pre-stress and characteristic tensile strength  (σpi / fpk) [-].

        NEN-EN 1992-1-1+C2:2011 art.3.3.2(7) - μ

        Parameters
        ----------
        sigma_pi : MPA
            [σpi] Initial pre-stress [MPa]
        f_pk : MPA
            [fpk] Characteristic tensile strength of pre-stress steel [MPa]

        Returns
        -------
        None
        """
        super().__init__()
        self.sigma_pi = sigma_pi
        self.f_pk = f_pk

    @staticmethod
    def _evaluate(
        sigma_pi: MPA,
        f_pk: MPA,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        if f_pk < 0:
            raise ValueError(f"Invalid f_pk: {f_pk}. f_pk cannot be negative")
        return sigma_pi / f_pk

"""Calculation of nominal concrete cover from NEN-EN 1992-1-1: Chapter 4 - Durability and cover to reinforcement."""

from blueprints.checks.nominal_concrete_cover.constants.base import (
    NominalConcreteCoverConstantsBase as ConstantsBase,
)
from blueprints.checks.nominal_concrete_cover.definitions import AbrasionClass, CastingSurface
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.formula_4_1 import Form4Dot1NominalConcreteCover
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.formula_4_2 import Form4Dot2MinimumConcreteCover
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.table_4_2 import Table4Dot2MinimumCoverWithRegardToBond
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.table_4_4n import (
    Table4Dot4nMinimumCoverDurabilityReinforcementSteel,
)
from blueprints.codes.formula import Formula
from blueprints.type_alias import MM


class NominalConcreteCover(Formula):
    """Class responsible for the calculation of the nominal concrete cover :math:`c_{nom}` [:math:`mm`]."""

    label = "Nominal concrete cover"
    source_document = "NEN-EN 1992-1-1"

    def __init__(
        self,
        c_min_b: Table4Dot2MinimumCoverWithRegardToBond,
        c_min_dur: Table4Dot4nMinimumCoverDurabilityReinforcementSteel,
        constants: ConstantsBase,
        delta_c_dur_gamma: MM = 0,
        delta_c_dur_st: MM = 0,
        delta_c_dur_add: MM = 0,
        casting_surface: CastingSurface = CastingSurface.PERMANENTLY_EXPOSED,
        uneven_surface: bool = False,
        abrasion_class: AbrasionClass = AbrasionClass.NA,
    ) -> None:
        """[:math:`c_{nom}`] Calculates the nominal concrete cover [:math:`mm`]. It takes considerations of art.4.4.1.2 and 4.4.1.3 into account.

        Parameters
        ----------
        c_min_b: Table4Dot2MinimumCoverWithRegardToBond
            [:math:`c_{min,b}`] The minimum concrete cover based on the adhesion requirements based on art. 4.4.1.2 (3) [:math:`mm`].
        c_min_dur: Table4Dot4nMinimumCoverDurabilityReinforcementSteel
            [:math:`c_{min,dur}`] The minimum concrete cover based on environmental conditions based on art. 4.4.1.2 (5) [:math:`mm`].
        constants: ConstantsBase
            The constants for the calculation of the nominal concrete cover.
        delta_c_dur_gamma: MM
            [:math:`Δc_{dur,γ}`] An additional safety requirement based on art. 4.4.1.2 (6) [:math:`mm`].
            The value of [:math:`Δc_{dur,γ}`] for use in a Country may be found in its National Annex.
            The recommended value is O mm. 0 mm is the default value in the formula if not specified otherwise.
        delta_c_dur_st: MM
            [:math:`Δc_{dur,st}`] A reduction of minimum concrete cover when using stainless steel based on art. 4.4.1.2 (7) [:math:`mm`].
            The value of [:math:`Δc_{dur,st}`] for use in a Country may be found in its National Annex.
            The recommended value, without further specification, is 0 mm. 0 mm is the default value in the formula if not specified otherwise.
        delta_c_dur_add: MM
            [:math:`Δc_{dur,add}`] A reduction of minimum concrete cover when using additional protection based on art. 4.4.1.2 (8) [:math:`mm`].
            The value of [:math:`Δc_{dur,add}`] for use in a Country may be found in its National Annex.
            The recommended value, without further specification, is 0 mm. 0 mm is the default value in the formula if not specified otherwise.
        casting_surface: CastingSurface
            The casting surface of the concrete according to art. 4.4.1.3 (4).
            The default value is "Permanently exposed".
        uneven_surface: bool
            Is the surface uneven according to art. 4.4.1.2 (11)?
            The default value is False.
        abrasion_class: AbrasionClass
            The abrasion class of the concrete surface according to art. 4.4.1.2 (13).
            The default value is "Not applicable".
        """
        super().__init__()
        self.c_min_b = c_min_b
        self.c_min_dur = c_min_dur
        self.constants = constants
        self.delta_c_dur_gamma = delta_c_dur_gamma
        self.delta_c_dur_st = delta_c_dur_st
        self.delta_c_dur_add = delta_c_dur_add
        self.casting_surface = casting_surface
        self.uneven_surface = uneven_surface
        self.abrasion_class = abrasion_class

    @staticmethod
    def _evaluate(
        c_min_b: MM,
        c_min_dur: MM,
        constants: ConstantsBase,
        delta_c_dur_gamma: MM = 0,
        delta_c_dur_st: MM = 0,
        delta_c_dur_add: MM = 0,
        casting_surface: CastingSurface = CastingSurface.PERMANENTLY_EXPOSED,
        uneven_surface: bool = False,
        abrasion_class: AbrasionClass = AbrasionClass.NA,
    ) -> MM:
        """For more detailed documentation see the class docstring."""
        c_min = Form4Dot2MinimumConcreteCover(
            c_min_b=c_min_b,
            c_min_dur=c_min_dur,
            delta_c_dur_gamma=delta_c_dur_gamma,
            delta_c_dur_st=delta_c_dur_st,
            delta_c_dur_add=delta_c_dur_add,
        )

        # According to art. 4.4.1.2 (11) from NEN-EN 1992-1-1
        c_min += constants.COVER_INCREASE_FOR_UNEVEN_SURFACE * uneven_surface  # type: ignore[assignment]
        # According to art. 4.4.1.2 (13) from NEN-EN 1992-1-1
        c_min += constants.COVER_INCREATSE_FOR_ABRASION_CLASS[abrasion_class]  # type: ignore[assignment]

        return max(
            Form4Dot1NominalConcreteCover(c_min=c_min, delta_c_dev=constants.DEFAULT_DELTA_C_DEV),
            constants.minimum_cover_with_regard_to_casting_surface(c_min_dur, casting_surface),
        )

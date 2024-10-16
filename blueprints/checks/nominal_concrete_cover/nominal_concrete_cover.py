"""Calculation of nominal concrete cover from NEN-EN 1992-1-1: Chapter 4 - Durability and cover to reinforcement."""

from dataclasses import dataclass, field

from blueprints.checks.nominal_concrete_cover.constants.base import (
    NominalConcreteCoverConstantsBase as ConstantsBase,
)
from blueprints.checks.nominal_concrete_cover.definitions import AbrasionClass, CastingSurface
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.formula_4_1 import Form4Dot1NominalConcreteCover
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.formula_4_2 import Form4Dot2MinimumConcreteCover
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.table_4_1 import (
    Carbonation,
    Chemical,
    Chloride,
    ChlorideSeawater,
    FreezeThaw,
    Table4Dot1ExposureClasses,
)
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.table_4_2 import Table4Dot2MinimumCoverWithRegardToBond
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.table_4_4n import (
    Table4Dot4nMinimumCoverDurabilityReinforcementSteel,
)
from blueprints.codes.eurocode.structural_class import ConcreteStructuralClassBase
from blueprints.codes.latex_formula import latex_max_curly_brackets
from blueprints.type_alias import MM


@dataclass(frozen=True)
class NominalConcreteCover:
    """Class responsible for the calculation of the nominal concrete cover :math:`c_{nom}` [:math:`mm`].
    It takes considerations of art.4.4.1.2 and 4.4.1.3 into account.

    Parameters
    ----------
    reinforcement_diameter: MM
        The diameter of the reinforcement [:math:`mm`].
    nominal_max_aggregate_size: MM
        The nominal maximum aggregate size [:math:`mm`].
    constants: ConstantsBase
        The constants for the calculation of the nominal concrete cover.
    structural_class: ConcreteStructuralClassBase | int
        The structural class of the concrete. Either an instance of the ConcreteStructuralClassBase class or an integer.
        Tip: Use the :class:`Table4Dot3ConcreteStructuralClass` class to calculate the structural class.
    carbonation: Carbonation
        The classification of corrosion induced by carbonation. Default is "Not applicable".
    chloride: Chloride
        The classification of corrosion induced by chlorides other than by sea water. Default is "Not applicable".
    chloride_seawater: ChlorideSeawater
        The classification of corrosion induced by chlorides from sea water. Default is "Not applicable".
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

    label = "Nominal concrete cover according to art. 4.4.1"
    source_document = "NEN-EN 1992-1-1"

    reinforcement_diameter: MM
    nominal_max_aggregate_size: MM
    constants: ConstantsBase
    structural_class: ConcreteStructuralClassBase | int
    carbonation: Carbonation = field(default_factory=lambda: Carbonation.NA)
    chloride: Chloride = field(default_factory=lambda: Chloride.NA)
    chloride_seawater: ChlorideSeawater = field(default_factory=lambda: ChlorideSeawater.NA)
    delta_c_dur_gamma: MM = field(default=0)
    delta_c_dur_st: MM = field(default=0)
    delta_c_dur_add: MM = field(default=0)
    casting_surface: CastingSurface = field(default=CastingSurface.PERMANENTLY_EXPOSED)
    uneven_surface: bool = field(default=False)
    abrasion_class: AbrasionClass = field(default=AbrasionClass.NA)

    def __post_init__(self) -> None:
        """Check the input parameters for validity."""
        if not isinstance(self.uneven_surface, bool):
            raise TypeError(f"Invalid type for uneven_surface: {type(self.uneven_surface)}. Expected type is bool.")

        if not isinstance(self.abrasion_class, AbrasionClass):
            raise TypeError(f"Invalid type for abrasion_class: {type(self.abrasion_class)}. Expected type is AbrasionClass.")

        if not isinstance(self.casting_surface, CastingSurface):
            raise TypeError(f"Invalid type for casting_surface: {type(self.casting_surface)}. Expected type is CastingSurface.")

    def exposure_classes(self) -> Table4Dot1ExposureClasses:
        """Exposure classes according to table 4.1 from NEN-EN 1992-1-1."""
        return Table4Dot1ExposureClasses(self.carbonation, self.chloride, self.chloride_seawater, FreezeThaw.NA, Chemical.NA)

    def c_min_b(self) -> Table4Dot2MinimumCoverWithRegardToBond:
        """Minimum concrete cover with regard to bond according to table 4.2 from NEN-EN 1992-1-1."""
        return Table4Dot2MinimumCoverWithRegardToBond(self.reinforcement_diameter, self.nominal_max_aggregate_size > 32)

    def c_min_dur(self) -> Table4Dot4nMinimumCoverDurabilityReinforcementSteel:
        """Minimum concrete cover with regard to durability according to table 4.4N from NEN-EN 1992-1-1."""
        return Table4Dot4nMinimumCoverDurabilityReinforcementSteel(self.exposure_classes(), self.structural_class)  # type: ignore[arg-type]

    def c_min(self) -> Form4Dot2MinimumConcreteCover:
        """Minimum concrete cover according to formula 4.2 from NEN-EN 1992-1-1."""
        return Form4Dot2MinimumConcreteCover(
            c_min_b=self.c_min_b(),
            c_min_dur=self.c_min_dur(),
            delta_c_dur_gamma=self.delta_c_dur_gamma,
            delta_c_dur_st=self.delta_c_dur_st,
            delta_c_dur_add=self.delta_c_dur_add,
        )

    def c_min_total(self) -> MM:
        """Total minimum concrete cover according to art. 4.4.1.2 (11) and (13) from NEN-EN 1992-1-1."""
        c_min = self.c_min()
        # According to art. 4.4.1.2 (11) from NEN-EN 1992-1-1
        c_min += self.constants.COVER_INCREASE_FOR_UNEVEN_SURFACE * self.uneven_surface  # type: ignore[assignment]
        # According to art. 4.4.1.2 (13) from NEN-EN 1992-1-1
        c_min += self.constants.COVER_INCREASE_FOR_ABRASION_CLASS[self.abrasion_class]  # type: ignore[assignment]
        return c_min

    def c_nom(self) -> Form4Dot1NominalConcreteCover:
        """Nominal concrete cover according to art. 4.4.1 from NEN-EN 1992-1-1."""
        return Form4Dot1NominalConcreteCover(c_min=self.c_min_total(), delta_c_dev=self.constants.DEFAULT_DELTA_C_DEV)

    def minimum_cover_with_regard_to_casting_surface(self) -> MM:
        """Calculate the minimum cover with regard to casting surface according to art. 4.4.1.3 (4) from NEN-EN 1992-1-1."""
        return self.constants.minimum_cover_with_regard_to_casting_surface(self.c_min_dur(), self.casting_surface)

    def value(self) -> MM:
        """Get the value of the nominal concrete cover."""
        return max(
            self.c_nom(),
            self.minimum_cover_with_regard_to_casting_surface(),
        )

    def latex(self) -> str:
        """Returns the lateX string representation for Nominal concrete cover check."""
        return "\n".join(
            [
                "Nominal concrete cover according to art. 4.4.1 from NEN-EN 1992-1-1:",
                latex_max_curly_brackets(
                    r"Nominal concrete cover according to art. 4.4.1 (c_{nom}).",
                    "Minimum cover with regard to casting surface according to art. 4.4.1.3 (4)",
                ),
                "",
                "Where:",
                r"c_{nom} = " + self.c_nom().latex().equation.replace("min", "min, total"),
                r"c_{min,total} = c_{min} + \Delta c_{uneven surface}  + \Delta c_{abrasion class}",
                r"c_{min} = " + self.c_min().latex().equation,
                r"c_{min,b} = " + self.c_min_b().latex().equation,
                r"c_{min,dur} = " + self.c_min_dur().latex().equation,
                "Minimum cover with regard to casting surface according to art. 4.4.1.3 (4) = "
                + self.constants.minimum_cover_with_regard_to_casting_surface_latex(self.casting_surface),
            ]
        )

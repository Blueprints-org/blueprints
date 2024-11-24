"""Example of nominal concrete cover calculation with Blueprints according to art.4.4.1.2 and 4.4.1.3 of ."""

from blueprints.checks.nominal_concrete_cover.constants.constants_nen_en_1992_1_1_c2_2011 import NominalConcreteCoverConstants2011C2
from blueprints.checks.nominal_concrete_cover.definitions import AbrasionClass, CastingSurface
from blueprints.checks.nominal_concrete_cover.nominal_concrete_cover import NominalConcreteCover
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.table_4_1 import Table4Dot1ExposureClasses
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.table_4_3 import Table4Dot3ConcreteStructuralClass
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass

# Define the concrete material to be used in the calculation
concrete_material = ConcreteMaterial(
    concrete_class=ConcreteStrengthClass.C30_37,
)

# Define the constants for the calculation of nominal concrete cover according to NEN-EN 1992-1-1+C2:2011
constants = NominalConcreteCoverConstants2011C2()

# Exposure classes of the concrete element
exposure_classes = Table4Dot1ExposureClasses.from_exposure_list(["XC1", "XD1", "XS1"])

# Define the structural class by its number (For example, S4)
structural_class = 4

# Or calculate the structural class by its exposure classes, design working life and other parameters
structural_class = Table4Dot3ConcreteStructuralClass(
    exposure_classes=exposure_classes,
    design_working_life=50,
    concrete_material=concrete_material,
    plate_geometry=False,
    quality_control=False,
)

# Define the nominal concrete cover
calculation = NominalConcreteCover(
    reinforcement_diameter=32,
    nominal_max_aggregate_size=32,
    constants=constants,
    structural_class=structural_class,
    carbonation=exposure_classes.carbonation,
    chloride=exposure_classes.chloride,
    chloride_seawater=exposure_classes.chloride_seawater,
    delta_c_dur_gamma=10,
    delta_c_dur_add=0,
    casting_surface=CastingSurface.PERMANENTLY_EXPOSED,
    uneven_surface=True,
    abrasion_class=AbrasionClass.NA,
)

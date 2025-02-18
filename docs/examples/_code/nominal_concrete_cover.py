"""Example of nominal concrete cover calculation with Blueprints according to art.4.4.1.2 and 4.4.1.3 of ."""
# ruff: noqa: T201

from blueprints.checks.nominal_concrete_cover.constants.constants_nen_en_1992_1_1_c2_2011 import NominalConcreteCoverConstants2011C2
from blueprints.checks.nominal_concrete_cover.definitions import AbrasionClass, CastingSurface
from blueprints.checks.nominal_concrete_cover.nominal_concrete_cover import NominalConcreteCover
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.table_4_3 import Table4Dot3ConcreteStructuralClass
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass

# Define the concrete material to be used in the calculation
concrete_material = ConcreteMaterial(concrete_class=ConcreteStrengthClass.C30_37)

# Calculate the structural class by its exposure classes, design working life and other parameters
structural_class = Table4Dot3ConcreteStructuralClass(
    exposure_classes=["XC1"],
    design_working_life=100,
    concrete_material=concrete_material,
    plate_geometry=False,
    quality_control=False,
)

# Define the nominal concrete cover
calculation = NominalConcreteCover(
    reinforcement_diameter=32,
    nominal_max_aggregate_size=32,
    constants=NominalConcreteCoverConstants2011C2(),
    structural_class=structural_class,  # or by its number, for example 4 in the case of S4
    carbonation="XC1",
    delta_c_dur_gamma=10,
    delta_c_dur_add=0,
    casting_surface=CastingSurface.PREPARED_GROUND,
    uneven_surface=False,
    abrasion_class=AbrasionClass.NA,
)

# check the results
print(
    f"Structural class: {structural_class}\n\n"
    f"C,min,dur: {calculation.c_min_dur()} mm\n"
    f"C,min,b: {calculation.c_min_b()} mm\n"
    f"C,min,total: {calculation.c_min_total()} mm\n"
    f"\tCover increase due to uneven surface: {calculation.cover_increase_for_uneven_surface()} mm\n"
    f"\tCover increase due to abrasion: {calculation.cover_increase_for_abrasion_class()} mm\n\n"
    f"Nominal concrete cover: {calculation.value()} mm\n"
    f"\tC,nom: {calculation.c_nom()} mm\n"
    f"\tMinimum cover with regard to casting surface: {calculation.minimum_cover_with_regard_to_casting_surface()} mm\n\n"
)


# Get a latex representation of the entire calculation, you can use this in your Word or PDF for example
print(calculation.latex())

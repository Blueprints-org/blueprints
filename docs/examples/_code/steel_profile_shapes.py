"""Steel Profile Shapes Example
This example demonstrates how to create and visualize different steel profile shapes using the Blueprints library.
"""

# ruff: noqa: T201

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.structural_sections.steel.steel_cross_sections.chs_profile import CHSSteelProfile, LoadStandardCHS
from blueprints.structural_sections.steel.steel_cross_sections.i_profile import ISteelProfile, LoadStandardIProfile
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.chs import CHS
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.heb import HEB
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.strip import Strip
from blueprints.structural_sections.steel.steel_cross_sections.strip_profile import LoadStandardStrip, StripSteelProfile

# Define steel class
steel_class = SteelStrengthClass.S355

# Example usage for CHS profile
chs_profile = LoadStandardCHS(profile=CHS.CHS273x5, steel_class=steel_class).get_profile(corrosion_inside=0, corrosion_outside=1)
chs_profile.plot(show=True)
print(f"Steel class: {chs_profile.steel_material}")
print(f"Moment of inertia about y-axis: {chs_profile.moment_of_inertia_about_y} mm⁴")
print(f"Moment of inertia about z-axis: {chs_profile.moment_of_inertia_about_z} mm⁴")
print(f"Elastic section modulus about y-axis: {chs_profile.elastic_section_modulus_about_y_negative} mm³")
print(f"Elastic section modulus about z-axis: {chs_profile.elastic_section_modulus_about_z_positive} mm³")
print(f"Area: {chs_profile.area} mm²")

# Example usage for custom CHS profile
custom_chs_profile = CHSSteelProfile(outer_diameter=150, wall_thickness=10, steel_class=steel_class)
custom_chs_profile.plot(show=True)

# Example usage for Strip profile
strip_profile = LoadStandardStrip(profile=Strip.STRIP160x5, steel_class=steel_class).get_profile(corrosion=1)
strip_profile.plot(show=True)

# Example usage for custom Strip profile
custom_strip_profile = StripSteelProfile(
    width=100,
    height=41,
    steel_class=steel_class,
)
custom_strip_profile.plot(show=True)

# Example usage for HEB600 profile
heb_profile = LoadStandardIProfile(profile=HEB.HEB600, steel_class=steel_class).get_profile(corrosion=7)
heb_profile.plot(show=True)

# Example usage for custom I profile
custom_i_profile = ISteelProfile(
    top_flange_width=300,  # mm
    top_flange_thickness=20,  # mm
    bottom_flange_width=200,  # mm
    bottom_flange_thickness=10,  # mm
    total_height=600,  # mm
    web_thickness=10,  # mm
    steel_class=steel_class,
    top_radius=15,  # mm
    bottom_radius=8,  # mm
)
custom_i_profile.plot(show=True)

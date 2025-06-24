"""Steel Profile Shapes Example
This example demonstrates how to create and visualize different steel profile shapes using the Blueprints library.
"""

import matplotlib.pyplot as plt

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.materials.steel import SteelMaterial

# ruff: noqa: T201
from blueprints.structural_sections.steel.steel_cross_sections.chs_profile import CHSSteelProfile
from blueprints.structural_sections.steel.steel_cross_sections.i_profile import ISteelProfile
from blueprints.structural_sections.steel.steel_cross_sections.rhs_profile import RHSSteelProfile
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.chs import CHS
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.heb import HEB
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.rhs import RHS
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.strip import Strip
from blueprints.structural_sections.steel.steel_cross_sections.strip_profile import StripSteelProfile

# Define steel class
steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)

# Example usage for CHS profile
chs_profile = CHSSteelProfile.from_standard_profile(
    profile=CHS.CHS273x5,
    steel_material=steel_material,
    corrosion_inside=0,  # mm
    corrosion_outside=4,  # mm
)

chs_profile.plot(show=False)
print(chs_profile.section_properties())

# Example usage for custom CHS profile
custom_chs_profile = CHSSteelProfile(
    outer_diameter=150,
    wall_thickness=10,
    steel_material=steel_material,
)

custom_chs_profile.plot(show=False)
print(custom_chs_profile.section_properties())

# Example usage for Strip profile
strip_profile = StripSteelProfile.from_standard_profile(
    profile=Strip.STRIP160x5,
    steel_material=steel_material,
    corrosion=1,  # mm
)

strip_profile.plot(show=False)
print(strip_profile.section_properties())

# Example usage for custom Strip profile
custom_strip_profile = StripSteelProfile(
    strip_width=100,
    strip_height=41,
    steel_material=steel_material,
)

custom_strip_profile.plot(show=False)
print(custom_strip_profile.section_properties())

# Example usage for HEB600 profile
heb_profile = ISteelProfile.from_standard_profile(
    profile=HEB.HEB600,
    steel_material=steel_material,
    corrosion=7,  # mm
)

heb_profile.plot(show=False)
print(heb_profile.section_properties())

# Example usage for custom I profile
custom_i_profile = ISteelProfile(
    top_flange_width=300,  # mm
    top_flange_thickness=20,  # mm
    bottom_flange_width=200,  # mm
    bottom_flange_thickness=10,  # mm
    total_height=600,  # mm
    web_thickness=10,  # mm
    steel_material=steel_material,
    top_radius=15,  # mm
    bottom_radius=8,  # mm
)

print(custom_i_profile.section_properties())
custom_i_profile.plot(show=False)

# Example usage for RHS profile
rhs_profile = RHSSteelProfile.from_standard_profile(
    profile=RHS.RHS400x200_16,
    steel_material=steel_material,
    corrosion_inside=0,  # mm
    corrosion_outside=0,  # mm
)

print(rhs_profile.section_properties())
rhs_profile.plot(show=False)

# Example usage for custom RHS profile
custom_rhs_profile = RHSSteelProfile(
    steel_material=steel_material,
    total_width=300,  # mm
    total_height=200,  # mm
    left_wall_thickness=12,  # mm
    right_wall_thickness=40,  # mm
    top_wall_thickness=9,  # mm
    bottom_wall_thickness=7,  # mm
    top_right_inner_radius=50,  # mm (optional)
    top_left_inner_radius=5,  # mm (optional)
    bottom_right_inner_radius=9,  # mm (optional)
    bottom_left_inner_radius=14,  # mm (optional)
    top_right_outer_radius=55,  # mm (optional)
    top_left_outer_radius=13,  # mm (optional)
    bottom_right_outer_radius=10,  # mm (optional)
    bottom_left_outer_radius=12,  # mm (optional)
)

print(custom_rhs_profile.section_properties())
custom_rhs_profile.plot(show=False)

plt.show()

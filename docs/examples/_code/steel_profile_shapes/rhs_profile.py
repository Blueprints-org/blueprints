"""Steel Profile Shapes Example
This example demonstrates how to create and visualize RHS steel profile shapes using the Blueprints library.
"""

import matplotlib.pyplot as plt

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.steel.steel_cross_sections.rhs_profile import RHSSteelProfile
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.rhs import RHS

# Define steel class
steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)

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
    total_height=350,  # mm
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

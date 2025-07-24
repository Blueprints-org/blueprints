"""Steel Profile Shapes Example
This example demonstrates how to create and visualize CHS steel profile shapes using the Blueprints library.
"""

import matplotlib.pyplot as plt

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.steel.steel_cross_sections.chs_profile import CHSSteelProfile
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.chs import CHS

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

plt.show()

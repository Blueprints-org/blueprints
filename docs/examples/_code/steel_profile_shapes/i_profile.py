"""Steel I-Profile Example
This example demonstrates how to create and visualize steel I-profiles using the Blueprints library.
"""

import matplotlib.pyplot as plt

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.steel.steel_cross_sections.i_profile import ISteelProfile
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.heb import HEB

# Define steel class
steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)

# Example usage for HEB600 I-profile
heb_profile = ISteelProfile.from_standard_profile(
    profile=HEB.HEB600,
    steel_material=steel_material,
    corrosion=7,  # mm
)

heb_profile.plot(show=False)
print(heb_profile.section_properties())

# Example usage for custom I-profile
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

plt.show()

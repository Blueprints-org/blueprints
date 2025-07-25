"""Steel Profile Shapes Example
This example demonstrates how to create and visualize strip steel profile shapes using the Blueprints library.
"""

import matplotlib.pyplot as plt

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.strip import Strip
from blueprints.structural_sections.steel.steel_cross_sections.strip_profile import StripSteelProfile

# Define steel class
steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)

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

plt.show()

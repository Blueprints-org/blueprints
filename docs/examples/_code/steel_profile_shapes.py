"""Steel Profile Shapes Example
This example demonstrates how to create and visualize different steel profile shapes using the Blueprints library.
"""

# ruff: noqa: T201

from blueprints.materials.steel import SteelStrengthClass
from blueprints.structural_sections.steel.steel_cross_sections.chs_profile import CHSProfiles, CHSSteelProfile
from blueprints.structural_sections.steel.steel_cross_sections.i_profile import IProfiles, ISteelProfile
from blueprints.structural_sections.steel.steel_cross_sections.rhs_profile import RHSProfiles, RHSSteelProfile
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.chs import CHSStandardProfileClass
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.heb import HEBStandardProfileClass
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.rhs import RHSStandardProfileClass
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.strip import StripStandardProfileClass
from blueprints.structural_sections.steel.steel_cross_sections.strip_profile import StripProfiles, StripSteelProfile

# Define steel class
steel_class = SteelStrengthClass.EN_10025_2_S355

# Example usage for CHS profile
chs_profile = CHSProfiles(profile=CHSStandardProfileClass.CHS_273x5, steel_class=steel_class).get_profile()
chs_profile.plot(show=True)
print(f"Steel class: {chs_profile.steel_material}")
print(f"Moment of inertia about y-axis: {chs_profile.moment_of_inertia_about_y} mm⁴")
print(f"Moment of inertia about z-axis: {chs_profile.moment_of_inertia_about_z} mm⁴")
print(f"Elastic section modulus about y-axis: {chs_profile.elastic_section_modulus_about_y_negative} mm³")
print(f"Elastic section modulus about z-axis: {chs_profile.elastic_section_modulus_about_z_positive} mm³")
print(f"Area: {chs_profile.steel_area} mm²")

# Example usage for custom CHS profile
custom_chs_profile = CHSSteelProfile(outer_diameter=150, wall_thickness=10, steel_class=steel_class)
custom_chs_profile.plot(show=True)

# Example usage for RHS profile
rhs_profile = RHSProfiles(profile=RHSStandardProfileClass.RHS120x60_4, steel_class=steel_class).get_profile()
rhs_profile.plot(show=True)

# Example usage for custom RHS profile
custom_rhs_profile = RHSSteelProfile(total_height=100, total_width=100, thickness=5, steel_class=steel_class)
custom_rhs_profile.plot(show=True)

# Example usage for I-profile (HEB)
i_profile = IProfiles(profile=HEBStandardProfileClass.HEB_200, steel_class=steel_class).get_profile()
i_profile.plot(show=True)

# Example usage for custom I-profile
custom_i_profile = ISteelProfile(
    top_flange_width=200,
    top_flange_thickness=15,
    bottom_flange_width=200,
    bottom_flange_thickness=15,
    total_height=400,
    web_thickness=10,
    steel_class=steel_class,
    top_radius=10,
    bottom_radius=10,
)
custom_i_profile.plot(show=True)

# Example usage for Strip profile
strip_profile = StripProfiles(profile=StripStandardProfileClass.STRIP_160x5, steel_class=steel_class).get_profile()
strip_profile.plot(show=True)

# Example usage for custom Strip profile
custom_strip_profile = StripSteelProfile(
    width=100,
    height=30,
    steel_class=steel_class,
)
custom_strip_profile.plot(show=True)

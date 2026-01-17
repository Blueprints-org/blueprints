from blueprints.structural_sections.steel.profile_definitions.unp_profile import UNPProfile
from blueprints.type_alias import MM, PERCENTAGE

class UNP:
    UNP80: UNPProfile
    UNP100: UNPProfile
    UNP120: UNPProfile
    UNP140: UNPProfile
    UNP160: UNPProfile
    UNP180: UNPProfile
    UNP200: UNPProfile
    UNP220: UNPProfile
    UNP240: UNPProfile
    UNP260: UNPProfile
    UNP280: UNPProfile
    UNP300: UNPProfile
    UNP320: UNPProfile
    UNP350: UNPProfile
    UNP380: UNPProfile
    UNP400: UNPProfile

class __UNPProfileParameters:
    name: str
    top_flange_total_width: MM
    top_flange_thickness: MM
    bottom_flange_total_width: MM
    bottom_flange_thickness: MM
    total_height: MM
    web_thickness: MM
    root_fillet_radius: MM
    toe_radius: MM
    slope: PERCENTAGE

UNP_PROFILES_DATABASE: dict[str, __UNPProfileParameters]

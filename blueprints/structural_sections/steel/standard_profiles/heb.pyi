from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.type_alias import MM

class HEB:
    HEB100: IProfile
    HEB120: IProfile
    HEB140: IProfile
    HEB160: IProfile
    HEB180: IProfile
    HEB200: IProfile
    HEB220: IProfile
    HEB240: IProfile
    HEB260: IProfile
    HEB280: IProfile
    HEB300: IProfile
    HEB320: IProfile
    HEB340: IProfile
    HEB360: IProfile
    HEB400: IProfile
    HEB450: IProfile
    HEB500: IProfile
    HEB550: IProfile
    HEB600: IProfile
    HEB650: IProfile
    HEB700: IProfile
    HEB800: IProfile
    HEB900: IProfile
    HEB1000: IProfile

class __HEBProfileParameters:
    name: str
    top_flange_width: MM
    top_flange_thickness: MM
    bottom_flange_width: MM
    bottom_flange_thickness: MM
    total_height: MM
    web_thickness: MM
    top_radius: MM
    bottom_radius: MM

HEB_PROFILES_DATABASE: dict[str, __HEBProfileParameters]

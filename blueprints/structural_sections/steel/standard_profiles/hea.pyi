from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.type_alias import MM

class HEA:
    HEA100: IProfile
    HEA120: IProfile
    HEA140: IProfile
    HEA160: IProfile
    HEA180: IProfile
    HEA200: IProfile
    HEA220: IProfile
    HEA240: IProfile
    HEA260: IProfile
    HEA280: IProfile
    HEA300: IProfile
    HEA320: IProfile
    HEA340: IProfile
    HEA360: IProfile
    HEA400: IProfile
    HEA450: IProfile
    HEA500: IProfile
    HEA550: IProfile
    HEA600: IProfile
    HEA650: IProfile
    HEA700: IProfile
    HEA800: IProfile
    HEA900: IProfile
    HEA1000: IProfile

class __HEAProfileParameters:
    name: str
    top_flange_width: MM
    top_flange_thickness: MM
    bottom_flange_width: MM
    bottom_flange_thickness: MM
    total_height: MM
    web_thickness: MM
    top_radius: MM
    bottom_radius: MM

HEA_PROFILES_DATABASE: dict[str, __HEAProfileParameters]

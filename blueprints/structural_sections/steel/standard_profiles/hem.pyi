from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.type_alias import MM

class HEM:
    HEM100: IProfile
    HEM120: IProfile
    HEM140: IProfile
    HEM160: IProfile
    HEM180: IProfile
    HEM200: IProfile
    HEM220: IProfile
    HEM240: IProfile
    HEM260: IProfile
    HEM280: IProfile
    HEM300: IProfile
    HEM320: IProfile
    HEM340: IProfile
    HEM360: IProfile
    HEM400: IProfile
    HEM450: IProfile
    HEM500: IProfile
    HEM550: IProfile
    HEM600: IProfile
    HEM650: IProfile
    HEM700: IProfile
    HEM800: IProfile
    HEM900: IProfile
    HEM1000: IProfile

class __HEMProfileParameters:
    name: str
    top_flange_width: MM
    top_flange_thickness: MM
    bottom_flange_width: MM
    bottom_flange_thickness: MM
    total_height: MM
    web_thickness: MM
    top_radius: MM
    bottom_radius: MM

HEM_PROFILES_DATABASE: dict[str, __HEMProfileParameters]

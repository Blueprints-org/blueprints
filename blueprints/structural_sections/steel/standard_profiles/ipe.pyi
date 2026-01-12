from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.type_alias import MM

class IPE:
    IPE80: IProfile
    IPE100: IProfile
    IPE120: IProfile
    IPE140: IProfile
    IPE160: IProfile
    IPE180: IProfile
    IPE200: IProfile
    IPE220: IProfile
    IPE240: IProfile
    IPE270: IProfile
    IPE300: IProfile
    IPE330: IProfile
    IPE360: IProfile
    IPE400: IProfile
    IPE450: IProfile
    IPE500: IProfile
    IPE550: IProfile
    IPE600: IProfile

class __IPEProfileParameters:
    name: str
    top_flange_width: MM
    top_flange_thickness: MM
    bottom_flange_width: MM
    bottom_flange_thickness: MM
    total_height: MM
    web_thickness: MM
    top_radius: MM
    bottom_radius: MM

IPE_PROFILES_DATABASE: dict[str, __IPEProfileParameters]

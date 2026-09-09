from blueprints.structural_sections.steel.profile_definitions.sheetpile_u_profile import SheetpileUProfile
from blueprints.type_alias import MM

class PU:
    PU12: SheetpileUProfile
    PU18: SheetpileUProfile
    PU22: SheetpileUProfile
    PU28: SheetpileUProfile
    PU32: SheetpileUProfile

class __PUProfileParameters:
    name: str
    coordinates: list[tuple[float, float]]
    web_thickness: MM
    flange_thickness: MM
    interlocking_ctc: MM

PU_PROFILES_DATABASE: dict[str, __PUProfileParameters]

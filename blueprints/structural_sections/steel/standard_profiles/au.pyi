from blueprints.structural_sections.steel.profile_definitions.sheetpile_u_profile import SheetpileUProfile
from blueprints.type_alias import MM

class AU:
    AU14: SheetpileUProfile
    AU16: SheetpileUProfile
    AU18: SheetpileUProfile
    AU20: SheetpileUProfile
    AU23: SheetpileUProfile
    AU25: SheetpileUProfile

class __AUProfileParameters:
    name: str
    coordinates: list[tuple[float, float]]
    web_thickness: MM
    flange_thickness: MM
    interlocking_ctc: MM

AU_PROFILES_DATABASE: dict[str, __AUProfileParameters]

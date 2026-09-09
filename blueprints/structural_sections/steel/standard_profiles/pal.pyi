from blueprints.structural_sections.steel.profile_definitions.sheetpile_u_profile import SheetpileUProfile
from blueprints.type_alias import MM

class PAL:
    PAL3030: SheetpileUProfile
    PAL3040: SheetpileUProfile
    PAL3050: SheetpileUProfile
    PAL3130: SheetpileUProfile
    PAL3140: SheetpileUProfile
    PAL3150: SheetpileUProfile

class __PALProfileParameters:
    name: str
    coordinates: list[tuple[float, float]]
    web_thickness: MM
    flange_thickness: MM
    interlocking_ctc: MM

PAL_PROFILES_DATABASE: dict[str, __PALProfileParameters]

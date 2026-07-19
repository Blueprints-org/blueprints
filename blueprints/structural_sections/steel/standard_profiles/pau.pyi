from blueprints.structural_sections.steel.profile_definitions.sheetpile_u_profile import SheetpileUProfile
from blueprints.type_alias import MM

class PAU:
    PAU2240: SheetpileUProfile
    PAU2250: SheetpileUProfile
    PAU2260: SheetpileUProfile
    PAU2440: SheetpileUProfile
    PAU2450: SheetpileUProfile
    PAU2460: SheetpileUProfile
    PAU2770: SheetpileUProfile
    PAU2780: SheetpileUProfile

class __PAUProfileParameters:
    name: str
    coordinates: list[tuple[float, float]]
    web_thickness: MM
    flange_thickness: MM
    interlocking_ctc: MM

PAU_PROFILES_DATABASE: dict[str, __PAUProfileParameters]

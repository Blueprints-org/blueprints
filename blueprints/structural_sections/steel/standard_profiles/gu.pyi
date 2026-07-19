from blueprints.structural_sections.steel.profile_definitions.sheetpile_u_profile import SheetpileUProfile
from blueprints.type_alias import MM

class GU:
    GU6: SheetpileUProfile
    GU7: SheetpileUProfile
    GU8: SheetpileUProfile
    GU10: SheetpileUProfile
    GU11: SheetpileUProfile
    GU12: SheetpileUProfile
    GU13: SheetpileUProfile
    GU14: SheetpileUProfile
    GU15: SheetpileUProfile
    GU16: SheetpileUProfile
    GU18: SheetpileUProfile
    GU18_400: SheetpileUProfile
    GU20: SheetpileUProfile
    GU21: SheetpileUProfile
    GU22: SheetpileUProfile
    GU23: SheetpileUProfile
    GU27: SheetpileUProfile
    GU28: SheetpileUProfile
    GU30: SheetpileUProfile
    GU31: SheetpileUProfile
    GU32: SheetpileUProfile
    GU33: SheetpileUProfile

class __GUProfileParameters:
    name: str
    coordinates: list[tuple[float, float]]
    web_thickness: MM
    flange_thickness: MM
    interlocking_ctc: MM

GU_PROFILES_DATABASE: dict[str, __GUProfileParameters]

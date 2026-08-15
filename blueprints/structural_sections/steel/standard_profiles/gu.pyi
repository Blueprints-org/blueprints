from blueprints.structural_sections.steel.profile_definitions.sheetpile_u_profile import SheetpileUProfile
from blueprints.type_alias import MM

class GU:
    GU6N: SheetpileUProfile
    GU7S: SheetpileUProfile
    GU8S: SheetpileUProfile
    GU10N: SheetpileUProfile
    GU11N: SheetpileUProfile
    GU12N: SheetpileUProfile
    GU13N: SheetpileUProfile
    GU14N: SheetpileUProfile
    GU15N: SheetpileUProfile
    GU16N: SheetpileUProfile
    GU18N: SheetpileUProfile
    GU18_400: SheetpileUProfile
    GU20N: SheetpileUProfile
    GU21N: SheetpileUProfile
    GU22N: SheetpileUProfile
    GU23N: SheetpileUProfile
    GU27N: SheetpileUProfile
    GU28N: SheetpileUProfile
    GU30N: SheetpileUProfile
    GU31N: SheetpileUProfile
    GU32N: SheetpileUProfile
    GU33N: SheetpileUProfile

class __GUProfileParameters:
    name: str
    coordinates: list[tuple[float, float]]
    web_thickness: MM
    flange_thickness: MM
    interlocking_ctc: MM

GU_PROFILES_DATABASE: dict[str, __GUProfileParameters]

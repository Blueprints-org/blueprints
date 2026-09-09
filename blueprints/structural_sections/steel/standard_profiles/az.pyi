from blueprints.structural_sections.steel.profile_definitions.sheetpile_z_profile import SheetpileZProfile
from blueprints.type_alias import MM

class AZ:
    AZ12_700: SheetpileZProfile
    AZ12_770: SheetpileZProfile
    AZ13_700: SheetpileZProfile
    AZ13_700_10_10: SheetpileZProfile
    AZ13_770: SheetpileZProfile
    AZ14_700: SheetpileZProfile
    AZ14_770: SheetpileZProfile
    AZ14_770_10_10: SheetpileZProfile
    AZ17_700: SheetpileZProfile
    AZ18: SheetpileZProfile
    AZ18_10_10: SheetpileZProfile
    AZ18_700: SheetpileZProfile
    AZ18_800: SheetpileZProfile
    AZ19_700: SheetpileZProfile
    AZ20_700: SheetpileZProfile
    AZ22_800: SheetpileZProfile
    AZ24_700: SheetpileZProfile
    AZ25_800: SheetpileZProfile
    AZ26: SheetpileZProfile
    AZ26_700: SheetpileZProfile
    AZ27_800: SheetpileZProfile
    AZ28_700: SheetpileZProfile
    AZ28_750: SheetpileZProfile
    AZ30_750: SheetpileZProfile
    AZ32_750: SheetpileZProfile
    AZ36_700N: SheetpileZProfile
    AZ38_700N: SheetpileZProfile
    AZ40_700N: SheetpileZProfile
    AZ42_700N: SheetpileZProfile
    AZ44_700N: SheetpileZProfile
    AZ46_700N: SheetpileZProfile
    AZ48_700: SheetpileZProfile
    AZ50_700: SheetpileZProfile
    AZ52_700: SheetpileZProfile

class __AZProfileParameters:
    name: str
    coordinates: list[tuple[float, float]]
    web_thickness: MM
    flange_thickness: MM
    interlocking_ctc: MM

AZ_PROFILES_DATABASE: dict[str, __AZProfileParameters]

from blueprints.structural_sections.steel.profile_definitions.az_profile import AZProfile
from blueprints.type_alias import MM

class AZ:
    AZ12_700: AZProfile
    AZ12_770: AZProfile
    AZ13_700: AZProfile
    AZ13_700_10_10: AZProfile
    AZ13_770: AZProfile
    AZ14_700: AZProfile
    AZ14_770: AZProfile
    AZ14_770_10_10: AZProfile
    AZ17_700: AZProfile
    AZ18: AZProfile
    AZ18_10_10: AZProfile
    AZ18_700: AZProfile
    AZ18_800: AZProfile
    AZ19_700: AZProfile
    AZ20_700: AZProfile
    AZ22_800: AZProfile
    AZ24_700: AZProfile
    AZ25_800: AZProfile
    AZ26: AZProfile
    AZ26_700: AZProfile
    AZ27_800: AZProfile
    AZ28_700: AZProfile
    AZ28_750: AZProfile
    AZ30_750: AZProfile
    AZ32_750: AZProfile
    AZ36_700: AZProfile
    AZ38_700: AZProfile
    AZ40_700: AZProfile
    AZ42_700: AZProfile
    AZ44_700: AZProfile
    AZ46_700: AZProfile
    AZ48_700: AZProfile
    AZ50_700: AZProfile
    AZ52_700: AZProfile

class __AZProfileParameters:
    name: str
    coordinates: list[tuple[float, float]]
    web_thickness: MM
    flange_thickness: MM
    interlocking_ctc: MM

AZ_PROFILES_DATABASE: dict[str, __AZProfileParameters]

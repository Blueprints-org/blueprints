from blueprints.structural_sections.steel.profile_definitions.sheetpile_z_profile import SheetpileZProfile
from blueprints.type_alias import MM

class PAZ:
    PAZ4350: SheetpileZProfile
    PAZ4360: SheetpileZProfile
    PAZ4370: SheetpileZProfile
    PAZ4450: SheetpileZProfile
    PAZ4460: SheetpileZProfile
    PAZ4470: SheetpileZProfile
    PAZ4550: SheetpileZProfile
    PAZ4560: SheetpileZProfile
    PAZ4570: SheetpileZProfile
    PAZ4660: SheetpileZProfile
    PAZ4670: SheetpileZProfile
    PAZ5360: SheetpileZProfile
    PAZ5370: SheetpileZProfile
    PAZ5380: SheetpileZProfile
    PAZ5390: SheetpileZProfile
    PAZ54100: SheetpileZProfile
    PAZ5460: SheetpileZProfile
    PAZ5470: SheetpileZProfile
    PAZ5480: SheetpileZProfile
    PAZ5490: SheetpileZProfile
    PAZ55100: SheetpileZProfile
    PAZ5560: SheetpileZProfile
    PAZ5570: SheetpileZProfile
    PAZ5580: SheetpileZProfile
    PAZ5590: SheetpileZProfile
    PAZ56100: SheetpileZProfile
    PAZ5660: SheetpileZProfile
    PAZ5670: SheetpileZProfile
    PAZ5680: SheetpileZProfile
    PAZ5690: SheetpileZProfile

class __PAZProfileParameters:
    name: str
    coordinates: list[tuple[float, float]]
    web_thickness: MM
    flange_thickness: MM
    interlocking_ctc: MM

PAZ_PROFILES_DATABASE: dict[str, __PAZProfileParameters]

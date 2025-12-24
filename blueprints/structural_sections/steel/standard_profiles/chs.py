"""Standard CHS profiles."""

from blueprints.structural_sections.steel.profile_definitions.chs_profile import CHSProfile
from blueprints.structural_sections.steel.standard_profiles.utils import StandardProfileMeta

CHS_PROFILES = {
    "CHS21_3x2_3": {
        "name": "CHS 21.3x2.3",
        "outer_diameter": 21.3,
        "wall_thickness": 2.3,
    },
    "CHS21_3x2_6": {
        "name": "CHS 21.3x2.6",
        "outer_diameter": 21.3,
        "wall_thickness": 2.6,
    },
    "CHS21_3x3_2": {
        "name": "CHS 21.3x3.2",
        "outer_diameter": 21.3,
        "wall_thickness": 3.2,
    },
    "CHS26_9x2_3": {
        "name": "CHS 26.9x2.3",
        "outer_diameter": 26.9,
        "wall_thickness": 2.3,
    },
    "CHS26_9x2_6": {
        "name": "CHS 26.9x2.6",
        "outer_diameter": 26.9,
        "wall_thickness": 2.6,
    },
    "CHS26_9x3_2": {
        "name": "CHS 26.9x3.2",
        "outer_diameter": 26.9,
        "wall_thickness": 3.2,
    },
    "CHS33_7x2_6": {
        "name": "CHS 33.7x2.6",
        "outer_diameter": 33.7,
        "wall_thickness": 2.6,
    },
    "CHS33_7x3_2": {
        "name": "CHS 33.7x3.2",
        "outer_diameter": 33.7,
        "wall_thickness": 3.2,
    },
    "CHS33_7x4": {
        "name": "CHS 33.7x4",
        "outer_diameter": 33.7,
        "wall_thickness": 4,
    },
    "CHS42_4x2_6": {
        "name": "CHS 42.4x2.6",
        "outer_diameter": 42.4,
        "wall_thickness": 2.6,
    },
    "CHS42_4x3_2": {
        "name": "CHS 42.4x3.2",
        "outer_diameter": 42.4,
        "wall_thickness": 3.2,
    },
    "CHS42_4x4": {
        "name": "CHS 42.4x4",
        "outer_diameter": 42.4,
        "wall_thickness": 4,
    },
    "CHS48_3x2_6": {
        "name": "CHS 48.3x2.6",
        "outer_diameter": 48.3,
        "wall_thickness": 2.6,
    },
    "CHS48_3x3_2": {
        "name": "CHS 48.3x3.2",
        "outer_diameter": 48.3,
        "wall_thickness": 3.2,
    },
    "CHS48_3x4": {
        "name": "CHS 48.3x4",
        "outer_diameter": 48.3,
        "wall_thickness": 4,
    },
    "CHS48_3x5": {
        "name": "CHS 48.3x5",
        "outer_diameter": 48.3,
        "wall_thickness": 5,
    },
    "CHS60_3x2_6": {
        "name": "CHS 60.3x2.6",
        "outer_diameter": 60.3,
        "wall_thickness": 2.6,
    },
    "CHS60_3x3_2": {
        "name": "CHS 60.3x3.2",
        "outer_diameter": 60.3,
        "wall_thickness": 3.2,
    },
    "CHS60_3x4": {
        "name": "CHS 60.3x4",
        "outer_diameter": 60.3,
        "wall_thickness": 4,
    },
    "CHS60_3x5": {
        "name": "CHS 60.3x5",
        "outer_diameter": 60.3,
        "wall_thickness": 5,
    },
    "CHS76_1x2_6": {
        "name": "CHS 76.1x2.6",
        "outer_diameter": 76.1,
        "wall_thickness": 2.6,
    },
    "CHS76_1x3_2": {
        "name": "CHS 76.1x3.2",
        "outer_diameter": 76.1,
        "wall_thickness": 3.2,
    },
    "CHS76_1x4": {
        "name": "CHS 76.1x4",
        "outer_diameter": 76.1,
        "wall_thickness": 4,
    },
    "CHS76_1x5": {
        "name": "CHS 76.1x5",
        "outer_diameter": 76.1,
        "wall_thickness": 5,
    },
    "CHS88_9x3_2": {
        "name": "CHS 88.9x3.2",
        "outer_diameter": 88.9,
        "wall_thickness": 3.2,
    },
    "CHS88_9x4": {
        "name": "CHS 88.9x4",
        "outer_diameter": 88.9,
        "wall_thickness": 4,
    },
    "CHS88_9x5": {
        "name": "CHS 88.9x5",
        "outer_diameter": 88.9,
        "wall_thickness": 5,
    },
    "CHS88_9x6_3": {
        "name": "CHS 88.9x6.3",
        "outer_diameter": 88.9,
        "wall_thickness": 6.3,
    },
    "CHS101_6x3_2": {
        "name": "CHS 101.6x3.2",
        "outer_diameter": 101.6,
        "wall_thickness": 3.2,
    },
    "CHS101_6x4": {
        "name": "CHS 101.6x4",
        "outer_diameter": 101.6,
        "wall_thickness": 4,
    },
    "CHS101_6x5": {
        "name": "CHS 101.6x5",
        "outer_diameter": 101.6,
        "wall_thickness": 5,
    },
    "CHS101_6x6_3": {
        "name": "CHS 101.6x6.3",
        "outer_diameter": 101.6,
        "wall_thickness": 6.3,
    },
    "CHS101_6x8": {
        "name": "CHS 101.6x8",
        "outer_diameter": 101.6,
        "wall_thickness": 8,
    },
    "CHS101_6x10": {
        "name": "CHS 101.6x10",
        "outer_diameter": 101.6,
        "wall_thickness": 10,
    },
    "CHS114_3x3_2": {
        "name": "CHS 114.3x3.2",
        "outer_diameter": 114.3,
        "wall_thickness": 3.2,
    },
    "CHS114_3x4": {
        "name": "CHS 114.3x4",
        "outer_diameter": 114.3,
        "wall_thickness": 4,
    },
    "CHS114_3x5": {
        "name": "CHS 114.3x5",
        "outer_diameter": 114.3,
        "wall_thickness": 5,
    },
    "CHS114_3x6_3": {
        "name": "CHS 114.3x6.3",
        "outer_diameter": 114.3,
        "wall_thickness": 6.3,
    },
    "CHS114_3x8": {
        "name": "CHS 114.3x8",
        "outer_diameter": 114.3,
        "wall_thickness": 8,
    },
    "CHS114_3x10": {
        "name": "CHS 114.3x10",
        "outer_diameter": 114.3,
        "wall_thickness": 10,
    },
    "CHS139_7x4": {
        "name": "CHS 139.7x4",
        "outer_diameter": 139.7,
        "wall_thickness": 4,
    },
    "CHS139_7x5": {
        "name": "CHS 139.7x5",
        "outer_diameter": 139.7,
        "wall_thickness": 5,
    },
    "CHS139_7x6_3": {
        "name": "CHS 139.7x6.3",
        "outer_diameter": 139.7,
        "wall_thickness": 6.3,
    },
    "CHS139_7x8": {
        "name": "CHS 139.7x8",
        "outer_diameter": 139.7,
        "wall_thickness": 8,
    },
    "CHS139_7x10": {
        "name": "CHS 139.7x10",
        "outer_diameter": 139.7,
        "wall_thickness": 10,
    },
    "CHS139_7x12_5": {
        "name": "CHS 139.7x12.5",
        "outer_diameter": 139.7,
        "wall_thickness": 12.5,
    },
    "CHS168_3x4": {
        "name": "CHS 168.3x4",
        "outer_diameter": 168.3,
        "wall_thickness": 4,
    },
    "CHS168_3x5": {
        "name": "CHS 168.3x5",
        "outer_diameter": 168.3,
        "wall_thickness": 5,
    },
    "CHS168_3x6_3": {
        "name": "CHS 168.3x6.3",
        "outer_diameter": 168.3,
        "wall_thickness": 6.3,
    },
    "CHS168_3x8": {
        "name": "CHS 168.3x8",
        "outer_diameter": 168.3,
        "wall_thickness": 8,
    },
    "CHS168_3x10": {
        "name": "CHS 168.3x10",
        "outer_diameter": 168.3,
        "wall_thickness": 10,
    },
    "CHS168_3x12_5": {
        "name": "CHS 168.3x12.5",
        "outer_diameter": 168.3,
        "wall_thickness": 12.5,
    },
    "CHS177_8x5": {
        "name": "CHS 177.8x5",
        "outer_diameter": 177.8,
        "wall_thickness": 5,
    },
    "CHS177_8x6_3": {
        "name": "CHS 177.8x6.3",
        "outer_diameter": 177.8,
        "wall_thickness": 6.3,
    },
    "CHS177_8x8": {
        "name": "CHS 177.8x8",
        "outer_diameter": 177.8,
        "wall_thickness": 8,
    },
    "CHS177_8x10": {
        "name": "CHS 177.8x10",
        "outer_diameter": 177.8,
        "wall_thickness": 10,
    },
    "CHS177_8x12_5": {
        "name": "CHS 177.8x12.5",
        "outer_diameter": 177.8,
        "wall_thickness": 12.5,
    },
    "CHS193_7x5": {
        "name": "CHS 193.7x5",
        "outer_diameter": 193.7,
        "wall_thickness": 5,
    },
    "CHS193_7x6_3": {
        "name": "CHS 193.7x6.3",
        "outer_diameter": 193.7,
        "wall_thickness": 6.3,
    },
    "CHS193_7x8": {
        "name": "CHS 193.7x8",
        "outer_diameter": 193.7,
        "wall_thickness": 8,
    },
    "CHS193_7x10": {
        "name": "CHS 193.7x10",
        "outer_diameter": 193.7,
        "wall_thickness": 10,
    },
    "CHS193_7x12_5": {
        "name": "CHS 193.7x12.5",
        "outer_diameter": 193.7,
        "wall_thickness": 12.5,
    },
    "CHS193_7x14_2": {
        "name": "CHS 193.7x14.2",
        "outer_diameter": 193.7,
        "wall_thickness": 14.2,
    },
    "CHS193_7x16": {
        "name": "CHS 193.7x16",
        "outer_diameter": 193.7,
        "wall_thickness": 16,
    },
    "CHS219_1x5": {
        "name": "CHS 219.1x5",
        "outer_diameter": 219.1,
        "wall_thickness": 5,
    },
    "CHS219_1x6_3": {
        "name": "CHS 219.1x6.3",
        "outer_diameter": 219.1,
        "wall_thickness": 6.3,
    },
    "CHS219_1x8": {
        "name": "CHS 219.1x8",
        "outer_diameter": 219.1,
        "wall_thickness": 8,
    },
    "CHS219_1x10": {
        "name": "CHS 219.1x10",
        "outer_diameter": 219.1,
        "wall_thickness": 10,
    },
    "CHS219_1x12_5": {
        "name": "CHS 219.1x12.5",
        "outer_diameter": 219.1,
        "wall_thickness": 12.5,
    },
    "CHS219_1x14_2": {
        "name": "CHS 219.1x14.2",
        "outer_diameter": 219.1,
        "wall_thickness": 14.2,
    },
    "CHS219_1x16": {
        "name": "CHS 219.1x16",
        "outer_diameter": 219.1,
        "wall_thickness": 16,
    },
    "CHS219_1x20": {
        "name": "CHS 219.1x20",
        "outer_diameter": 219.1,
        "wall_thickness": 20,
    },
    "CHS244_5x5": {
        "name": "CHS 244.5x5",
        "outer_diameter": 244.5,
        "wall_thickness": 5,
    },
    "CHS244_5x6_3": {
        "name": "CHS 244.5x6.3",
        "outer_diameter": 244.5,
        "wall_thickness": 6.3,
    },
    "CHS244_5x8": {
        "name": "CHS 244.5x8",
        "outer_diameter": 244.5,
        "wall_thickness": 8,
    },
    "CHS244_5x10": {
        "name": "CHS 244.5x10",
        "outer_diameter": 244.5,
        "wall_thickness": 10,
    },
    "CHS244_5x12_5": {
        "name": "CHS 244.5x12.5",
        "outer_diameter": 244.5,
        "wall_thickness": 12.5,
    },
    "CHS244_5x14_2": {
        "name": "CHS 244.5x14.2",
        "outer_diameter": 244.5,
        "wall_thickness": 14.2,
    },
    "CHS244_5x16": {
        "name": "CHS 244.5x16",
        "outer_diameter": 244.5,
        "wall_thickness": 16,
    },
    "CHS244_5x20": {
        "name": "CHS 244.5x20",
        "outer_diameter": 244.5,
        "wall_thickness": 20,
    },
    "CHS244_5x25": {
        "name": "CHS 244.5x25",
        "outer_diameter": 244.5,
        "wall_thickness": 25,
    },
    "CHS273x5": {
        "name": "CHS 273x5",
        "outer_diameter": 273,
        "wall_thickness": 5,
    },
    "CHS273x6_3": {
        "name": "CHS 273x6.3",
        "outer_diameter": 273,
        "wall_thickness": 6.3,
    },
    "CHS273x8": {
        "name": "CHS 273x8",
        "outer_diameter": 273,
        "wall_thickness": 8,
    },
    "CHS273x10": {
        "name": "CHS 273x10",
        "outer_diameter": 273,
        "wall_thickness": 10,
    },
    "CHS273x12_5": {
        "name": "CHS 273x12.5",
        "outer_diameter": 273,
        "wall_thickness": 12.5,
    },
    "CHS273x14_2": {
        "name": "CHS 273x14.2",
        "outer_diameter": 273,
        "wall_thickness": 14.2,
    },
    "CHS273x16": {
        "name": "CHS 273x16",
        "outer_diameter": 273,
        "wall_thickness": 16,
    },
    "CHS273x20": {
        "name": "CHS 273x20",
        "outer_diameter": 273,
        "wall_thickness": 20,
    },
    "CHS273x25": {
        "name": "CHS 273x25",
        "outer_diameter": 273,
        "wall_thickness": 25,
    },
    "CHS323_9x5": {
        "name": "CHS 323.9x5",
        "outer_diameter": 323.9,
        "wall_thickness": 5,
    },
    "CHS323_9x6_3": {
        "name": "CHS 323.9x6.3",
        "outer_diameter": 323.9,
        "wall_thickness": 6.3,
    },
    "CHS323_9x8": {
        "name": "CHS 323.9x8",
        "outer_diameter": 323.9,
        "wall_thickness": 8,
    },
    "CHS323_9x10": {
        "name": "CHS 323.9x10",
        "outer_diameter": 323.9,
        "wall_thickness": 10,
    },
    "CHS323_9x12_5": {
        "name": "CHS 323.9x12.5",
        "outer_diameter": 323.9,
        "wall_thickness": 12.5,
    },
    "CHS323_9x14_2": {
        "name": "CHS 323.9x14.2",
        "outer_diameter": 323.9,
        "wall_thickness": 14.2,
    },
    "CHS323_9x16": {
        "name": "CHS 323.9x16",
        "outer_diameter": 323.9,
        "wall_thickness": 16,
    },
    "CHS323_9x20": {
        "name": "CHS 323.9x20",
        "outer_diameter": 323.9,
        "wall_thickness": 20,
    },
    "CHS323_9x25": {
        "name": "CHS 323.9x25",
        "outer_diameter": 323.9,
        "wall_thickness": 25,
    },
    "CHS355_6x6_3": {
        "name": "CHS 355.6x6.3",
        "outer_diameter": 355.6,
        "wall_thickness": 6.3,
    },
    "CHS355_6x8": {
        "name": "CHS 355.6x8",
        "outer_diameter": 355.6,
        "wall_thickness": 8,
    },
    "CHS355_6x10": {
        "name": "CHS 355.6x10",
        "outer_diameter": 355.6,
        "wall_thickness": 10,
    },
    "CHS355_6x12_5": {
        "name": "CHS 355.6x12.5",
        "outer_diameter": 355.6,
        "wall_thickness": 12.5,
    },
    "CHS355_6x14_2": {
        "name": "CHS 355.6x14.2",
        "outer_diameter": 355.6,
        "wall_thickness": 14.2,
    },
    "CHS355_6x16": {
        "name": "CHS 355.6x16",
        "outer_diameter": 355.6,
        "wall_thickness": 16,
    },
    "CHS355_6x20": {
        "name": "CHS 355.6x20",
        "outer_diameter": 355.6,
        "wall_thickness": 20,
    },
    "CHS355_6x25": {
        "name": "CHS 355.6x25",
        "outer_diameter": 355.6,
        "wall_thickness": 25,
    },
    "CHS406_4x6_3": {
        "name": "CHS 406.4x6.3",
        "outer_diameter": 406.4,
        "wall_thickness": 6.3,
    },
    "CHS406_4x8": {
        "name": "CHS 406.4x8",
        "outer_diameter": 406.4,
        "wall_thickness": 8,
    },
    "CHS406_4x10": {
        "name": "CHS 406.4x10",
        "outer_diameter": 406.4,
        "wall_thickness": 10,
    },
    "CHS406_4x12_5": {
        "name": "CHS 406.4x12.5",
        "outer_diameter": 406.4,
        "wall_thickness": 12.5,
    },
    "CHS406_4x14_2": {
        "name": "CHS 406.4x14.2",
        "outer_diameter": 406.4,
        "wall_thickness": 14.2,
    },
    "CHS406_4x16": {
        "name": "CHS 406.4x16",
        "outer_diameter": 406.4,
        "wall_thickness": 16,
    },
    "CHS406_4x20": {
        "name": "CHS 406.4x20",
        "outer_diameter": 406.4,
        "wall_thickness": 20,
    },
    "CHS406_4x25": {
        "name": "CHS 406.4x25",
        "outer_diameter": 406.4,
        "wall_thickness": 25,
    },
    "CHS406_4x30": {
        "name": "CHS 406.4x30",
        "outer_diameter": 406.4,
        "wall_thickness": 30,
    },
    "CHS406_4x40": {
        "name": "CHS 406.4x40",
        "outer_diameter": 406.4,
        "wall_thickness": 40,
    },
    "CHS457x6_3": {
        "name": "CHS 457x6.3",
        "outer_diameter": 457,
        "wall_thickness": 6.3,
    },
    "CHS457x8": {
        "name": "CHS 457x8",
        "outer_diameter": 457,
        "wall_thickness": 8,
    },
    "CHS457x10": {
        "name": "CHS 457x10",
        "outer_diameter": 457,
        "wall_thickness": 10,
    },
    "CHS457x12_5": {
        "name": "CHS 457x12.5",
        "outer_diameter": 457,
        "wall_thickness": 12.5,
    },
    "CHS457x14_2": {
        "name": "CHS 457x14.2",
        "outer_diameter": 457,
        "wall_thickness": 14.2,
    },
    "CHS457x16": {
        "name": "CHS 457x16",
        "outer_diameter": 457,
        "wall_thickness": 16,
    },
    "CHS457x20": {
        "name": "CHS 457x20",
        "outer_diameter": 457,
        "wall_thickness": 20,
    },
    "CHS457x25": {
        "name": "CHS 457x25",
        "outer_diameter": 457,
        "wall_thickness": 25,
    },
    "CHS457x30": {
        "name": "CHS 457x30",
        "outer_diameter": 457,
        "wall_thickness": 30,
    },
    "CHS457x40": {
        "name": "CHS 457x40",
        "outer_diameter": 457,
        "wall_thickness": 40,
    },
    "CHS508x6_3": {
        "name": "CHS 508x6.3",
        "outer_diameter": 508,
        "wall_thickness": 6.3,
    },
    "CHS508x8": {
        "name": "CHS 508x8",
        "outer_diameter": 508,
        "wall_thickness": 8,
    },
    "CHS508x10": {
        "name": "CHS 508x10",
        "outer_diameter": 508,
        "wall_thickness": 10,
    },
    "CHS508x12_5": {
        "name": "CHS 508x12.5",
        "outer_diameter": 508,
        "wall_thickness": 12.5,
    },
    "CHS508x14_2": {
        "name": "CHS 508x14.2",
        "outer_diameter": 508,
        "wall_thickness": 14.2,
    },
    "CHS508x16": {
        "name": "CHS 508x16",
        "outer_diameter": 508,
        "wall_thickness": 16,
    },
    "CHS508x20": {
        "name": "CHS 508x20",
        "outer_diameter": 508,
        "wall_thickness": 20,
    },
    "CHS508x25": {
        "name": "CHS 508x25",
        "outer_diameter": 508,
        "wall_thickness": 25,
    },
    "CHS508x30": {
        "name": "CHS 508x30",
        "outer_diameter": 508,
        "wall_thickness": 30,
    },
    "CHS508x40": {
        "name": "CHS 508x40",
        "outer_diameter": 508,
        "wall_thickness": 40,
    },
    "CHS610x6_3": {
        "name": "CHS 610x6.3",
        "outer_diameter": 610,
        "wall_thickness": 6.3,
    },
    "CHS610x8": {
        "name": "CHS 610x8",
        "outer_diameter": 610,
        "wall_thickness": 8,
    },
    "CHS610x10": {
        "name": "CHS 610x10",
        "outer_diameter": 610,
        "wall_thickness": 10,
    },
    "CHS610x12_5": {
        "name": "CHS 610x12.5",
        "outer_diameter": 610,
        "wall_thickness": 12.5,
    },
    "CHS610x14_2": {
        "name": "CHS 610x14.2",
        "outer_diameter": 610,
        "wall_thickness": 14.2,
    },
    "CHS610x16": {
        "name": "CHS 610x16",
        "outer_diameter": 610,
        "wall_thickness": 16,
    },
    "CHS610x20": {
        "name": "CHS 610x20",
        "outer_diameter": 610,
        "wall_thickness": 20,
    },
    "CHS610x25": {
        "name": "CHS 610x25",
        "outer_diameter": 610,
        "wall_thickness": 25,
    },
    "CHS610x30": {
        "name": "CHS 610x30",
        "outer_diameter": 610,
        "wall_thickness": 30,
    },
    "CHS610x40": {
        "name": "CHS 610x40",
        "outer_diameter": 610,
        "wall_thickness": 40,
    },
    "CHS711x6_3": {
        "name": "CHS 711x6.3",
        "outer_diameter": 711,
        "wall_thickness": 6.3,
    },
    "CHS711x8": {
        "name": "CHS 711x8",
        "outer_diameter": 711,
        "wall_thickness": 8,
    },
    "CHS711x10": {
        "name": "CHS 711x10",
        "outer_diameter": 711,
        "wall_thickness": 10,
    },
    "CHS711x12_5": {
        "name": "CHS 711x12.5",
        "outer_diameter": 711,
        "wall_thickness": 12.5,
    },
    "CHS711x14_2": {
        "name": "CHS 711x14.2",
        "outer_diameter": 711,
        "wall_thickness": 14.2,
    },
    "CHS711x16": {
        "name": "CHS 711x16",
        "outer_diameter": 711,
        "wall_thickness": 16,
    },
    "CHS711x20": {
        "name": "CHS 711x20",
        "outer_diameter": 711,
        "wall_thickness": 20,
    },
    "CHS711x25": {
        "name": "CHS 711x25",
        "outer_diameter": 711,
        "wall_thickness": 25,
    },
    "CHS711x30": {
        "name": "CHS 711x30",
        "outer_diameter": 711,
        "wall_thickness": 30,
    },
    "CHS711x40": {
        "name": "CHS 711x40",
        "outer_diameter": 711,
        "wall_thickness": 40,
    },
    "CHS762x6_3": {
        "name": "CHS 762x6.3",
        "outer_diameter": 762,
        "wall_thickness": 6.3,
    },
    "CHS762x8": {
        "name": "CHS 762x8",
        "outer_diameter": 762,
        "wall_thickness": 8,
    },
    "CHS762x10": {
        "name": "CHS 762x10",
        "outer_diameter": 762,
        "wall_thickness": 10,
    },
    "CHS762x12_5": {
        "name": "CHS 762x12.5",
        "outer_diameter": 762,
        "wall_thickness": 12.5,
    },
    "CHS762x14_2": {
        "name": "CHS 762x14.2",
        "outer_diameter": 762,
        "wall_thickness": 14.2,
    },
    "CHS762x16": {
        "name": "CHS 762x16",
        "outer_diameter": 762,
        "wall_thickness": 16,
    },
    "CHS762x20": {
        "name": "CHS 762x20",
        "outer_diameter": 762,
        "wall_thickness": 20,
    },
    "CHS762x25": {
        "name": "CHS 762x25",
        "outer_diameter": 762,
        "wall_thickness": 25,
    },
    "CHS762x30": {
        "name": "CHS 762x30",
        "outer_diameter": 762,
        "wall_thickness": 30,
    },
    "CHS762x40": {
        "name": "CHS 762x40",
        "outer_diameter": 762,
        "wall_thickness": 40,
    },
    "CHS813x8": {
        "name": "CHS 813x8",
        "outer_diameter": 813,
        "wall_thickness": 8,
    },
    "CHS813x10": {
        "name": "CHS 813x10",
        "outer_diameter": 813,
        "wall_thickness": 10,
    },
    "CHS813x12_5": {
        "name": "CHS 813x12.5",
        "outer_diameter": 813,
        "wall_thickness": 12.5,
    },
    "CHS813x14_2": {
        "name": "CHS 813x14.2",
        "outer_diameter": 813,
        "wall_thickness": 14.2,
    },
    "CHS813x16": {
        "name": "CHS 813x16",
        "outer_diameter": 813,
        "wall_thickness": 16,
    },
    "CHS813x20": {
        "name": "CHS 813x20",
        "outer_diameter": 813,
        "wall_thickness": 20,
    },
    "CHS813x25": {
        "name": "CHS 813x25",
        "outer_diameter": 813,
        "wall_thickness": 25,
    },
    "CHS813x30": {
        "name": "CHS 813x30",
        "outer_diameter": 813,
        "wall_thickness": 30,
    },
    "CHS914x8": {
        "name": "CHS 914x8",
        "outer_diameter": 914,
        "wall_thickness": 8,
    },
    "CHS914x10": {
        "name": "CHS 914x10",
        "outer_diameter": 914,
        "wall_thickness": 10,
    },
    "CHS914x12_5": {
        "name": "CHS 914x12.5",
        "outer_diameter": 914,
        "wall_thickness": 12.5,
    },
    "CHS914x14_2": {
        "name": "CHS 914x14.2",
        "outer_diameter": 914,
        "wall_thickness": 14.2,
    },
    "CHS914x16": {
        "name": "CHS 914x16",
        "outer_diameter": 914,
        "wall_thickness": 16,
    },
    "CHS914x20": {
        "name": "CHS 914x20",
        "outer_diameter": 914,
        "wall_thickness": 20,
    },
    "CHS914x25": {
        "name": "CHS 914x25",
        "outer_diameter": 914,
        "wall_thickness": 25,
    },
    "CHS914x30": {
        "name": "CHS 914x30",
        "outer_diameter": 914,
        "wall_thickness": 30,
    },
    "CHS1016x8": {
        "name": "CHS 1016x8",
        "outer_diameter": 1016,
        "wall_thickness": 8,
    },
    "CHS1016x10": {
        "name": "CHS 1016x10",
        "outer_diameter": 1016,
        "wall_thickness": 10,
    },
    "CHS1016x12_5": {
        "name": "CHS 1016x12.5",
        "outer_diameter": 1016,
        "wall_thickness": 12.5,
    },
    "CHS1016x14_2": {
        "name": "CHS 1016x14.2",
        "outer_diameter": 1016,
        "wall_thickness": 14.2,
    },
    "CHS1016x16": {
        "name": "CHS 1016x16",
        "outer_diameter": 1016,
        "wall_thickness": 16,
    },
    "CHS1016x20": {
        "name": "CHS 1016x20",
        "outer_diameter": 1016,
        "wall_thickness": 20,
    },
    "CHS1016x25": {
        "name": "CHS 1016x25",
        "outer_diameter": 1016,
        "wall_thickness": 25,
    },
    "CHS1016x30": {
        "name": "CHS 1016x30",
        "outer_diameter": 1016,
        "wall_thickness": 30,
    },
    "CHS1067x10": {
        "name": "CHS 1067x10",
        "outer_diameter": 1067,
        "wall_thickness": 10,
    },
    "CHS1067x12_5": {
        "name": "CHS 1067x12.5",
        "outer_diameter": 1067,
        "wall_thickness": 12.5,
    },
    "CHS1067x14_2": {
        "name": "CHS 1067x14.2",
        "outer_diameter": 1067,
        "wall_thickness": 14.2,
    },
    "CHS1067x16": {
        "name": "CHS 1067x16",
        "outer_diameter": 1067,
        "wall_thickness": 16,
    },
    "CHS1067x20": {
        "name": "CHS 1067x20",
        "outer_diameter": 1067,
        "wall_thickness": 20,
    },
    "CHS1067x25": {
        "name": "CHS 1067x25",
        "outer_diameter": 1067,
        "wall_thickness": 25,
    },
    "CHS1067x30": {
        "name": "CHS 1067x30",
        "outer_diameter": 1067,
        "wall_thickness": 30,
    },
    "CHS1168x10": {
        "name": "CHS 1168x10",
        "outer_diameter": 1168,
        "wall_thickness": 10,
    },
    "CHS1168x12_5": {
        "name": "CHS 1168x12.5",
        "outer_diameter": 1168,
        "wall_thickness": 12.5,
    },
    "CHS1168x14_2": {
        "name": "CHS 1168x14.2",
        "outer_diameter": 1168,
        "wall_thickness": 14.2,
    },
    "CHS1168x16": {
        "name": "CHS 1168x16",
        "outer_diameter": 1168,
        "wall_thickness": 16,
    },
    "CHS1168x20": {
        "name": "CHS 1168x20",
        "outer_diameter": 1168,
        "wall_thickness": 20,
    },
    "CHS1168x25": {
        "name": "CHS 1168x25",
        "outer_diameter": 1168,
        "wall_thickness": 25,
    },
    "CHS1219x10": {
        "name": "CHS 1219x10",
        "outer_diameter": 1219,
        "wall_thickness": 10,
    },
    "CHS1219x12_5": {
        "name": "CHS 1219x12.5",
        "outer_diameter": 1219,
        "wall_thickness": 12.5,
    },
    "CHS1219x14_2": {
        "name": "CHS 1219x14.2",
        "outer_diameter": 1219,
        "wall_thickness": 14.2,
    },
    "CHS1219x16": {
        "name": "CHS 1219x16",
        "outer_diameter": 1219,
        "wall_thickness": 16,
    },
    "CHS1219x20": {
        "name": "CHS 1219x20",
        "outer_diameter": 1219,
        "wall_thickness": 20,
    },
    "CHS1219x25": {
        "name": "CHS 1219x25",
        "outer_diameter": 1219,
        "wall_thickness": 25,
    },
    "CHS1219x30": {
        "name": "CHS 1219x30",
        "outer_diameter": 1219,
        "wall_thickness": 30,
    },
    "CHS1219x32": {
        "name": "CHS 1219x32",
        "outer_diameter": 1219,
        "wall_thickness": 32,
    },
    "CHS1219x36": {
        "name": "CHS 1219x36",
        "outer_diameter": 1219,
        "wall_thickness": 36,
    },
    "CHS1219x40": {
        "name": "CHS 1219x40",
        "outer_diameter": 1219,
        "wall_thickness": 40,
    },
    "CHS1420x10": {
        "name": "CHS 1420x10",
        "outer_diameter": 1420,
        "wall_thickness": 10,
    },
    "CHS1420x12_5": {
        "name": "CHS 1420x12.5",
        "outer_diameter": 1420,
        "wall_thickness": 12.5,
    },
    "CHS1420x14_2": {
        "name": "CHS 1420x14.2",
        "outer_diameter": 1420,
        "wall_thickness": 14.2,
    },
    "CHS1420x16": {
        "name": "CHS 1420x16",
        "outer_diameter": 1420,
        "wall_thickness": 16,
    },
    "CHS1420x20": {
        "name": "CHS 1420x20",
        "outer_diameter": 1420,
        "wall_thickness": 20,
    },
    "CHS1420x25": {
        "name": "CHS 1420x25",
        "outer_diameter": 1420,
        "wall_thickness": 25,
    },
    "CHS1420x30": {
        "name": "CHS 1420x30",
        "outer_diameter": 1420,
        "wall_thickness": 30,
    },
    "CHS1420x32": {
        "name": "CHS 1420x32",
        "outer_diameter": 1420,
        "wall_thickness": 32,
    },
    "CHS1420x36": {
        "name": "CHS 1420x36",
        "outer_diameter": 1420,
        "wall_thickness": 36,
    },
    "CHS1420x40": {
        "name": "CHS 1420x40",
        "outer_diameter": 1420,
        "wall_thickness": 40,
    },
    "CHS1620x10": {
        "name": "CHS 1620x10",
        "outer_diameter": 1620,
        "wall_thickness": 10,
    },
    "CHS1620x12_5": {
        "name": "CHS 1620x12.5",
        "outer_diameter": 1620,
        "wall_thickness": 12.5,
    },
    "CHS1620x14_2": {
        "name": "CHS 1620x14.2",
        "outer_diameter": 1620,
        "wall_thickness": 14.2,
    },
    "CHS1620x16": {
        "name": "CHS 1620x16",
        "outer_diameter": 1620,
        "wall_thickness": 16,
    },
    "CHS1620x20": {
        "name": "CHS 1620x20",
        "outer_diameter": 1620,
        "wall_thickness": 20,
    },
    "CHS1620x25": {
        "name": "CHS 1620x25",
        "outer_diameter": 1620,
        "wall_thickness": 25,
    },
    "CHS1620x30": {
        "name": "CHS 1620x30",
        "outer_diameter": 1620,
        "wall_thickness": 30,
    },
    "CHS1620x32": {
        "name": "CHS 1620x32",
        "outer_diameter": 1620,
        "wall_thickness": 32,
    },
    "CHS1620x36": {
        "name": "CHS 1620x36",
        "outer_diameter": 1620,
        "wall_thickness": 36,
    },
    "CHS1620x40": {
        "name": "CHS 1620x40",
        "outer_diameter": 1620,
        "wall_thickness": 40,
    },
    "CHS1820x12_5": {
        "name": "CHS 1820x12.5",
        "outer_diameter": 1820,
        "wall_thickness": 12.5,
    },
    "CHS1820x14_2": {
        "name": "CHS 1820x14.2",
        "outer_diameter": 1820,
        "wall_thickness": 14.2,
    },
    "CHS1820x16": {
        "name": "CHS 1820x16",
        "outer_diameter": 1820,
        "wall_thickness": 16,
    },
    "CHS1820x20": {
        "name": "CHS 1820x20",
        "outer_diameter": 1820,
        "wall_thickness": 20,
    },
    "CHS1820x25": {
        "name": "CHS 1820x25",
        "outer_diameter": 1820,
        "wall_thickness": 25,
    },
    "CHS1820x30": {
        "name": "CHS 1820x30",
        "outer_diameter": 1820,
        "wall_thickness": 30,
    },
    "CHS1820x32": {
        "name": "CHS 1820x32",
        "outer_diameter": 1820,
        "wall_thickness": 32,
    },
    "CHS1820x36": {
        "name": "CHS 1820x36",
        "outer_diameter": 1820,
        "wall_thickness": 36,
    },
    "CHS1820x40": {
        "name": "CHS 1820x40",
        "outer_diameter": 1820,
        "wall_thickness": 40,
    },
    "CHS2020x14_2": {
        "name": "CHS 2020x14.2",
        "outer_diameter": 2020,
        "wall_thickness": 14.2,
    },
    "CHS2020x16": {
        "name": "CHS 2020x16",
        "outer_diameter": 2020,
        "wall_thickness": 16,
    },
    "CHS2020x20": {
        "name": "CHS 2020x20",
        "outer_diameter": 2020,
        "wall_thickness": 20,
    },
    "CHS2020x25": {
        "name": "CHS 2020x25",
        "outer_diameter": 2020,
        "wall_thickness": 25,
    },
    "CHS2020x30": {
        "name": "CHS 2020x30",
        "outer_diameter": 2020,
        "wall_thickness": 30,
    },
    "CHS2020x32": {
        "name": "CHS 2020x32",
        "outer_diameter": 2020,
        "wall_thickness": 32,
    },
    "CHS2020x36": {
        "name": "CHS 2020x36",
        "outer_diameter": 2020,
        "wall_thickness": 36,
    },
    "CHS2020x40": {
        "name": "CHS 2020x40",
        "outer_diameter": 2020,
        "wall_thickness": 40,
    },
    "CHS2220x14_2": {
        "name": "CHS 2220x14.2",
        "outer_diameter": 2220,
        "wall_thickness": 14.2,
    },
    "CHS2220x16": {
        "name": "CHS 2220x16",
        "outer_diameter": 2220,
        "wall_thickness": 16,
    },
    "CHS2220x20": {
        "name": "CHS 2220x20",
        "outer_diameter": 2220,
        "wall_thickness": 20,
    },
    "CHS2220x25": {
        "name": "CHS 2220x25",
        "outer_diameter": 2220,
        "wall_thickness": 25,
    },
    "CHS2220x30": {
        "name": "CHS 2220x30",
        "outer_diameter": 2220,
        "wall_thickness": 30,
    },
    "CHS2220x32": {
        "name": "CHS 2220x32",
        "outer_diameter": 2220,
        "wall_thickness": 32,
    },
    "CHS2220x36": {
        "name": "CHS 2220x36",
        "outer_diameter": 2220,
        "wall_thickness": 36,
    },
    "CHS2220x40": {
        "name": "CHS 2220x40",
        "outer_diameter": 2220,
        "wall_thickness": 40,
    },
}


class CHS(metaclass=StandardProfileMeta):
    """Geometrical representation of standard CHS profiles."""

    _factory = CHSProfile
    _database = CHS_PROFILES
    _parameters = ("name", "outer_diameter", "wall_thickness")

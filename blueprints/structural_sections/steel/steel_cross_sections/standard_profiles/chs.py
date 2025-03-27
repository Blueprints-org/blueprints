"""Standard CHS profiles."""

from enum import Enum


class CHSStandardProfileClass(Enum):
    """Enumeration of standard CHS profiles."""

    CHS_21_3x2_3 = "CHS 21.3x2.3"
    CHS_21_3x2_6 = "CHS 21.3x2.6"
    CHS_21_3x3_2 = "CHS 21.3x3.2"
    CHS_26_9x2_3 = "CHS 26.9x2.3"
    CHS_26_9x2_6 = "CHS 26.9x2.6"
    CHS_26_9x3_2 = "CHS 26.9x3.2"
    CHS_33_7x2_6 = "CHS 33.7x2.6"
    CHS_33_7x3_2 = "CHS 33.7x3.2"
    CHS_33_7x4 = "CHS 33.7x4"
    CHS_42_4x2_6 = "CHS 42.4x2.6"
    CHS_42_4x3_2 = "CHS 42.4x3.2"
    CHS_42_4x4 = "CHS 42.4x4"
    CHS_48_3x2_6 = "CHS 48.3x2.6"
    CHS_48_3x3_2 = "CHS 48.3x3.2"
    CHS_48_3x4 = "CHS 48.3x4"
    CHS_48_3x5 = "CHS 48.3x5"
    CHS_60_3x2_6 = "CHS 60.3x2.6"
    CHS_60_3x3_2 = "CHS 60.3x3.2"
    CHS_60_3x4 = "CHS 60.3x4"
    CHS_60_3x5 = "CHS 60.3x5"
    CHS_76_1x2_6 = "CHS 76.1x2.6"
    CHS_76_1x3_2 = "CHS 76.1x3.2"
    CHS_76_1x4 = "CHS 76.1x4"
    CHS_76_1x5 = "CHS 76.1x5"
    CHS_88_9x3_2 = "CHS 88.9x3.2"
    CHS_88_9x4 = "CHS 88.9x4"
    CHS_88_9x5 = "CHS 88.9x5"
    CHS_88_9x6_3 = "CHS 88.9x6.3"
    CHS_101_6x3_2 = "CHS 101.6x3.2"
    CHS_101_6x4 = "CHS 101.6x4"
    CHS_101_6x5 = "CHS 101.6x5"
    CHS_101_6x6_3 = "CHS 101.6x6.3"
    CHS_101_6x8 = "CHS 101.6x8"
    CHS_101_6x10 = "CHS 101.6x10"
    CHS_114_3x3_2 = "CHS 114.3x3.2"
    CHS_114_3x4 = "CHS 114.3x4"
    CHS_114_3x5 = "CHS 114.3x5"
    CHS_114_3x6_3 = "CHS 114.3x6.3"
    CHS_114_3x8 = "CHS 114.3x8"
    CHS_114_3x10 = "CHS 114.3x10"
    CHS_139_7x4 = "CHS 139.7x4"
    CHS_139_7x5 = "CHS 139.7x5"
    CHS_139_7x6_3 = "CHS 139.7x6.3"
    CHS_139_7x8 = "CHS 139.7x8"
    CHS_139_7x10 = "CHS 139.7x10"
    CHS_139_7x12_5 = "CHS 139.7x12.5"
    CHS_168_3x4 = "CHS 168.3x4"
    CHS_168_3x5 = "CHS 168.3x5"
    CHS_168_3x6_3 = "CHS 168.3x6.3"
    CHS_168_3x8 = "CHS 168.3x8"
    CHS_168_3x10 = "CHS 168.3x10"
    CHS_168_3x12_5 = "CHS 168.3x12.5"
    CHS_177_8x5 = "CHS 177.8x5"
    CHS_177_8x6_3 = "CHS 177.8x6.3"
    CHS_177_8x8 = "CHS 177.8x8"
    CHS_177_8x10 = "CHS 177.8x10"
    CHS_177_8x12_5 = "CHS 177.8x12.5"
    CHS_193_7x5 = "CHS 193.7x5"
    CHS_193_7x6_3 = "CHS 193.7x6.3"
    CHS_193_7x8 = "CHS 193.7x8"
    CHS_193_7x10 = "CHS 193.7x10"
    CHS_193_7x12_5 = "CHS 193.7x12.5"
    CHS_193_7x14_2 = "CHS 193.7x14.2"
    CHS_193_7x16 = "CHS 193.7x16"
    CHS_219_1x5 = "CHS 219.1x5"
    CHS_219_1x6_3 = "CHS 219.1x6.3"
    CHS_219_1x8 = "CHS 219.1x8"
    CHS_219_1x10 = "CHS 219.1x10"
    CHS_219_1x12_5 = "CHS 219.1x12.5"
    CHS_219_1x14_2 = "CHS 219.1x14.2"
    CHS_219_1x16 = "CHS 219.1x16"
    CHS_219_1x20 = "CHS 219.1x20"
    CHS_244_5x5 = "CHS 244.5x5"
    CHS_244_5x6_3 = "CHS 244.5x6.3"
    CHS_244_5x8 = "CHS 244.5x8"
    CHS_244_5x10 = "CHS 244.5x10"
    CHS_244_5x12_5 = "CHS 244.5x12.5"
    CHS_244_5x14_2 = "CHS 244.5x14.2"
    CHS_244_5x16 = "CHS 244.5x16"
    CHS_244_5x20 = "CHS 244.5x20"
    CHS_244_5x25 = "CHS 244.5x25"
    CHS_273x5 = "CHS 273x5"
    CHS_273x6_3 = "CHS 273x6.3"
    CHS_273x8 = "CHS 273x8"
    CHS_273x10 = "CHS 273x10"
    CHS_273x12_5 = "CHS 273x12.5"
    CHS_273x14_2 = "CHS 273x14.2"
    CHS_273x16 = "CHS 273x16"
    CHS_273x20 = "CHS 273x20"
    CHS_273x25 = "CHS 273x25"
    CHS_323_9x5 = "CHS 323.9x5"
    CHS_323_9x6_3 = "CHS 323.9x6.3"
    CHS_323_9x8 = "CHS 323.9x8"
    CHS_323_9x10 = "CHS 323.9x10"
    CHS_323_9x12_5 = "CHS 323.9x12.5"
    CHS_323_9x14_2 = "CHS 323.9x14.2"
    CHS_323_9x16 = "CHS 323.9x16"
    CHS_323_9x20 = "CHS 323.9x20"
    CHS_323_9x25 = "CHS 323.9x25"
    CHS_355_6x6_3 = "CHS 355.6x6.3"
    CHS_355_6x8 = "CHS 355.6x8"
    CHS_355_6x10 = "CHS 355.6x10"
    CHS_355_6x12_5 = "CHS 355.6x12.5"
    CHS_355_6x14_2 = "CHS 355.6x14.2"
    CHS_355_6x16 = "CHS 355.6x16"
    CHS_355_6x20 = "CHS 355.6x20"
    CHS_355_6x25 = "CHS 355.6x25"
    CHS_406_4x6_3 = "CHS 406.4x6.3"
    CHS_406_4x8 = "CHS 406.4x8"
    CHS_406_4x10 = "CHS 406.4x10"
    CHS_406_4x12_5 = "CHS 406.4x12.5"
    CHS_406_4x14_2 = "CHS 406.4x14.2"
    CHS_406_4x16 = "CHS 406.4x16"
    CHS_406_4x20 = "CHS 406.4x20"
    CHS_406_4x25 = "CHS 406.4x25"
    CHS_406_4x30 = "CHS 406.4x30"
    CHS_406_4x40 = "CHS 406.4x40"
    CHS_457x6_3 = "CHS 457x6.3"
    CHS_457x8 = "CHS 457x8"
    CHS_457x10 = "CHS 457x10"
    CHS_457x12_5 = "CHS 457x12.5"
    CHS_457x14_2 = "CHS 457x14.2"
    CHS_457x16 = "CHS 457x16"
    CHS_457x20 = "CHS 457x20"
    CHS_457x25 = "CHS 457x25"
    CHS_457x30 = "CHS 457x30"
    CHS_457x40 = "CHS 457x40"
    CHS_508x6_3 = "CHS 508x6.3"
    CHS_508x8 = "CHS 508x8"
    CHS_508x10 = "CHS 508x10"
    CHS_508x12_5 = "CHS 508x12.5"
    CHS_508x14_2 = "CHS 508x14.2"
    CHS_508x16 = "CHS 508x16"
    CHS_508x20 = "CHS 508x20"
    CHS_508x25 = "CHS 508x25"
    CHS_508x30 = "CHS 508x30"
    CHS_508x40 = "CHS 508x40"
    CHS_610x6_3 = "CHS 610x6.3"
    CHS_610x8 = "CHS 610x8"
    CHS_610x10 = "CHS 610x10"
    CHS_610x12_5 = "CHS 610x12.5"
    CHS_610x14_2 = "CHS 610x14.2"
    CHS_610x16 = "CHS 610x16"
    CHS_610x20 = "CHS 610x20"
    CHS_610x25 = "CHS 610x25"
    CHS_610x30 = "CHS 610x30"
    CHS_610x40 = "CHS 610x40"
    CHS_711x6_3 = "CHS 711x6.3"
    CHS_711x8 = "CHS 711x8"
    CHS_711x10 = "CHS 711x10"
    CHS_711x12_5 = "CHS 711x12.5"
    CHS_711x14_2 = "CHS 711x14.2"
    CHS_711x16 = "CHS 711x16"
    CHS_711x20 = "CHS 711x20"
    CHS_711x25 = "CHS 711x25"
    CHS_711x30 = "CHS 711x30"
    CHS_711x40 = "CHS 711x40"
    CHS_762x6_3 = "CHS 762x6.3"
    CHS_762x8 = "CHS 762x8"
    CHS_762x10 = "CHS 762x10"
    CHS_762x12_5 = "CHS 762x12.5"
    CHS_762x14_2 = "CHS 762x14.2"
    CHS_762x16 = "CHS 762x16"
    CHS_762x20 = "CHS 762x20"
    CHS_762x25 = "CHS 762x25"
    CHS_762x30 = "CHS 762x30"
    CHS_762x40 = "CHS 762x40"
    CHS_813x8 = "CHS 813x8"
    CHS_813x10 = "CHS 813x10"
    CHS_813x12_5 = "CHS 813x12.5"
    CHS_813x14_2 = "CHS 813x14.2"
    CHS_813x16 = "CHS 813x16"
    CHS_813x20 = "CHS 813x20"
    CHS_813x25 = "CHS 813x25"
    CHS_813x30 = "CHS 813x30"
    CHS_914x8 = "CHS 914x8"
    CHS_914x10 = "CHS 914x10"
    CHS_914x12_5 = "CHS 914x12.5"
    CHS_914x14_2 = "CHS 914x14.2"
    CHS_914x16 = "CHS 914x16"
    CHS_914x20 = "CHS 914x20"
    CHS_914x25 = "CHS 914x25"
    CHS_914x30 = "CHS 914x30"
    CHS_1016x8 = "CHS 1016x8"
    CHS_1016x10 = "CHS 1016x10"
    CHS_1016x12_5 = "CHS 1016x12.5"
    CHS_1016x14_2 = "CHS 1016x14.2"
    CHS_1016x16 = "CHS 1016x16"
    CHS_1016x20 = "CHS 1016x20"
    CHS_1016x25 = "CHS 1016x25"
    CHS_1016x30 = "CHS 1016x30"
    CHS_1067x10 = "CHS 1067x10"
    CHS_1067x12_5 = "CHS 1067x12.5"
    CHS_1067x14_2 = "CHS 1067x14.2"
    CHS_1067x16 = "CHS 1067x16"
    CHS_1067x20 = "CHS 1067x20"
    CHS_1067x25 = "CHS 1067x25"
    CHS_1067x30 = "CHS 1067x30"
    CHS_1168x10 = "CHS 1168x10"
    CHS_1168x12_5 = "CHS 1168x12.5"
    CHS_1168x14_2 = "CHS 1168x14.2"
    CHS_1168x16 = "CHS 1168x16"
    CHS_1168x20 = "CHS 1168x20"
    CHS_1168x25 = "CHS 1168x25"
    CHS_1219x10 = "CHS 1219x10"
    CHS_1219x12_5 = "CHS 1219x12.5"
    CHS_1219x14_2 = "CHS 1219x14.2"
    CHS_1219x16 = "CHS 1219x16"
    CHS_1219x20 = "CHS 1219x20"
    CHS_1219x25 = "CHS 1219x25"
    CHS_1219x30 = "CHS 1219x30"
    CHS_1219x32 = "CHS 1219x32"
    CHS_1219x36 = "CHS 1219x36"
    CHS_1219x40 = "CHS 1219x40"
    CHS_1420x10 = "CHS 1420x10"
    CHS_1420x12_5 = "CHS 1420x12.5"
    CHS_1420x14_2 = "CHS 1420x14.2"
    CHS_1420x16 = "CHS 1420x16"
    CHS_1420x20 = "CHS 1420x20"
    CHS_1420x25 = "CHS 1420x25"
    CHS_1420x30 = "CHS 1420x30"
    CHS_1420x32 = "CHS 1420x32"
    CHS_1420x36 = "CHS 1420x36"
    CHS_1420x40 = "CHS 1420x40"
    CHS_1620x10 = "CHS 1620x10"
    CHS_1620x12_5 = "CHS 1620x12.5"
    CHS_1620x14_2 = "CHS 1620x14.2"
    CHS_1620x16 = "CHS 1620x16"
    CHS_1620x20 = "CHS 1620x20"
    CHS_1620x25 = "CHS 1620x25"
    CHS_1620x30 = "CHS 1620x30"
    CHS_1620x32 = "CHS 1620x32"
    CHS_1620x36 = "CHS 1620x36"
    CHS_1620x40 = "CHS 1620x40"
    CHS_1820x12_5 = "CHS 1820x12.5"
    CHS_1820x14_2 = "CHS 1820x14.2"
    CHS_1820x16 = "CHS 1820x16"
    CHS_1820x20 = "CHS 1820x20"
    CHS_1820x25 = "CHS 1820x25"
    CHS_1820x30 = "CHS 1820x30"
    CHS_1820x32 = "CHS 1820x32"
    CHS_1820x36 = "CHS 1820x36"
    CHS_1820x40 = "CHS 1820x40"
    CHS_2020x14_2 = "CHS 2020x14.2"
    CHS_2020x16 = "CHS 2020x16"
    CHS_2020x20 = "CHS 2020x20"
    CHS_2020x25 = "CHS 2020x25"
    CHS_2020x30 = "CHS 2020x30"
    CHS_2020x32 = "CHS 2020x32"
    CHS_2020x36 = "CHS 2020x36"
    CHS_2020x40 = "CHS 2020x40"
    CHS_2220x14_2 = "CHS 2220x14.2"
    CHS_2220x16 = "CHS 2220x16"
    CHS_2220x20 = "CHS 2220x20"
    CHS_2220x25 = "CHS 2220x25"
    CHS_2220x30 = "CHS 2220x30"
    CHS_2220x32 = "CHS 2220x32"
    CHS_2220x36 = "CHS 2220x36"
    CHS_2220x40 = "CHS 2220x40"

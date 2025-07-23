"""AZ Sheet Pile Steel Profiles (Z-Section)."""

from enum import Enum

from blueprints.type_alias import CM, CM2, CM3, CM4, DEG, KG, M2, MM


class AZ(Enum):
    """Geometrical representation of AZ sheet pile steel profiles (Z-Section)."""

    AZ_18 = (
        "AZ 18",
        630,  # b_width_single_pile
        380,  # h_height_pile
        9.5,  # tf_flange_thickness
        9.5,  # tw_web_thickness
        348,  # bf_flange_width
        55.4,  # a_flange_angle
        150.4,  # a_cross_sectional_area
        74.4,  # gsp_mass_per_single_pile
        34200,  # i_y_moment_inertia
        1800,  # w_el_y_elastic_section_modulus
        1050,  # s_y_static_moment
        2104,  # w_pl_y_plastic_section_modulus
        118.1,  # gw_mass_per_m
        15.07,  # rg_radius_of_gyration
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    AZ_18_10_10 = (
        "AZ 18-10/10",
        630,
        381,
        10.0,
        10.0,
        348,
        55.4,
        157.2,
        77.8,
        35540,
        1870,
        1095,
        2189,
        123.4,
        15.04,
        1.35,
        "ArcelorMittal",
    )

    AZ_26 = (
        "AZ 26",
        630,
        427,
        13.0,
        12.2,
        347,
        58.5,
        197.8,
        97.8,
        55510,
        2600,
        1530,
        3059,
        155.2,
        16.75,
        1.41,
        "ArcelorMittal",
    )

    AZ_12_770 = (
        "AZ 12-770",
        770,
        344,
        8.5,
        8.5,
        346,
        39.5,
        120.1,
        72.6,
        21430,
        1245,
        740,
        1480,
        94.3,
        13.36,
        1.2,
        "ArcelorMittal",
    )

    AZ_13_770 = (
        "AZ 13-770",
        770,
        344,
        9.0,
        9.0,
        346,
        39.5,
        125.8,
        76.1,
        22360,
        1300,
        775,
        1546,
        98.8,
        13.33,
        1.2,
        "ArcelorMittal",
    )

    AZ_14_770 = (
        "AZ 14-770",
        770,
        345,
        9.5,
        9.5,
        346,
        39.5,
        131.5,
        79.5,
        23300,
        1355,
        805,
        1611,
        103.2,
        13.31,
        1.2,
        "ArcelorMittal",
    )

    AZ_14_770_10_10 = (
        "AZ 14-770-10/10",
        770,
        345,
        10.0,
        10.0,
        346,
        39.5,
        137.2,
        82.9,
        24240,
        1405,
        840,
        1677,
        107.7,
        13.3,
        1.2,
        "ArcelorMittal",
    )

    AZ_12_700 = (
        "AZ 12-700",
        700,
        314,
        8.5,
        8.5,
        350,
        42.8,
        123.2,
        67.7,
        18880,
        1205,
        710,
        1415,
        96.7,
        12.38,
        1.22,
        "ArcelorMittal",
    )

    AZ_13_700 = (
        "AZ 13-700",
        700,
        315,
        9.5,
        9.5,
        350,
        42.8,
        134.7,
        74.0,
        20540,
        1305,
        770,
        1540,
        105.7,
        12.35,
        1.22,
        "ArcelorMittal",
    )

    AZ_13_700_10_10 = (
        "AZ 13-700-10/10",
        700,
        316,
        10.0,
        10.0,
        350,
        42.8,
        140.4,
        77.2,
        21370,
        1355,
        800,
        1600,
        110.2,
        12.33,
        1.22,
        "ArcelorMittal",
    )

    AZ_14_700 = (
        "AZ 14-700",
        700,
        316,
        10.5,
        10.5,
        350,
        42.8,
        146.1,
        80.3,
        22190,
        1405,
        835,
        1665,
        114.7,
        12.32,
        1.22,
        "ArcelorMittal",
    )

    AZ_17_700 = (
        "AZ 17-700",
        700,
        420,
        8.5,
        8.5,
        346,
        51.2,
        133.0,
        73.1,
        36230,
        1730,
        1015,
        2027,
        104.4,
        16.5,
        1.33,
        "ArcelorMittal",
    )

    AZ_18_700 = (
        "AZ 18-700",
        700,
        420,
        9.0,
        9.0,
        346,
        51.2,
        139.2,
        76.5,
        37800,
        1800,
        1060,
        2116,
        109.3,
        16.47,
        1.33,
        "ArcelorMittal",
    )

    AZ_19_700 = (
        "AZ 19-700",
        700,
        421,
        9.5,
        9.5,
        346,
        51.2,
        145.6,
        80.0,
        39380,
        1870,
        1105,
        2206,
        114.3,
        16.44,
        1.33,
        "ArcelorMittal",
    )

    AZ_20_700 = (
        "AZ 20-700",
        700,
        421,
        10.0,
        10.0,
        346,
        51.2,
        152.0,
        83.5,
        40960,
        1945,
        1150,
        2296,
        119.3,
        16.42,
        1.33,
        "ArcelorMittal",
    )

    AZ_24_700 = (
        "AZ 24-700",
        700,
        459,
        11.2,
        11.2,
        361,
        55.2,
        174.1,
        95.7,
        55820,
        2430,
        1435,
        2867,
        136.7,
        17.9,
        1.38,
        "ArcelorMittal",
    )

    AZ_26_700 = (
        "AZ 26-700",
        700,
        460,
        12.2,
        12.2,
        361,
        55.2,
        187.2,
        102.9,
        59720,
        2600,
        1535,
        3070,
        146.9,
        17.86,
        1.38,
        "ArcelorMittal",
    )

    AZ_28_700 = (
        "AZ 28-700",
        700,
        461,
        13.2,
        13.2,
        361,
        55.2,
        200.2,
        110.0,
        63620,
        2760,
        1635,
        3273,
        157.2,
        17.83,
        1.38,
        "ArcelorMittal",
    )

    AZ_36_700N = (
        "AZ 36-700N",
        700,
        499,
        15.0,
        11.2,
        425,
        63.2,
        215.9,
        118.6,
        89610,
        3590,
        2055,
        4110,
        169.5,
        20.37,
        1.47,
        "ArcelorMittal",
    )

    AZ_38_700N = (
        "AZ 38-700N",
        700,
        500,
        16.0,
        12.2,
        425,
        63.2,
        230.0,
        126.4,
        94840,
        3795,
        2180,
        4360,
        180.6,
        20.31,
        1.47,
        "ArcelorMittal",
    )

    AZ_40_700N = (
        "AZ 40-700N",
        700,
        501,
        17.0,
        13.2,
        425,
        63.2,
        244.2,
        134.2,
        100080,
        3995,
        2305,
        4605,
        191.7,
        20.25,
        1.47,
        "ArcelorMittal",
    )

    AZ_42_700N = (
        "AZ 42-700N",
        700,
        499,
        18.0,
        14.0,
        425,
        63.2,
        258.7,
        142.1,
        104930,
        4205,
        2425,
        4855,
        203.1,
        20.14,
        1.47,
        "ArcelorMittal",
    )

    AZ_44_700N = (
        "AZ 44-700N",
        700,
        500,
        19.0,
        15.0,
        425,
        63.2,
        272.8,
        149.9,
        110150,
        4405,
        2550,
        5105,
        214.2,
        20.09,
        1.47,
        "ArcelorMittal",
    )

    AZ_46_700N = (
        "AZ 46-700N",
        700,
        501,
        20.0,
        16.0,
        425,
        63.2,
        287.0,
        157.7,
        115370,
        4605,
        2675,
        5350,
        225.3,
        20.05,
        1.47,
        "ArcelorMittal",
    )

    AZ_48_700 = (
        "AZ 48-700",
        700,
        503,
        22.0,
        15.0,
        426,
        63.2,
        288.4,
        158.5,
        119650,
        4755,
        2745,
        5490,
        226.4,
        20.37,
        1.46,
        "ArcelorMittal",
    )

    AZ_50_700 = (
        "AZ 50-700",
        700,
        504,
        23.0,
        16.0,
        426,
        63.2,
        302.6,
        166.3,
        124890,
        4955,
        2870,
        5735,
        237.5,
        20.32,
        1.46,
        "ArcelorMittal",
    )

    AZ_52_700 = (
        "AZ 52-700",
        700,
        505,
        24.0,
        17.0,
        426,
        63.2,
        316.8,
        174.1,
        130140,
        5155,
        2990,
        5985,
        248.7,
        20.27,
        1.46,
        "ArcelorMittal",
    )

    AZ_28_750 = (
        "AZ 28-750",
        750,
        509,
        12.0,
        10.0,
        422,
        58.9,
        171.2,
        100.8,
        71540,
        2810,
        1620,
        3245,
        134.4,
        20.44,
        1.41,
        "ArcelorMittal",
    )

    AZ_30_750 = (
        "AZ 30-750",
        750,
        510,
        13.0,
        11.0,
        422,
        58.9,
        184.7,
        108.8,
        76670,
        3005,
        1740,
        3485,
        145.0,
        20.37,
        1.41,
        "ArcelorMittal",
    )

    AZ_32_750 = (
        "AZ 32-750",
        750,
        511,
        14.0,
        12.0,
        422,
        58.9,
        198.3,
        116.7,
        81800,
        3200,
        1860,
        3720,
        155.6,
        20.31,
        1.41,
        "ArcelorMittal",
    )

    AZ_18_800 = (
        "AZ 18-800",
        800,
        449,
        8.5,
        8.5,
        428,
        51.8,
        128.6,
        80.7,
        41320,
        1840,
        1065,
        2135,
        100.9,
        17.93,
        1.3,
        "ArcelorMittal",
    )

    AZ_20_800 = (
        "AZ 20-800",
        800,
        450,
        9.5,
        9.5,
        428,
        51.8,
        141.0,
        88.6,
        45050,
        2000,
        1165,
        2330,
        110.7,
        17.87,
        1.3,
        "ArcelorMittal",
    )

    AZ_22_800 = (
        "AZ 22-800",
        800,
        451,
        10.5,
        10.5,
        428,
        51.8,
        153.5,
        96.4,
        48790,
        2165,
        1260,
        2525,
        120.5,
        17.83,
        1.3,
        "ArcelorMittal",
    )

    AZ_23_800 = (
        "AZ 23-800",
        800,
        474,
        11.5,
        9.0,
        426,
        52.9,
        150.6,
        94.6,
        55260,
        2330,
        1340,
        2680,
        118.2,
        19.15,
        1.32,
        "ArcelorMittal",
    )

    AZ_25_800 = (
        "AZ 25-800",
        800,
        475,
        12.5,
        10.0,
        426,
        52.9,
        163.3,
        102.6,
        59410,
        2500,
        1445,
        2890,
        128.2,
        19.07,
        1.32,
        "ArcelorMittal",
    )

    AZ_27_800 = (
        "AZ 27-800",
        800,
        476,
        13.5,
        11.0,
        426,
        52.9,
        176.0,
        110.5,
        63570,
        2670,
        1550,
        3100,
        138.1,
        19.01,
        1.32,
        "ArcelorMittal",
    )

    # Old AZ profiles
    AZ_13 = (
        "AZ 13",
        670,  # b_width_single_pile
        302,  # h_height_pile
        8.5,  # tf_flange_thickness
        8.5,  # tw_web_thickness
        157,  # bf_flange_width
        55.0,  # a_flange_angle
        126,  # a_cross_sectional_area
        66.1,  # gsp_mass_per_single_pile
        18140,  # i_y_moment_inertia
        1200,  # w_el_y_elastic_section_modulus
        1409,  # s_y_static_moment
        1440,  # w_pl_y_plastic_section_modulus
        99,  # gw_mass_per_m
        12.0,  # radius_of_gyration_y_y
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    AZ_13_10_10 = (
        "AZ 13-10/10",
        670,  # b_width_single_pile
        303,  # h_height_pile
        9.5,  # tf_flange_thickness
        9.5,  # tw_web_thickness
        157,  # bf_flange_width
        55.0,  # a_flange_angle
        137,  # a_cross_sectional_area
        72.0,  # gsp_mass_per_single_pile
        19700,  # i_y_moment_inertia
        1300,  # w_el_y_elastic_section_modulus
        1528,  # s_y_static_moment
        1560,  # w_pl_y_plastic_section_modulus
        107,  # gw_mass_per_m
        11.99,  # radius_of_gyration_y_y
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    AZ_14 = (
        "AZ 14",
        670,  # b_width_single_pile
        304,  # h_height_pile
        10.0,  # tf_flange_thickness
        10.0,  # tw_web_thickness
        158,  # bf_flange_width
        55.0,  # a_flange_angle
        143,  # a_cross_sectional_area
        75.2,  # gsp_mass_per_single_pile
        20480,  # i_y_moment_inertia
        1350,  # w_el_y_elastic_section_modulus
        1589,  # s_y_static_moment
        1620,  # w_pl_y_plastic_section_modulus
        112,  # gw_mass_per_m
        11.97,  # radius_of_gyration_y_y
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    AZ_17 = (
        "AZ 17",
        670,  # b_width_single_pile
        304,  # h_height_pile
        10.5,  # tf_flange_thickness
        10.5,  # tw_web_thickness
        158,  # bf_flange_width
        55.0,  # a_flange_angle
        149,  # a_cross_sectional_area
        78.3,  # gsp_mass_per_single_pile
        21300,  # i_y_moment_inertia
        1400,  # w_el_y_elastic_section_modulus
        1651,  # s_y_static_moment
        1680,  # w_pl_y_plastic_section_modulus
        117,  # gw_mass_per_m
        11.96,  # radius_of_gyration_y_y
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    AZ_17_630 = (
        "AZ 17-630",
        630,  # b_width_single_pile
        379,  # h_height_pile
        8.5,  # tf_flange_thickness
        8.5,  # tw_web_thickness
        197,  # bf_flange_width
        52.0,  # a_flange_angle
        138,  # a_cross_sectional_area
        68.4,  # gsp_mass_per_single_pile
        31580,  # i_y_moment_inertia
        1665,  # w_el_y_elastic_section_modulus
        1945,  # s_y_static_moment
        1998,  # w_pl_y_plastic_section_modulus
        109,  # gw_mass_per_m
        15.13,  # radius_of_gyration_y_y
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    AZ_24_700N = (
        "AZ 24-700N",
        700,  # b_width_single_pile
        459,  # h_height_pile
        12.5,  # tf_flange_thickness
        9.0,  # tw_web_thickness
        238,  # bf_flange_width
        52.0,  # a_flange_angle
        163,  # a_cross_sectional_area
        89.7,  # gsp_mass_per_single_pile
        55890,  # i_y_moment_inertia
        2435,  # w_el_y_elastic_section_modulus
        2810,  # s_y_static_moment
        2922,  # w_pl_y_plastic_section_modulus
        128,  # gw_mass_per_m
        18.52,  # radius_of_gyration_y_y
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    AZ_25 = (
        "AZ 25",
        630,  # b_width_single_pile
        426,  # h_height_pile
        12.0,  # tf_flange_thickness
        11.2,  # tw_web_thickness
        221,  # bf_flange_width
        50.0,  # a_flange_angle
        185,  # a_cross_sectional_area
        91.5,  # gsp_mass_per_single_pile
        52250,  # i_y_moment_inertia
        2455,  # w_el_y_elastic_section_modulus
        2875,  # s_y_static_moment
        2946,  # w_pl_y_plastic_section_modulus
        145,  # gw_mass_per_m
        16.81,  # radius_of_gyration_y_y
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    AZ_26_700N = (
        "AZ 26-700N",
        700,  # b_width_single_pile
        460,  # h_height_pile
        13.5,  # tf_flange_thickness
        10.0,  # tw_web_thickness
        239,  # bf_flange_width
        52.0,  # a_flange_angle
        176,  # a_cross_sectional_area
        96.9,  # gsp_mass_per_single_pile
        59790,  # i_y_moment_inertia
        2600,  # w_el_y_elastic_section_modulus
        3015,  # s_y_static_moment
        3120,  # w_pl_y_plastic_section_modulus
        138,  # gw_mass_per_m
        18.43,  # radius_of_gyration_y_y
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    AZ_28 = (
        "AZ 28",
        630,  # b_width_single_pile
        428,  # h_height_pile
        14.0,  # tf_flange_thickness
        13.2,  # tw_web_thickness
        222,  # bf_flange_width
        50.0,  # a_flange_angle
        211,  # a_cross_sectional_area
        85.0,  # gsp_mass_per_single_pile
        45570,  # i_y_moment_inertia
        2600,  # w_el_y_elastic_section_modulus
        3250,  # s_y_static_moment
        3120,  # w_pl_y_plastic_section_modulus
        170,  # gw_mass_per_m
        14.72,  # radius_of_gyration_y_y
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    AZ_28_700N = (
        "AZ 28-700N",
        700,  # b_width_single_pile
        461,  # h_height_pile
        14.5,  # tf_flange_thickness
        11.0,  # tw_web_thickness
        239,  # bf_flange_width
        52.0,  # a_flange_angle
        189,  # a_cross_sectional_area
        104.1,  # gsp_mass_per_single_pile
        63700,  # i_y_moment_inertia
        2765,  # w_el_y_elastic_section_modulus
        3220,  # s_y_static_moment
        3318,  # w_pl_y_plastic_section_modulus
        149,  # gw_mass_per_m
        18.36,  # radius_of_gyration_y_y
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    AZ_34 = (
        "AZ 34",
        630,  # b_width_single_pile
        459,  # h_height_pile
        17.0,  # tf_flange_thickness
        13.0,  # tw_web_thickness
        238,  # bf_flange_width
        50.0,  # a_flange_angle
        234,  # a_cross_sectional_area
        115.5,  # gsp_mass_per_single_pile
        78700,  # i_y_moment_inertia
        3430,  # w_el_y_elastic_section_modulus
        3980,  # s_y_static_moment
        4114,  # w_pl_y_plastic_section_modulus
        183,  # gw_mass_per_m
        18.34,  # radius_of_gyration_y_y
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    AZ_36 = (
        "AZ 36",
        630,  # b_width_single_pile
        460,  # h_height_pile
        18.0,  # tf_flange_thickness
        14.0,  # tw_web_thickness
        239,  # bf_flange_width
        50.0,  # a_flange_angle
        247,  # a_cross_sectional_area
        122.2,  # gsp_mass_per_single_pile
        82800,  # i_y_moment_inertia
        3600,  # w_el_y_elastic_section_modulus
        4196,  # s_y_static_moment
        4320,  # w_pl_y_plastic_section_modulus
        194,  # gw_mass_per_m
        18.32,  # radius_of_gyration_y_y
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    AZ_36_700 = (
        "AZ 36-700",
        700,  # b_width_single_pile
        499,  # h_height_pile
        17.0,  # tf_flange_thickness
        11.2,  # tw_web_thickness
        259,  # bf_flange_width
        50.0,  # a_flange_angle
        216,  # a_cross_sectional_area
        118.5,  # gsp_mass_per_single_pile
        89740,  # i_y_moment_inertia
        3600,  # w_el_y_elastic_section_modulus
        4111,  # s_y_static_moment
        4320,  # w_pl_y_plastic_section_modulus
        169,  # gw_mass_per_m
        20.39,  # radius_of_gyration_y_y
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    AZ_37_700 = (
        "AZ 37-700",
        700,  # b_width_single_pile
        499,  # h_height_pile
        17.0,  # tf_flange_thickness
        12.2,  # tw_web_thickness
        259,  # bf_flange_width
        50.0,  # a_flange_angle
        226,  # a_cross_sectional_area
        124.2,  # gsp_mass_per_single_pile
        92400,  # i_y_moment_inertia
        3705,  # w_el_y_elastic_section_modulus
        4260,  # s_y_static_moment
        4446,  # w_pl_y_plastic_section_modulus
        177,  # gw_mass_per_m
        20.22,  # radius_of_gyration_y_y
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    AZ_38 = (
        "AZ 38",
        630,  # b_width_single_pile
        461,  # h_height_pile
        19.0,  # tf_flange_thickness
        15.0,  # tw_web_thickness
        239,  # bf_flange_width
        50.0,  # a_flange_angle
        261,  # a_cross_sectional_area
        129.1,  # gsp_mass_per_single_pile
        87080,  # i_y_moment_inertia
        3780,  # w_el_y_elastic_section_modulus
        4417,  # s_y_static_moment
        4536,  # w_pl_y_plastic_section_modulus
        205,  # gw_mass_per_m
        18.27,  # radius_of_gyration_y_y
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    AZ_38_700 = (
        "AZ 38-700",
        700,  # b_width_single_pile
        500,  # h_height_pile
        18.0,  # tf_flange_thickness
        12.2,  # tw_web_thickness
        260,  # bf_flange_width
        50.0,  # a_flange_angle
        230,  # a_cross_sectional_area
        126.2,  # gsp_mass_per_single_pile
        94840,  # i_y_moment_inertia
        3800,  # w_el_y_elastic_section_modulus
        4353,  # s_y_static_moment
        4560,  # w_pl_y_plastic_section_modulus
        180,  # gw_mass_per_m
        20.31,  # radius_of_gyration_y_y
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    AZ_39_700 = (
        "AZ 39-700",
        700,  # b_width_single_pile
        500,  # h_height_pile
        18.0,  # tf_flange_thickness
        13.2,  # tw_web_thickness
        260,  # bf_flange_width
        50.0,  # a_flange_angle
        240,  # a_cross_sectional_area
        131.9,  # gsp_mass_per_single_pile
        97500,  # i_y_moment_inertia
        3900,  # w_el_y_elastic_section_modulus
        4500,  # s_y_static_moment
        4680,  # w_pl_y_plastic_section_modulus
        188,  # gw_mass_per_m
        20.16,  # radius_of_gyration_y_y
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    AZ_40_700 = (
        "AZ 40-700",
        700,  # b_width_single_pile
        501,  # h_height_pile
        19.0,  # tf_flange_thickness
        13.2,  # tw_web_thickness
        260,  # bf_flange_width
        50.0,  # a_flange_angle
        244,  # a_cross_sectional_area
        133.8,  # gsp_mass_per_single_pile
        99930,  # i_y_moment_inertia
        4000,  # w_el_y_elastic_section_modulus
        4596,  # s_y_static_moment
        4800,  # w_pl_y_plastic_section_modulus
        191,  # gw_mass_per_m
        20.24,  # radius_of_gyration_y_y
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    AZ_41_700 = (
        "AZ 41-700",
        700,  # b_width_single_pile
        501,  # h_height_pile
        19.0,  # tf_flange_thickness
        14.2,  # tw_web_thickness
        260,  # bf_flange_width
        50.0,  # a_flange_angle
        254,  # a_cross_sectional_area
        139.5,  # gsp_mass_per_single_pile
        102610,  # i_y_moment_inertia
        4095,  # w_el_y_elastic_section_modulus
        4745,  # s_y_static_moment
        4914,  # w_pl_y_plastic_section_modulus
        199,  # gw_mass_per_m
        20.1,  # radius_of_gyration_y_y
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    AZ_46 = (
        "AZ 46",
        580,  # b_width_single_pile
        481,  # h_height_pile
        18.0,  # tf_flange_thickness
        14.0,  # tw_web_thickness
        250,  # bf_flange_width
        50.0,  # a_flange_angle
        291,  # a_cross_sectional_area
        132.6,  # gsp_mass_per_single_pile
        110450,  # i_y_moment_inertia
        4595,  # w_el_y_elastic_section_modulus
        2650,  # s_y_static_moment
        5295,  # w_pl_y_plastic_section_modulus
        229,  # gw_mass_per_m
        19.48,  # radius_of_gyration_y_y
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    AZ_48 = (
        "AZ 48",
        580,  # b_width_single_pile
        482,  # h_height_pile
        19.0,  # tf_flange_thickness
        15.0,  # tw_web_thickness
        250,  # bf_flange_width
        50.0,  # a_flange_angle
        307,  # a_cross_sectional_area
        139.6,  # gsp_mass_per_single_pile
        115670,  # i_y_moment_inertia
        4800,  # w_el_y_elastic_section_modulus
        2775,  # s_y_static_moment
        5553,  # w_pl_y_plastic_section_modulus
        241,  # gw_mass_per_m
        19.41,  # radius_of_gyration_y_y
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    AZ_50 = (
        "AZ 50",
        580,  # b_width_single_pile
        483,  # h_height_pile
        20.0,  # tf_flange_thickness
        16.0,  # tw_web_thickness
        251,  # bf_flange_width
        50.0,  # a_flange_angle
        322,  # a_cross_sectional_area
        146.7,  # gsp_mass_per_single_pile
        121060,  # i_y_moment_inertia
        5015,  # w_el_y_elastic_section_modulus
        2910,  # s_y_static_moment
        5816,  # w_pl_y_plastic_section_modulus
        253,  # gw_mass_per_m
        19.39,  # radius_of_gyration_y_y
        1.35,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    def __init__(  # noqa: PLR0913
        self,
        alias: str,
        b_width_single_pile: MM,
        h_height_pile: MM,
        tf_flange_thickness: MM,
        tw_web_thickness: MM,
        bf_flange_width: MM,
        a_flange_angle: DEG,
        a_cross_sectional_area: CM2,
        gsp_mass_per_single_pile: KG,
        i_y_moment_inertia: CM4,
        w_el_y_elastic_section_modulus: CM3,
        s_y_static_moment: CM3,
        w_pl_y_plastic_section_modulus: CM3,
        gw_mass_per_m: KG,
        radius_of_gyration_y_y: CM,
        al_coating_area: M2,
        manufacturer: str,
    ) -> None:
        """Initialize AZ sheet pile profile.

        This method sets the profile's alias, dimensions, and properties.

        Parameters
        ----------
        alias: str
            Name of the sheet pile profile.
            For example: "AZ 18".
        b_width_single_pile: MM
            (b) Width of a single pile [mm].
        h_height_pile: MM
            (h) Height of the wall [mm].
        tf_flange_thickness: MM
            (tf) Thickness of the flange (mm).
        tw_web_thickness: MM
            (tw) Thickness of the web (mm).
        bf_flange_width: MM
            (bf) Width of the flange [mm].
        a_flange_angle: float
            (α) Flange angle in degrees [°].
        a_cross_sectional_area: CM2
            (A) Cross sectional steel area in [cm²/m].
        gsp_mass_per_single_pile: KG
            (Gsp) Mass per single pile in [kg/m].
        i_y_moment_inertia: CM4
            (Iy) Moment of inertia about the main neutral axis y-y in [cm⁴/m].
        w_el_y_elastic_section_modulus: CM3
            (Wel,y) Elastic section modulus in [cm³/m].
        s_y_static_moment: CM3
            (Sy) Static moment in [cm³/m].
        w_pl_y_plastic_section_modulus: CM3
            (Wpl,y) Plastic section modulus in [cm³/m].
        gw_mass_per_m: KG
            (G) Mass per m in [kg/m].
        radius_of_gyration_y_y: float
            (rg) Radius of gyration about the main neutral axis y-y in [cm].
        al_coating_area: M2
            (Al) Coating area. One side, excludes inside interlocks in [m²/m].
        manufacturer: str
            Manufacturer name.
        """
        self.alias = alias
        self.b_width_single_pile = b_width_single_pile
        self.h_height_pile = h_height_pile
        self.tf_flange_thickness = tf_flange_thickness
        self.tw_web_thickness = tw_web_thickness
        self.bf_flange_width = bf_flange_width
        self.a_flange_angle = a_flange_angle
        self.a_cross_sectional_area = a_cross_sectional_area
        self.gsp_mass_per_single_pile = gsp_mass_per_single_pile
        self.i_y_moment_inertia = i_y_moment_inertia
        self.w_el_y_elastic_section_modulus = w_el_y_elastic_section_modulus
        self.s_y_static_moment = s_y_static_moment
        self.w_pl_y_plastic_section_modulus = w_pl_y_plastic_section_modulus
        self.gw_mass_per_m = gw_mass_per_m
        self.radius_of_gyration_y_y = radius_of_gyration_y_y
        self.al_coating_area = al_coating_area
        self.manufacturer = manufacturer
        self.sheet_pile_type = "Z-Section"

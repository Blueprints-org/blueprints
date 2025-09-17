"""GU and PU Sheet Pile Steel Profiles (U-Section)."""

from enum import Enum

from blueprints.type_alias import CM, CM2, CM3, CM4, DEG, KG, M2, MM


class USections(Enum):
    """Geometrical representation of GU and PU sheet pile steel profiles (U-Sections)."""

    # GU profiles
    GU_6N = (
        "GU 6N",
        600,  # b_width_single_pile
        309,  # h_height_pile
        6.0,  # tf_flange_thickness
        6.0,  # tw_web_thickness
        248,  # bf_flange_width
        42.5,  # a_flange_angle
        89.0,  # a_cross_sectional_area
        41.9,  # gsp_mass_per_single_pile
        9670,  # i_y_moment_inertia
        625,  # w_el_y_elastic_section_modulus
        375,  # s_y_static_moment
        765,  # w_pl_y_plastic_section_modulus
        69.9,  # gw_mass_per_m
        10.43,  # rg_radius_of_gyration
        1.26,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    GU_7N = (
        "GU 7N",
        600,
        310,
        6.5,
        6.4,
        248,
        42.5,
        93.7,
        44.1,
        10450,
        675,
        400,
        825,
        73.5,
        10.56,
        1.26,
        "ArcelorMittal",
    )

    GU_7S = (
        "GU 7S",
        600,
        311,
        7.2,
        6.9,
        248,
        42.5,
        98.2,
        46.3,
        11540,
        740,
        440,
        900,
        77.1,
        10.84,
        1.26,
        "ArcelorMittal",
    )

    GU_7HWS = (
        "GU 7HWS",
        600,
        312,
        7.3,
        6.9,
        248,
        42.5,
        100.7,
        47.4,
        11620,
        745,
        445,
        910,
        79.1,
        10.74,
        1.26,
        "ArcelorMittal",
    )

    GU_8N = (
        "GU 8N",
        600,
        312,
        7.5,
        7.1,
        248,
        42.5,
        103.1,
        48.5,
        12010,
        770,
        460,
        935,
        80.9,
        10.8,
        1.26,
        "ArcelorMittal",
    )

    GU_8S = (
        "GU 8S",
        600,
        313,
        8.0,
        7.5,
        248,
        42.5,
        107.8,
        50.8,
        12800,
        820,
        490,
        995,
        84.6,
        10.9,
        1.26,
        "ArcelorMittal",
    )

    GU_10N = (
        "GU 10N",
        600,
        316,
        9.0,
        6.8,
        283,
        52.0,
        118.5,
        55.8,
        15700,
        990,
        565,
        1160,
        93.0,
        11.51,
        1.29,
        "ArcelorMittal",
    )

    GU_11N = (
        "GU 11N",
        600,
        318,
        10.0,
        7.4,
        283,
        52.0,
        127.9,
        60.2,
        17450,
        1095,
        630,
        1280,
        100.4,
        11.68,
        1.29,
        "ArcelorMittal",
    )

    GU_12N = (
        "GU 12N",
        600,
        320,
        11.0,
        8.0,
        283,
        52.0,
        137.2,
        64.6,
        19220,
        1200,
        690,
        1400,
        107.7,
        11.83,
        1.29,
        "ArcelorMittal",
    )

    GU_13N = (
        "GU 13N",
        600,
        418,
        9.0,
        7.4,
        250,
        54.3,
        127.2,
        59.9,
        26590,
        1270,
        755,
        1535,
        99.8,
        14.46,
        1.41,
        "ArcelorMittal",
    )

    GU_14N = (
        "GU 14N",
        600,
        420,
        10.0,
        8.0,
        250,
        54.3,
        136.5,
        64.3,
        29410,
        1400,
        830,
        1685,
        107.1,
        14.68,
        1.41,
        "ArcelorMittal",
    )

    GU_15N = (
        "GU 15N",
        600,
        422,
        11.0,
        8.6,
        250,
        54.3,
        145.9,
        68.7,
        32260,
        1530,
        910,
        1840,
        114.5,
        14.87,
        1.41,
        "ArcelorMittal",
    )

    GU_16N = (
        "GU 16N",
        600,
        430,
        10.2,
        8.4,
        269,
        57.5,
        154.2,
        72.6,
        35950,
        1670,
        980,
        1988,
        121.0,
        15.3,
        1.43,
        "ArcelorMittal",
    )

    GU_18N = (
        "GU 18N",
        600,
        430,
        11.2,
        9.0,
        269,
        57.5,
        163.3,
        76.9,
        38650,
        1800,
        1055,
        2134,
        128.2,
        15.38,
        1.43,
        "ArcelorMittal",
    )

    GU_20N = (
        "GU 20N",
        600,
        430,
        12.2,
        9.5,
        269,
        57.5,
        172.3,
        81.1,
        41320,
        1920,
        1125,
        2280,
        135.2,
        15.49,
        1.43,
        "ArcelorMittal",
    )

    GU_21N = (
        "GU 21N",
        600,
        450,
        11.1,
        9.0,
        297,
        62.4,
        173.9,
        81.9,
        46380,
        2060,
        1195,
        2422,
        136.5,
        16.33,
        1.49,
        "ArcelorMittal",
    )

    GU_22N = (
        "GU 22N",
        600,
        450,
        12.1,
        9.5,
        297,
        62.4,
        182.9,
        86.1,
        49460,
        2200,
        1275,
        2580,
        143.6,
        16.45,
        1.49,
        "ArcelorMittal",
    )

    GU_23N = (
        "GU 23N",
        600,
        450,
        13.1,
        10.0,
        297,
        62.4,
        192.0,
        90.4,
        52510,
        2335,
        1355,
        2735,
        150.7,
        16.54,
        1.49,
        "ArcelorMittal",
    )

    GU_27N = (
        "GU 27N",
        600,
        452,
        14.2,
        9.7,
        339,
        68.0,
        206.8,
        97.4,
        60580,
        2680,
        1525,
        3087,
        162.3,
        17.12,
        1.54,
        "ArcelorMittal",
    )

    GU_28N = (
        "GU 28N",
        600,
        454,
        15.2,
        10.1,
        339,
        68.0,
        216.1,
        101.8,
        64460,
        2840,
        1620,
        3269,
        169.6,
        17.27,
        1.54,
        "ArcelorMittal",
    )

    GU_30N = (
        "GU 30N",
        600,
        456,
        16.2,
        10.5,
        339,
        68.0,
        225.6,
        106.2,
        68380,
        3000,
        1710,
        3450,
        177.1,
        17.41,
        1.54,
        "ArcelorMittal",
    )

    GU_31N = (
        "GU 31N",
        600,
        452,
        18.5,
        10.6,
        342,
        68.1,
        233.3,
        109.9,
        69210,
        3065,
        1745,
        3525,
        183.2,
        17.22,
        1.52,
        "ArcelorMittal",
    )

    GU_32N = (
        "GU 32N",
        600,
        452,
        19.5,
        11.0,
        342,
        68.1,
        242.3,
        114.1,
        72320,
        3200,
        1825,
        3687,
        190.2,
        17.28,
        1.52,
        "ArcelorMittal",
    )

    GU_33N = (
        "GU 33N",
        600,
        452,
        20.5,
        11.4,
        342,
        68.1,
        251.3,
        118.4,
        75410,
        3340,
        1905,
        3845,
        197.3,
        17.32,
        1.52,
        "ArcelorMittal",
    )

    GU_16_400 = (
        "GU 16-400",
        400,
        290,
        12.7,
        9.4,
        252,
        82.1,
        197.3,
        62.0,
        22580,
        1560,
        885,
        1815,
        154.9,
        10.7,
        1.6,
        "ArcelorMittal",
    )

    GU_18_400 = (
        "GU 18-400",
        400,
        292,
        15.0,
        9.7,
        252,
        82.1,
        220.8,
        69.3,
        26090,
        1785,
        1015,
        2080,
        173.3,
        10.87,
        1.6,
        "ArcelorMittal",
    )

    # PU profiles
    PU_12 = (
        "PU 12",
        600,
        360,
        9.8,
        9.0,
        258,
        50.4,
        140.0,
        66.1,
        21600,
        1200,
        715,
        1457,
        110.1,
        12.41,
        1.32,
        "ArcelorMittal",
    )

    PU_12S = (
        "PU 12S",
        600,
        360,
        10.0,
        10.0,
        257,
        50.4,
        150.8,
        71.0,
        22660,
        1260,
        755,
        1543,
        118.4,
        12.26,
        1.32,
        "ArcelorMittal",
    )

    PU_18_1 = (
        "PU 18-1",
        600,
        430,
        10.2,
        8.4,
        269,
        57.5,
        154.2,
        72.6,
        35950,
        1670,
        980,
        1988,
        121.0,
        15.30,
        1.43,
        "ArcelorMittal",
    )

    PU_18 = (
        "PU 18",
        600,
        430,
        11.2,
        9.0,
        269,
        57.5,
        163.3,
        76.9,
        38650,
        1800,
        1055,
        2134,
        128.2,
        15.38,
        1.43,
        "ArcelorMittal",
    )

    PU_18_PLUS_1 = (
        "PU 18+1",
        600,
        430,
        12.2,
        9.5,
        269,
        57.5,
        172.3,
        81.1,
        41320,
        1920,
        1125,
        2280,
        135.2,
        15.49,
        1.43,
        "ArcelorMittal",
    )

    PU_22_1 = (
        "PU 22-1",
        600,
        450,
        11.1,
        9.0,
        297,
        62.4,
        173.9,
        81.9,
        46380,
        2060,
        1195,
        2422,
        136.5,
        16.33,
        1.49,
        "ArcelorMittal",
    )

    PU_22 = (
        "PU 22",
        600,
        450,
        12.1,
        9.5,
        297,
        62.4,
        182.9,
        86.1,
        49460,
        2200,
        1275,
        2580,
        143.6,
        16.45,
        1.49,
        "ArcelorMittal",
    )

    PU_22_PLUS_1 = (
        "PU 22+1",
        600,
        450,
        13.1,
        10.0,
        297,
        62.4,
        192.0,
        90.4,
        52510,
        2335,
        1355,
        2735,
        150.7,
        16.54,
        1.49,
        "ArcelorMittal",
    )

    PU_28_1 = (
        "PU 28-1",
        600,
        452,
        14.2,
        9.7,
        339,
        68.0,
        206.8,
        97.4,
        60580,
        2680,
        1525,
        3087,
        162.3,
        17.12,
        1.54,
        "ArcelorMittal",
    )

    PU_28 = (
        "PU 28",
        600,
        454,
        15.2,
        10.1,
        339,
        68.0,
        216.1,
        101.8,
        64460,
        2840,
        1620,
        3269,
        169.6,
        17.27,
        1.54,
        "ArcelorMittal",
    )

    PU_28_PLUS_1 = (
        "PU 28+1",
        600,
        456,
        16.2,
        10.5,
        339,
        68.0,
        225.6,
        106.2,
        68380,
        3000,
        1710,
        3450,
        177.1,
        17.41,
        1.54,
        "ArcelorMittal",
    )

    PU_32_1 = (
        "PU 32-1",
        600,
        452,
        18.5,
        10.6,
        342,
        68.1,
        233.3,
        109.9,
        69210,
        3065,
        1745,
        3525,
        183.2,
        17.22,
        1.52,
        "ArcelorMittal",
    )

    PU_32 = (
        "PU 32",
        600,
        452,
        19.5,
        11.0,
        342,
        68.1,
        242.3,
        114.1,
        72320,
        3200,
        1825,
        3687,
        190.2,
        17.28,
        1.52,
        "ArcelorMittal",
    )

    PU_32_PLUS_1 = (
        "PU 32+1",
        600,
        452,
        20.5,
        11.4,
        342,
        68.1,
        251.3,
        118.4,
        75410,
        3340,
        1905,
        3845,
        197.3,
        17.32,
        1.52,
        "ArcelorMittal",
    )

    # Old U-section profiles
    GU_13_500 = (
        "GU 13-500",
        500,  # b_width_single_pile
        340,  # h_height_pile
        9.0,  # tf_flange_thickness
        8.5,  # tw_web_thickness
        136,  # bf_flange_width
        50.0,  # a_flange_angle
        144,  # a_cross_sectional_area
        56.6,  # gsp_mass_per_single_pile
        19640,  # i_y_moment_inertia
        1155,  # w_el_y_elastic_section_modulus
        1390,  # s_y_static_moment
        1328,  # w_pl_y_plastic_section_modulus
        113,  # gw_mass_per_m
        11.68,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    GU_15_500 = (
        "GU 15-500",
        500,  # b_width_single_pile
        340,  # h_height_pile
        10.0,  # tf_flange_thickness
        9.0,  # tw_web_thickness
        136,  # bf_flange_width
        50.0,  # a_flange_angle
        155,  # a_cross_sectional_area
        60.8,  # gsp_mass_per_single_pile
        21390,  # i_y_moment_inertia
        1260,  # w_el_y_elastic_section_modulus
        1515,  # s_y_static_moment
        1449,  # w_pl_y_plastic_section_modulus
        122,  # gw_mass_per_m
        11.75,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    JSP_2 = (
        "JSP 2",
        500,  # b_width_single_pile
        340,  # h_height_pile
        12.0,  # tf_flange_thickness
        10.0,  # tw_web_thickness
        136,  # bf_flange_width
        50.0,  # a_flange_angle
        177,  # a_cross_sectional_area
        69.3,  # gsp_mass_per_single_pile
        24810,  # i_y_moment_inertia
        1460,  # w_el_y_elastic_section_modulus
        1755,  # s_y_static_moment
        1678,  # w_pl_y_plastic_section_modulus
        139,  # gw_mass_per_m
        11.84,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    JSP_3 = (
        "JSP 3",
        400,  # b_width_single_pile
        200,  # h_height_pile
        10.5,  # tf_flange_thickness
        8.4,  # tw_web_thickness
        80,  # bf_flange_width
        55.0,  # a_flange_angle
        153,  # a_cross_sectional_area
        48.0,  # gsp_mass_per_single_pile
        8740,  # i_y_moment_inertia
        874,  # w_el_y_elastic_section_modulus
        971,  # s_y_static_moment
        1005,  # w_pl_y_plastic_section_modulus
        120,  # gw_mass_per_m
        7.56,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    JSP_4 = (
        "JSP 4",
        400,  # b_width_single_pile
        250,  # h_height_pile
        13.0,  # tf_flange_thickness
        10.4,  # tw_web_thickness
        100,  # bf_flange_width
        55.0,  # a_flange_angle
        191,  # a_cross_sectional_area
        60.0,  # gsp_mass_per_single_pile
        16800,  # i_y_moment_inertia
        1340,  # w_el_y_elastic_section_modulus
        1487,  # s_y_static_moment
        1540,  # w_pl_y_plastic_section_modulus
        150,  # gw_mass_per_m
        9.38,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    L_2S = (
        "L 2S",
        400,  # b_width_single_pile
        170,  # h_height_pile
        15.5,  # tf_flange_thickness
        12.4,  # tw_web_thickness
        68,  # bf_flange_width
        60.0,  # a_flange_angle
        242,  # a_cross_sectional_area
        76.1,  # gsp_mass_per_single_pile
        38600,  # i_y_moment_inertia
        2270,  # w_el_y_elastic_section_modulus
        2618,  # s_y_static_moment
        2610,  # w_pl_y_plastic_section_modulus
        190,  # gw_mass_per_m
        12.63,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    L_3S = (
        "L 3S",
        500,  # b_width_single_pile
        340,  # h_height_pile
        12.3,  # tf_flange_thickness
        9.0,  # tw_web_thickness
        136,  # bf_flange_width
        50.0,  # a_flange_angle
        177,  # a_cross_sectional_area
        69.7,  # gsp_mass_per_single_pile
        27200,  # i_y_moment_inertia
        1600,  # w_el_y_elastic_section_modulus
        1871,  # s_y_static_moment
        1839,  # w_pl_y_plastic_section_modulus
        139,  # gw_mass_per_m
        12.4,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    L_4S = (
        "L 4S",
        500,  # b_width_single_pile
        400,  # h_height_pile
        14.1,  # tf_flange_thickness
        10.0,  # tw_web_thickness
        160,  # bf_flange_width
        50.0,  # a_flange_angle
        201,  # a_cross_sectional_area
        78.9,  # gsp_mass_per_single_pile
        40010,  # i_y_moment_inertia
        2000,  # w_el_y_elastic_section_modulus
        2389,  # s_y_static_moment
        2300,  # w_pl_y_plastic_section_modulus
        158,  # gw_mass_per_m
        14.11,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    L_5S = (
        "L 5S",
        500,  # b_width_single_pile
        440,  # h_height_pile
        15.5,  # tf_flange_thickness
        10.0,  # tw_web_thickness
        176,  # bf_flange_width
        50.0,  # a_flange_angle
        219,  # a_cross_sectional_area
        86.2,  # gsp_mass_per_single_pile
        55010,  # i_y_moment_inertia
        2500,  # w_el_y_elastic_section_modulus
        2956,  # s_y_static_moment
        2875,  # w_pl_y_plastic_section_modulus
        172,  # gw_mass_per_m
        15.84,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    PU_10R = (
        "PU 10R",
        500,  # b_width_single_pile
        450,  # h_height_pile
        20.6,  # tf_flange_thickness
        11.5,  # tw_web_thickness
        180,  # bf_flange_width
        50.0,  # a_flange_angle
        270,  # a_cross_sectional_area
        106.0,  # gsp_mass_per_single_pile
        72000,  # i_y_moment_inertia
        3200,  # w_el_y_elastic_section_modulus
        3783,  # s_y_static_moment
        3680,  # w_pl_y_plastic_section_modulus
        212,  # gw_mass_per_m
        16.33,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    PU_11 = (
        "PU 11",
        600,  # b_width_single_pile
        360,  # h_height_pile
        8.0,  # tf_flange_thickness
        7.0,  # tw_web_thickness
        144,  # bf_flange_width
        55.0,  # a_flange_angle
        114,  # a_cross_sectional_area
        53.8,  # gsp_mass_per_single_pile
        18960,  # i_y_moment_inertia
        1055,  # w_el_y_elastic_section_modulus
        1245,  # s_y_static_moment
        1213,  # w_pl_y_plastic_section_modulus
        90,  # gw_mass_per_m
        12.9,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    PU_11R = (
        "PU 11R",
        600,  # b_width_single_pile
        360,  # h_height_pile
        8.8,  # tf_flange_thickness
        8.4,  # tw_web_thickness
        144,  # bf_flange_width
        55.0,  # a_flange_angle
        131,  # a_cross_sectional_area
        61.8,  # gsp_mass_per_single_pile
        19760,  # i_y_moment_inertia
        1095,  # w_el_y_elastic_section_modulus
        1336,  # s_y_static_moment
        1259,  # w_pl_y_plastic_section_modulus
        103,  # gw_mass_per_m
        12.29,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    PU_13R = (
        "PU 13R",
        600,  # b_width_single_pile
        360,  # h_height_pile
        9.0,  # tf_flange_thickness
        7.6,  # tw_web_thickness
        144,  # bf_flange_width
        55.0,  # a_flange_angle
        123,  # a_cross_sectional_area
        58.1,  # gsp_mass_per_single_pile
        20960,  # i_y_moment_inertia
        1165,  # w_el_y_elastic_section_modulus
        1370,  # s_y_static_moment
        1339,  # w_pl_y_plastic_section_modulus
        97,  # gw_mass_per_m
        13.05,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    PU_14R = (
        "PU 14R",
        675,  # b_width_single_pile
        400,  # h_height_pile
        10.0,  # tf_flange_thickness
        7.4,  # tw_web_thickness
        160,  # bf_flange_width
        52.0,  # a_flange_angle
        124,  # a_cross_sectional_area
        65.6,  # gsp_mass_per_single_pile
        25690,  # i_y_moment_inertia
        1285,  # w_el_y_elastic_section_modulus
        1515,  # s_y_static_moment
        1477,  # w_pl_y_plastic_section_modulus
        97,  # gw_mass_per_m
        14.39,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    PU_15R = (
        "PU 15R",
        675,  # b_width_single_pile
        400,  # h_height_pile
        11.0,  # tf_flange_thickness
        8.0,  # tw_web_thickness
        160,  # bf_flange_width
        52.0,  # a_flange_angle
        133,  # a_cross_sectional_area
        70.5,  # gsp_mass_per_single_pile
        28000,  # i_y_moment_inertia
        1400,  # w_el_y_elastic_section_modulus
        1655,  # s_y_static_moment
        1610,  # w_pl_y_plastic_section_modulus
        104,  # gw_mass_per_m
        14.52,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    PU_16 = (
        "PU 16",
        675,  # b_width_single_pile
        400,  # h_height_pile
        12.0,  # tf_flange_thickness
        8.6,  # tw_web_thickness
        160,  # bf_flange_width
        52.0,  # a_flange_angle
        142,  # a_cross_sectional_area
        75.4,  # gsp_mass_per_single_pile
        30290,  # i_y_moment_inertia
        1515,  # w_el_y_elastic_section_modulus
        1790,  # s_y_static_moment
        1742,  # w_pl_y_plastic_section_modulus
        112,  # gw_mass_per_m
        14.63,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    PU_20 = (
        "PU 20",
        600,  # b_width_single_pile
        380,  # h_height_pile
        12.0,  # tf_flange_thickness
        9.0,  # tw_web_thickness
        152,  # bf_flange_width
        55.0,  # a_flange_angle
        159,  # a_cross_sectional_area
        74.7,  # gsp_mass_per_single_pile
        30400,  # i_y_moment_inertia
        1600,  # w_el_y_elastic_section_modulus
        1878,  # s_y_static_moment
        1840,  # w_pl_y_plastic_section_modulus
        124,  # gw_mass_per_m
        13.83,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    PU_25 = (
        "PU 25",
        600,  # b_width_single_pile
        430,  # h_height_pile
        12.4,  # tf_flange_thickness
        10.0,  # tw_web_thickness
        172,  # bf_flange_width
        50.0,  # a_flange_angle
        179,  # a_cross_sectional_area
        84.3,  # gsp_mass_per_single_pile
        43000,  # i_y_moment_inertia
        2000,  # w_el_y_elastic_section_modulus
        2363,  # s_y_static_moment
        2300,  # w_pl_y_plastic_section_modulus
        141,  # gw_mass_per_m
        15.5,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    PU_6 = (
        "PU 6",
        600,  # b_width_single_pile
        452,  # h_height_pile
        14.2,  # tf_flange_thickness
        10.0,  # tw_web_thickness
        180,  # bf_flange_width
        50.0,  # a_flange_angle
        199,  # a_cross_sectional_area
        93.6,  # gsp_mass_per_single_pile
        56490,  # i_y_moment_inertia
        2500,  # w_el_y_elastic_section_modulus
        2899,  # s_y_static_moment
        2875,  # w_pl_y_plastic_section_modulus
        156,  # gw_mass_per_m
        16.85,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    PU_6R = (
        "PU 6R",
        600,  # b_width_single_pile
        226,  # h_height_pile
        7.5,  # tf_flange_thickness
        6.4,  # tw_web_thickness
        90,  # bf_flange_width
        65.0,  # a_flange_angle
        97,  # a_cross_sectional_area
        45.6,  # gsp_mass_per_single_pile
        6780,  # i_y_moment_inertia
        600,  # w_el_y_elastic_section_modulus
        697,  # s_y_static_moment
        690,  # w_pl_y_plastic_section_modulus
        76,  # gw_mass_per_m
        8.36,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    PU_7 = (
        "PU 7",
        600,  # b_width_single_pile
        280,  # h_height_pile
        6.0,  # tf_flange_thickness
        6.0,  # tw_web_thickness
        112,  # bf_flange_width
        60.0,  # a_flange_angle
        90,  # a_cross_sectional_area
        42.2,  # gsp_mass_per_single_pile
        8940,  # i_y_moment_inertia
        640,  # w_el_y_elastic_section_modulus
        750,  # s_y_static_moment
        736,  # w_pl_y_plastic_section_modulus
        70,  # gw_mass_per_m
        9.97,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    PU_7R = (
        "PU 7R",
        600,  # b_width_single_pile
        226,  # h_height_pile
        8.5,  # tf_flange_thickness
        7.1,  # tw_web_thickness
        90,  # bf_flange_width
        65.0,  # a_flange_angle
        106,  # a_cross_sectional_area
        49.9,  # gsp_mass_per_single_pile
        7570,  # i_y_moment_inertia
        670,  # w_el_y_elastic_section_modulus
        779,  # s_y_static_moment
        770,  # w_pl_y_plastic_section_modulus
        83,  # gw_mass_per_m
        8.45,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    PU_8 = (
        "PU 8",
        600,  # b_width_single_pile
        280,  # h_height_pile
        6.5,  # tf_flange_thickness
        6.3,  # tw_web_thickness
        112,  # bf_flange_width
        60.0,  # a_flange_angle
        94,  # a_cross_sectional_area
        44.3,  # gsp_mass_per_single_pile
        9580,  # i_y_moment_inertia
        685,  # w_el_y_elastic_section_modulus
        800,  # s_y_static_moment
        787,  # w_pl_y_plastic_section_modulus
        74,  # gw_mass_per_m
        10.1,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    PU_8R = (
        "PU 8R",
        600,  # b_width_single_pile
        280,  # h_height_pile
        8.0,  # tf_flange_thickness
        8.0,  # tw_web_thickness
        112,  # bf_flange_width
        60.0,  # a_flange_angle
        116,  # a_cross_sectional_area
        54.5,  # gsp_mass_per_single_pile
        11620,  # i_y_moment_inertia
        830,  # w_el_y_elastic_section_modulus
        983,  # s_y_static_moment
        954,  # w_pl_y_plastic_section_modulus
        91,  # gw_mass_per_m
        10.01,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    PU_9 = (
        "PU 9",
        600,  # b_width_single_pile
        280,  # h_height_pile
        7.5,  # tf_flange_thickness
        6.9,  # tw_web_thickness
        112,  # bf_flange_width
        60.0,  # a_flange_angle
        103,  # a_cross_sectional_area
        48.7,  # gsp_mass_per_single_pile
        10830,  # i_y_moment_inertia
        775,  # w_el_y_elastic_section_modulus
        905,  # s_y_static_moment
        891,  # w_pl_y_plastic_section_modulus
        81,  # gw_mass_per_m
        10.25,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
        "ArcelorMittal",  # manufacturer
    )

    PU_9R = (
        "PU 9R",
        600,  # b_width_single_pile
        280,  # h_height_pile
        9.0,  # tf_flange_thickness
        8.7,  # tw_web_thickness
        112,  # bf_flange_width
        60.0,  # a_flange_angle
        125,  # a_cross_sectional_area
        58.8,  # gsp_mass_per_single_pile
        12830,  # i_y_moment_inertia
        915,  # w_el_y_elastic_section_modulus
        1083,  # s_y_static_moment
        1052,  # w_pl_y_plastic_section_modulus
        98,  # gw_mass_per_m
        10.13,  # radius_of_gyration_y_y
        1.3,  # al_coating_area
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
        """Initialize GU/PU sheet pile profile.

        This method sets the profile's alias, dimensions, and properties.

        Parameters
        ----------
        alias: str
            Name of the sheet pile profile.
            For example: "PU 18".
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
        self.sheet_pile_type = "U-Section"

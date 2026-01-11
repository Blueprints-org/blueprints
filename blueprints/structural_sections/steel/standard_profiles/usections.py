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

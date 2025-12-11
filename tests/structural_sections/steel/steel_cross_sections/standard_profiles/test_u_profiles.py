"""Test the GU enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.usections import USections


class TestUProfiles:
    """Tests for the GU enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert USections.GU_6N.value == (
            "GU 6N",
            600,
            309,
            6.0,
            6.0,
            248,
            42.5,
            89.0,
            41.9,
            9670,
            625,
            375,
            765,
            69.9,
            10.43,
            1.26,
            "ArcelorMittal",
        )
        assert USections.PU_32_PLUS_1.value == (
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

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "GU 6N" in [e.value[0] for e in USections]
        assert "PU 12" in [e.value[0] for e in USections]
        assert "PU 32+1" in [e.value[0] for e in USections]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in USections]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = USections.GU_6N
        assert profile.alias == "GU 6N"
        assert profile.b_width_single_pile == 600
        assert profile.h_height_pile == 309
        assert profile.tf_flange_thickness == 6.0
        assert profile.tw_web_thickness == 6.0
        assert profile.bf_flange_width == 248
        assert profile.a_flange_angle == 42.5
        assert profile.a_cross_sectional_area == 89.0
        assert profile.gsp_mass_per_single_pile == 41.9
        assert profile.i_y_moment_inertia == 9670
        assert profile.w_el_y_elastic_section_modulus == 625
        assert profile.s_y_static_moment == 375
        assert profile.w_pl_y_plastic_section_modulus == 765
        assert profile.gw_mass_per_m == 69.9
        assert profile.radius_of_gyration_y_y == 10.43
        assert profile.al_coating_area == 1.26
        assert profile.manufacturer == "ArcelorMittal"
        assert profile.sheet_pile_type == "U-Section"

    def test_profile_count(self) -> None:
        """Test that all profiles are present."""
        # There should be 66 GU/PU profiles (40 existing + 26 old profiles)
        assert len(USections) == 66

    def test_specific_profiles(self) -> None:
        """Test specific profiles from the JSON data."""
        # Test GU 33N
        profile = USections.GU_33N
        assert profile.alias == "GU 33N"
        assert profile.h_height_pile == 452
        assert profile.tf_flange_thickness == 20.5
        assert profile.tw_web_thickness == 11.4

        # Test PU 12
        profile = USections.PU_12
        assert profile.alias == "PU 12"
        assert profile.h_height_pile == 360
        assert profile.tf_flange_thickness == 9.8
        assert profile.tw_web_thickness == 9.0

        # Test GU 16-400
        profile = USections.GU_16_400
        assert profile.alias == "GU 16-400"
        assert profile.b_width_single_pile == 400
        assert profile.h_height_pile == 290
        assert profile.a_flange_angle == 82.1

    def test_old_profiles(self) -> None:
        """Test some old U-section profiles from the JSON data."""
        # Test GU 13-500
        profile = USections.GU_13_500
        assert profile.alias == "GU 13-500"
        assert profile.b_width_single_pile == 500
        assert profile.h_height_pile == 340
        assert profile.tf_flange_thickness == 9.0
        assert profile.tw_web_thickness == 8.5
        assert profile.a_cross_sectional_area == 144
        assert profile.gsp_mass_per_single_pile == 56.6
        assert profile.i_y_moment_inertia == 19640

        # Test JSP 3 (has estimated tw)
        profile = USections.JSP_3
        assert profile.alias == "JSP 3"
        assert profile.b_width_single_pile == 400
        assert profile.h_height_pile == 200
        assert profile.tf_flange_thickness == 10.5
        assert profile.tw_web_thickness == 8.4  # Estimated value

        # Test L 2S
        profile = USections.L_2S
        assert profile.alias == "L 2S"
        assert profile.b_width_single_pile == 400
        assert profile.h_height_pile == 170
        assert profile.tf_flange_thickness == 15.5

        # Test PU 11R
        profile = USections.PU_11R
        assert profile.alias == "PU 11R"
        assert profile.b_width_single_pile == 600
        assert profile.h_height_pile == 360

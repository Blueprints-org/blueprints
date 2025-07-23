"""Test the AZ enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.az import AZ


class TestAZ:
    """Tests for the AZ enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert AZ.AZ_18.value == (
            "AZ 18",
            630,
            380,
            9.5,
            9.5,
            348,
            55.4,
            150.4,
            74.4,
            34200,
            1800,
            1050,
            2104,
            118.1,
            15.07,
            1.35,
            "ArcelorMittal",
        )
        assert AZ.AZ_27_800.value == (
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

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "AZ 18" in [e.value[0] for e in AZ]
        assert "AZ 26" in [e.value[0] for e in AZ]
        assert "AZ 27-800" in [e.value[0] for e in AZ]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in AZ]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = AZ.AZ_18
        assert profile.alias == "AZ 18"
        assert profile.b_width_single_pile == 630
        assert profile.h_height_pile == 380
        assert profile.tf_flange_thickness == 9.5
        assert profile.tw_web_thickness == 9.5
        assert profile.bf_flange_width == 348
        assert profile.a_flange_angle == 55.4
        assert profile.a_cross_sectional_area == 150.4
        assert profile.gsp_mass_per_single_pile == 74.4
        assert profile.i_y_moment_inertia == 34200
        assert profile.w_el_y_elastic_section_modulus == 1800
        assert profile.s_y_static_moment == 1050
        assert profile.w_pl_y_plastic_section_modulus == 2104
        assert profile.gw_mass_per_m == 118.1
        assert profile.radius_of_gyration_y_y == 15.07
        assert profile.al_coating_area == 1.35
        assert profile.manufacturer == "ArcelorMittal"
        assert profile.sheet_pile_type == "Z-Section"

    def test_profile_count(self) -> None:
        """Test that all profiles are present."""
        # There should be 36 AZ profiles
        assert len(AZ) == 36

    def test_specific_profiles(self) -> None:
        """Test specific profiles from the JSON data."""
        # Test AZ 18-10/10
        profile = AZ.AZ_18_10_10
        assert profile.alias == "AZ 18-10/10"
        assert profile.h_height_pile == 381
        assert profile.tf_flange_thickness == 10.0
        assert profile.tw_web_thickness == 10.0

        # Test AZ 26
        profile = AZ.AZ_26
        assert profile.alias == "AZ 26"
        assert profile.h_height_pile == 427
        assert profile.tf_flange_thickness == 13.0
        assert profile.tw_web_thickness == 12.2

        # Test AZ 12-770
        profile = AZ.AZ_12_770
        assert profile.alias == "AZ 12-770"
        assert profile.b_width_single_pile == 770
        assert profile.h_height_pile == 344
        assert profile.a_flange_angle == 39.5

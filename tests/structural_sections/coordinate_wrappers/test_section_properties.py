"""Tests for BPSectionProperties."""

from dataclasses import fields
from typing import NamedTuple

import numpy as np
import pytest
from sectionproperties.analysis import Section
from sectionproperties.post.post import SectionProperties as SpSectionProperties
from sectionproperties.pre.library import angle_section

from blueprints.structural_sections import BPSectionProperties
from blueprints.structural_sections.geometric_profiles.rectangle import RectangularProfile


class PropertyMapping(NamedTuple):
    """How a Blueprints property relates to the raw sectionproperties result.

    bp: name of the Blueprints property.
    sp: name of the raw sectionproperties property it is taken from (bp = sign * sp).
    sign: +1 or -1.
    mirrored: name of the property of the sectionproperties result of the mirrored section that has the same value
        (the mirrored section has sectionproperties axes x, y that are the Blueprints axes y, z), None if it cannot be compared.
    """

    bp: str
    sp: str
    sign: int
    mirrored: str | None


# Every property of sectionproperties, written out by hand (not derived from the implementation).
# The plus/minus labels of properties about the z-axis and about the 22-axis swap, because positive y is to the left.
MAPPING = [
    PropertyMapping("bp_area", "area", 1, "area"),
    PropertyMapping("bp_perimeter", "perimeter", 1, "perimeter"),
    PropertyMapping("bp_mass", "mass", 1, "mass"),
    PropertyMapping("bp_ea", "ea", 1, "ea"),
    PropertyMapping("bp_ga", "ga", 1, "ga"),
    PropertyMapping("bp_nu_eff", "nu_eff", 1, "nu_eff"),
    PropertyMapping("bp_e_eff", "e_eff", 1, "e_eff"),
    PropertyMapping("bp_g_eff", "g_eff", 1, "g_eff"),
    PropertyMapping("bp_qy", "qx", 1, "qx"),
    PropertyMapping("bp_qz", "qy", -1, "qy"),
    PropertyMapping("bp_iyy_g", "ixx_g", 1, "ixx_g"),
    PropertyMapping("bp_izz_g", "iyy_g", 1, "iyy_g"),
    PropertyMapping("bp_iyz_g", "ixy_g", -1, "ixy_g"),
    PropertyMapping("bp_cy", "cx", -1, "cx"),
    PropertyMapping("bp_cz", "cy", 1, "cy"),
    PropertyMapping("bp_iyy_c", "ixx_c", 1, "ixx_c"),
    PropertyMapping("bp_izz_c", "iyy_c", 1, "iyy_c"),
    PropertyMapping("bp_iyz_c", "ixy_c", -1, "ixy_c"),
    PropertyMapping("bp_zyy_plus", "zxx_plus", 1, "zxx_plus"),
    PropertyMapping("bp_zyy_minus", "zxx_minus", 1, "zxx_minus"),
    PropertyMapping("bp_zzz_plus", "zyy_minus", 1, "zyy_plus"),
    PropertyMapping("bp_zzz_minus", "zyy_plus", 1, "zyy_minus"),
    PropertyMapping("bp_ry_c", "rx_c", 1, "rx_c"),
    PropertyMapping("bp_rz_c", "ry_c", 1, "ry_c"),
    PropertyMapping("bp_i11_c", "i11_c", 1, "i11_c"),
    PropertyMapping("bp_i22_c", "i22_c", 1, "i22_c"),
    PropertyMapping("bp_phi", "phi", -1, "phi"),
    PropertyMapping("bp_z11_plus", "z11_minus", 1, "z11_plus"),
    PropertyMapping("bp_z11_minus", "z11_plus", 1, "z11_minus"),
    PropertyMapping("bp_z22_plus", "z22_plus", 1, "z22_plus"),
    PropertyMapping("bp_z22_minus", "z22_minus", 1, "z22_minus"),
    PropertyMapping("bp_r11_c", "r11_c", 1, "r11_c"),
    PropertyMapping("bp_r22_c", "r22_c", 1, "r22_c"),
    PropertyMapping("bp_my_yy", "my_xx", 1, "my_xx"),
    PropertyMapping("bp_my_zz", "my_yy", 1, "my_yy"),
    PropertyMapping("bp_my_11", "my_11", 1, "my_11"),
    PropertyMapping("bp_my_22", "my_22", 1, "my_22"),
    PropertyMapping("bp_j", "j", 1, "j"),
    PropertyMapping("bp_omega", "omega", 1, None),
    PropertyMapping("bp_psi_shear", "psi_shear", 1, None),
    PropertyMapping("bp_phi_shear", "phi_shear", 1, None),
    PropertyMapping("bp_delta_s", "delta_s", 1, "delta_s"),
    PropertyMapping("bp_y_se", "x_se", -1, "x_se"),
    PropertyMapping("bp_z_se", "y_se", 1, "y_se"),
    PropertyMapping("bp_y11_se", "x11_se", 1, "x11_se"),
    PropertyMapping("bp_z22_se", "y22_se", -1, "y22_se"),
    PropertyMapping("bp_y_st", "x_st", -1, "x_st"),
    PropertyMapping("bp_z_st", "y_st", 1, "y_st"),
    PropertyMapping("bp_gamma", "gamma", 1, "gamma"),
    PropertyMapping("bp_a_sy", "a_sx", 1, "a_sx"),
    PropertyMapping("bp_a_sz", "a_sy", 1, "a_sy"),
    PropertyMapping("bp_a_syz", "a_sxy", -1, "a_sxy"),
    PropertyMapping("bp_a_s11", "a_s11", 1, "a_s11"),
    PropertyMapping("bp_a_s22", "a_s22", 1, "a_s22"),
    PropertyMapping("bp_beta_y_plus", "beta_x_plus", 1, "beta_x_plus"),
    PropertyMapping("bp_beta_y_minus", "beta_x_minus", 1, "beta_x_minus"),
    PropertyMapping("bp_beta_z_plus", "beta_y_minus", 1, "beta_y_plus"),
    PropertyMapping("bp_beta_z_minus", "beta_y_plus", 1, "beta_y_minus"),
    PropertyMapping("bp_beta_11_plus", "beta_11_minus", 1, "beta_11_plus"),
    PropertyMapping("bp_beta_11_minus", "beta_11_plus", 1, "beta_11_minus"),
    PropertyMapping("bp_beta_22_plus", "beta_22_plus", 1, "beta_22_plus"),
    PropertyMapping("bp_beta_22_minus", "beta_22_minus", 1, "beta_22_minus"),
    PropertyMapping("bp_y_pc", "x_pc", -1, "x_pc"),
    PropertyMapping("bp_z_pc", "y_pc", 1, "y_pc"),
    PropertyMapping("bp_y11_pc", "x11_pc", 1, "x11_pc"),
    PropertyMapping("bp_z22_pc", "y22_pc", -1, "y22_pc"),
    PropertyMapping("bp_syy", "sxx", 1, "sxx"),
    PropertyMapping("bp_szz", "syy", 1, "syy"),
    PropertyMapping("bp_sf_yy_plus", "sf_xx_plus", 1, "sf_xx_plus"),
    PropertyMapping("bp_sf_yy_minus", "sf_xx_minus", 1, "sf_xx_minus"),
    PropertyMapping("bp_sf_zz_plus", "sf_yy_minus", 1, "sf_yy_plus"),
    PropertyMapping("bp_sf_zz_minus", "sf_yy_plus", 1, "sf_yy_minus"),
    PropertyMapping("bp_s11", "s11", 1, "s11"),
    PropertyMapping("bp_s22", "s22", 1, "s22"),
    PropertyMapping("bp_sf_11_plus", "sf_11_minus", 1, "sf_11_plus"),
    PropertyMapping("bp_sf_11_minus", "sf_11_plus", 1, "sf_11_minus"),
    PropertyMapping("bp_sf_22_plus", "sf_22_plus", 1, "sf_22_plus"),
    PropertyMapping("bp_sf_22_minus", "sf_22_minus", 1, "sf_22_minus"),
]


def _calculate(geometry) -> SpSectionProperties:  # noqa: ANN001
    """Calculate all properties of a sectionproperties geometry."""
    geometry.create_mesh(mesh_sizes=[5.0])
    section = Section(geometry)
    section.calculate_geometric_properties()
    section.calculate_warping_properties()
    section.calculate_plastic_properties()
    return section.section_props


@pytest.fixture(scope="module")
def sp_props() -> SpSectionProperties:
    """Raw sectionproperties result of an asymmetric angle section."""
    return _calculate(angle_section(d=100.0, b=60.0, t=10.0, r_r=0.0, r_t=0.0, n_r=1))


@pytest.fixture(scope="module")
def sp_props_mirrored() -> SpSectionProperties:
    """Raw sectionproperties result of the same angle section, mirrored in the vertical axis (x -> -x)."""
    geometry = angle_section(d=100.0, b=60.0, t=10.0, r_r=0.0, r_t=0.0, n_r=1)
    return _calculate(geometry.mirror_section(axis="y", mirror_point=(0.0, 0.0)))


@pytest.fixture(scope="module")
def from_raw(sp_props: SpSectionProperties) -> BPSectionProperties:
    """The Blueprints version of the raw sectionproperties result."""
    return BPSectionProperties.from_sectionproperties(sp_props)


@pytest.fixture
def rectangle() -> RectangularProfile:
    """Rectangle of 100 (width, horizontal) x 200 (height, vertical) with its centroid at (100, 250)."""
    return RectangularProfile(name="Rectangle", width=100.0, height=200.0, x=100.0, y=250.0)


@pytest.fixture
def bp_props(rectangle: RectangularProfile) -> BPSectionProperties:
    """All section properties of the rectangle in the Blueprints coordinate system."""
    return rectangle.section_properties(geometric=True, plastic=True, warping=True)


class TestBPSectionProperties:
    """Tests for BPSectionProperties."""

    def test_all_attributes_have_bp_prefix(self) -> None:
        """Every attribute must carry the bp_ prefix."""
        names = [field.name for field in fields(BPSectionProperties)]
        assert names
        assert all(name.startswith("bp_") for name in names)

    def test_asdict_keys_have_bp_prefix(self, bp_props: BPSectionProperties) -> None:
        """Return the bp_ prefixed names from asdict."""
        result = bp_props.asdict()
        assert set(result) == {field.name for field in fields(BPSectionProperties)}
        assert all(key.startswith("bp_") for key in result)

    def test_no_unprefixed_axis_related_names(self, bp_props: BPSectionProperties) -> None:
        """Everything related to an axis, including the principal axes, is only available with the bp_ prefix."""
        names = ("ixx_c", "iyy_c", "sxx", "syy", "zxx_plus", "zyy_plus", "cx", "cy", "qx", "a_sx", "i11_c", "i22_c", "r11_c", "r22_c")
        for name in (*names, "my_11", "my_22", "s11", "s22", "a_s11", "a_s22", "z11_plus", "phi", "omega", "bp_not_existing"):
            assert not hasattr(bp_props, name)

    def test_plain_scalars_work_without_prefix(self, bp_props: BPSectionProperties) -> None:
        """Plain scalars without any relation to the axes are available with and without the bp_ prefix."""
        names = ("area", "perimeter", "mass", "ea", "ga", "nu_eff", "e_eff", "g_eff", "j", "gamma", "delta_s")
        for name in names:
            assert getattr(bp_props, name) == getattr(bp_props, f"bp_{name}")
        assert bp_props.area == pytest.approx(20000.0, rel=1e-6)
        assert bp_props.j is not None

    def test_unprefixed_names_are_not_in_asdict(self, bp_props: BPSectionProperties) -> None:
        """Asdict only contains the bp_ names, so there is a single key per property."""
        assert "area" not in bp_props.asdict()
        assert "bp_area" in bp_props.asdict()

    def test_unprefixed_names_are_read_only(self, bp_props: BPSectionProperties) -> None:
        """Only the bp_ attribute can be changed, so both names can never disagree."""
        with pytest.raises(AttributeError):
            bp_props.area = 1.0  # type: ignore[misc]

    def test_profile_returns_bp_properties_by_default(self, rectangle: RectangularProfile) -> None:
        """Profile.section_properties returns the Blueprints wrapper without any opt-in."""
        assert isinstance(rectangle.section_properties(), BPSectionProperties)

    def test_not_calculated_properties_are_none(self, rectangle: RectangularProfile) -> None:
        """Properties that were not requested stay None."""
        props = rectangle.section_properties(geometric=True, plastic=False, warping=False)
        assert props.bp_area is not None
        assert props.bp_syy is None
        assert props.bp_gamma is None

    def test_general_properties(self, bp_props: BPSectionProperties) -> None:
        """Orientation independent properties."""
        assert bp_props.bp_area == pytest.approx(20000.0, rel=1e-6)
        assert bp_props.bp_perimeter == pytest.approx(600.0, rel=1e-6)

    def test_centroid(self, bp_props: BPSectionProperties) -> None:
        """Positive y points to the left, so a centroid at x=100 ends up at y=-100."""
        assert bp_props.bp_cy == pytest.approx(-100.0, rel=1e-6)
        assert bp_props.bp_cz == pytest.approx(250.0, rel=1e-6)

    def test_first_moments_of_area(self, bp_props: BPSectionProperties) -> None:
        """First moments are taken about the Blueprints axes."""
        assert bp_props.bp_qy == pytest.approx(20000.0 * 250.0, rel=1e-6)
        assert bp_props.bp_qz == pytest.approx(20000.0 * -100.0, rel=1e-6)

    def test_second_moments_of_area(self, bp_props: BPSectionProperties) -> None:
        """Iyy is about the horizontal axis (height governs), Izz about the vertical axis."""
        assert bp_props.bp_iyy_c == pytest.approx(100.0 * 200.0**3 / 12, rel=1e-6)
        assert bp_props.bp_izz_c == pytest.approx(200.0 * 100.0**3 / 12, rel=1e-6)
        assert bp_props.bp_iyz_c == pytest.approx(0.0, abs=1e-3)

    def test_section_and_plastic_moduli(self, bp_props: BPSectionProperties) -> None:
        """Moduli about y are governed by the height, about z by the width."""
        assert bp_props.bp_zyy_plus == pytest.approx(100.0 * 200.0**2 / 6, rel=1e-6)
        assert bp_props.bp_zyy_minus == pytest.approx(100.0 * 200.0**2 / 6, rel=1e-6)
        assert bp_props.bp_zzz_plus == pytest.approx(200.0 * 100.0**2 / 6, rel=1e-6)
        assert bp_props.bp_zzz_minus == pytest.approx(200.0 * 100.0**2 / 6, rel=1e-6)
        assert bp_props.bp_syy == pytest.approx(100.0 * 200.0**2 / 4, rel=1e-6)
        assert bp_props.bp_szz == pytest.approx(200.0 * 100.0**2 / 4, rel=1e-6)

    def test_warping_properties_present(self, bp_props: BPSectionProperties) -> None:
        """Warping results are available when requested."""
        assert bp_props.bp_j is not None
        assert isinstance(bp_props.bp_omega, np.ndarray)

    def test_all_sectionproperties_fields_are_mapped(self) -> None:
        """Every field of the raw sectionproperties result maps to exactly one Blueprints property, and vice versa."""
        sp_names = [row.sp for row in MAPPING]
        assert len(set(sp_names)) == len(sp_names)
        assert set(sp_names) == {field.name for field in fields(SpSectionProperties)}
        bp_names = [row.bp for row in MAPPING]
        assert len(set(bp_names)) == len(bp_names)
        assert set(bp_names) == {field.name for field in fields(BPSectionProperties)}

    def test_raw_values_are_all_calculated(self, sp_props: SpSectionProperties) -> None:
        """The reference section has a value for every property, so no mapping is tested against None."""
        assert [field.name for field in fields(sp_props) if getattr(sp_props, field.name) is None] == []

    @pytest.mark.parametrize("row", MAPPING, ids=[row.bp for row in MAPPING])
    def test_every_property_is_converted_from_the_raw_value(
        self, row: PropertyMapping, sp_props: SpSectionProperties, from_raw: BPSectionProperties
    ) -> None:
        """Each Blueprints value is the (sign flipped) raw value of the property it is mapped to."""
        raw = getattr(sp_props, row.sp)
        assert np.allclose(getattr(from_raw, row.bp), row.sign * raw, rtol=1e-12, atol=0.0)

    def test_sign_flips_are_not_vacuous(self, sp_props: SpSectionProperties) -> None:
        """The reference section is asymmetric, so every property that changes sign is non zero."""
        for row in MAPPING:
            if row.sign == -1:
                assert np.any(np.abs(getattr(sp_props, row.sp)) > 1e-6), row.bp

    @pytest.mark.parametrize("row", [row for row in MAPPING if row.mirrored is not None], ids=lambda row: row.bp)
    def test_property_equals_sectionproperties_of_the_mirrored_section(
        self, row: PropertyMapping, from_raw: BPSectionProperties, sp_props_mirrored: SpSectionProperties, sp_props: SpSectionProperties
    ) -> None:
        """Independent check of the whole mapping.

        Mirroring the section in sectionproperties (x -> -x) gives a section whose sectionproperties x, y
        axes are the Blueprints y, z axes of the original section. So every Blueprints property must equal the
        sectionproperties property of the mirrored section that has the same axis letters (x -> y, y -> z).
        """
        assert row.mirrored is not None
        # sanity check that the mirroring did what is expected: x is flipped, y is not
        assert sp_props_mirrored.cx == pytest.approx(-sp_props.cx)
        assert sp_props_mirrored.cy == pytest.approx(sp_props.cy)

        expected = getattr(sp_props_mirrored, row.mirrored)
        actual = getattr(from_raw, row.bp)
        if row.bp == "bp_phi":
            # a principal axis angle is only defined up to 180 degrees
            assert (actual - expected + 90.0) % 180.0 - 90.0 == pytest.approx(0.0, abs=0.5)
        else:
            # the finite element mesh of the mirrored section is not exactly the mirrored mesh
            assert actual == pytest.approx(expected, rel=2e-2, abs=1e-2)

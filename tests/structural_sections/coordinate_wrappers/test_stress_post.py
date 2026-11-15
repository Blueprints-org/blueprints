"""Tests for BPStressPost."""

from unittest.mock import MagicMock

import numpy as np
import pytest

from blueprints.structural_sections import BPStressPost
from blueprints.structural_sections.geometric_profiles.rectangle import RectangularProfile


@pytest.fixture
def rectangle() -> RectangularProfile:
    """Rectangle of 100 (width, horizontal) x 200 (height, vertical)."""
    return RectangularProfile(name="Rectangle", width=100.0, height=200.0, x=0.0, y=0.0)


class TestBPStressPost:
    """Tests for BPStressPost."""

    def test_calculate_stress_returns_bp_stress_post_by_default(self, rectangle: RectangularProfile) -> None:
        """Profile.calculate_stress returns the Blueprints wrapper without any opt-in."""
        assert isinstance(rectangle.calculate_stress(n=1.0), BPStressPost)

    def test_get_stress_keys_are_in_blueprints_frame(self, rectangle: RectangularProfile) -> None:
        """Stress keys use x for the longitudinal direction and y, z for the section plane."""
        stress = rectangle.calculate_stress(n=1.0, v_y=1.0, v_z=1.0, m_x=1.0, m_y=1.0, m_z=1.0).get_stress()[0]
        for key in (
            "bp_sig_xx",
            "bp_sig_xy",
            "bp_sig_xz",
            "bp_sig_xyz",
            "bp_sig_xx_my",
            "bp_sig_xx_mz",
            "bp_sig_xyz_vy",
            "bp_sig_xyz_vz",
            "bp_sig_xyz_mx",
            "bp_sig_vm",
        ):
            assert key in stress
        assert all(key.startswith("bp_") for key in stress)

    def test_axial_force(self, rectangle: RectangularProfile) -> None:
        """A tensile normal force gives a uniform tensile stress of N / A."""
        stress = rectangle.calculate_stress(n=20.0).get_stress()[0]
        assert np.allclose(stress["bp_sig_xx_n"], 1.0)

    def test_bending_my_follows_z(self, rectangle: RectangularProfile) -> None:
        """Bending about the horizontal y-axis varies over the height and is antisymmetric."""
        sig = rectangle.calculate_stress(m_y=1.0).get_stress()[0]["bp_sig_xx_my"]
        assert np.max(sig) == pytest.approx(-np.min(sig), rel=1e-6)
        assert np.max(sig) == pytest.approx(1.0e6 / (100.0 * 200.0**2 / 6), rel=1e-6)

    def test_bending_mz_follows_y(self, rectangle: RectangularProfile) -> None:
        """Bending about the vertical z-axis varies over the width."""
        sig = rectangle.calculate_stress(m_z=1.0).get_stress()[0]["bp_sig_xx_mz"]
        assert np.max(sig) == pytest.approx(1.0e6 / (200.0 * 100.0**2 / 6), rel=1e-6)

    def test_shear_in_y_and_z_are_swapped_versus_sectionproperties(self, rectangle: RectangularProfile) -> None:
        """Vy in Blueprints is the horizontal shear force, Vz the vertical one."""
        post = rectangle.calculate_stress(v_y=10.0, v_z=20.0)
        sp_stress = post._sp_stress_post.get_stress()[0]  # noqa: SLF001
        bp_stress = post.get_stress()[0]
        assert np.allclose(bp_stress["bp_sig_xyz_vy"], sp_stress["sig_zxy_vx"])
        assert np.allclose(bp_stress["bp_sig_xyz_vz"], sp_stress["sig_zxy_vy"])
        assert np.allclose(bp_stress["bp_sig_xy_vy"], -sp_stress["sig_zx_vx"])
        assert np.allclose(bp_stress["bp_sig_xz_vz"], sp_stress["sig_zy_vy"])

    def test_plot_stress_translates_label_and_title(self) -> None:
        """Blueprints stress labels are translated to sectionproperties labels and get a Blueprints title."""
        sp_post = MagicMock()
        BPStressPost(sp_post).plot_stress(stress="my_xx")
        kwargs = sp_post.plot_stress.call_args.kwargs
        assert kwargs["stress"] == "mxx_zz"
        assert kwargs["title"] == r"Stress Contour Plot - $\sigma_{xx,My}$"
        BPStressPost(sp_post).plot_stress(stress="vz_xyz", title="custom")
        kwargs = sp_post.plot_stress.call_args.kwargs
        assert kwargs["stress"] == "vy_zxy"
        assert kwargs["title"] == "custom"

    def test_plot_stress_rejects_unknown_label(self) -> None:
        """Unknown labels, including sectionproperties labels, are rejected."""
        post = BPStressPost(MagicMock())
        for label in ("unknown", "zz", "mxx_zz"):
            with pytest.raises(ValueError, match="Unknown stress"):
                post.plot_stress(stress=label)

    def test_plot_stress_y_component_is_negated(self, rectangle: RectangularProfile) -> None:
        """The y-component of a shear stress contour has the same sign as the value from get_stress."""
        post = rectangle.calculate_stress(v_y=10.0, v_z=20.0)
        original = post._sp_stress_post  # noqa: SLF001
        flipped = post._with_negated_attribute("sig_zx_vy")  # noqa: SLF001
        assert np.allclose(flipped.material_groups[0].stress_result.sig_zx_vy, -original.material_groups[0].stress_result.sig_zx_vy)
        assert np.allclose(flipped.material_groups[0].stress_result.sig_zy_vy, original.material_groups[0].stress_result.sig_zy_vy)
        # the wrapped post is left untouched
        assert np.allclose(post.get_stress()[0]["bp_sig_xy_vz"], -original.material_groups[0].stress_result.sig_zx_vy)

    def test_plot_stress_draws_blueprints_axes_and_title(self, rectangle: RectangularProfile) -> None:
        """A real contour plot is titled and labelled in Blueprints terms."""
        post = rectangle.calculate_stress(v_y=10.0, v_z=20.0, m_y=5.0)
        ax = post.plot_stress(stress="vz_xy", render=False)
        assert ax.get_title() == r"Stress Contour Plot - $\sigma_{xy,Vz}$"
        assert ax.get_xlabel() == "y"
        assert ax.get_ylabel() == "z"
        # sectionproperties x=+50 (drawn to the right) is Blueprints y=-50
        formatter = ax.xaxis.get_major_formatter()
        assert formatter(50.0, 0) == "-50"
        assert formatter(-50.0, 0) == "50"
        assert formatter(0.0, 0) == "0"

    def test_plot_stress_vector_translates_label_and_title(self) -> None:
        """Vector labels are translated to sectionproperties labels and get a Blueprints title."""
        sp_post = MagicMock()
        post = BPStressPost(sp_post)
        for bp_label, sp_label in (("mx_xyz", "mzz_zxy"), ("vy_xyz", "vx_zxy"), ("vz_xyz", "vy_zxy"), ("v_xyz", "v_zxy"), ("xyz", "zxy")):
            post.plot_stress_vector(stress=bp_label)
            kwargs = sp_post.plot_stress_vector.call_args.kwargs
            assert kwargs["stress"] == sp_label
            assert kwargs["title"].startswith("Stress Vector Plot - $\\sigma_{xyz")

    def test_plot_stress_vector_rejects_unknown_label(self) -> None:
        """Unknown vector labels are rejected."""
        with pytest.raises(ValueError, match="Unknown stress"):
            BPStressPost(MagicMock()).plot_stress_vector(stress="mx")

    def test_plot_stress_vector_draws_blueprints_axes(self, rectangle: RectangularProfile) -> None:
        """A real vector plot is titled and labelled in Blueprints terms."""
        post = rectangle.calculate_stress(v_y=10.0, v_z=20.0)
        ax = post.plot_stress_vector(stress="v_xyz", render=False)
        assert ax.get_title() == r"Stress Vector Plot - $\sigma_{xyz,\Sigma V}$"
        assert ax.get_xlabel() == "y"
        assert ax.get_ylabel() == "z"

    def test_plot_mohrs_circles_uses_blueprints_coordinates(self) -> None:
        """Positions are given in Blueprints (y, z), converted to sectionproperties (x, y) and shown as such in the title."""
        sp_post = MagicMock()
        BPStressPost(sp_post).plot_mohrs_circles(y=10.0, z=20.0)
        kwargs = sp_post.plot_mohrs_circles.call_args.kwargs
        assert kwargs["x"] == -10.0
        assert kwargs["y"] == 20.0
        assert kwargs["title"] == "Mohr's Circles for 3D Stress State at (10.0, 20.0)"

    def test_section_and_material_groups_are_delegated(self) -> None:
        """The underlying section and material groups stay accessible."""
        sp_post = MagicMock()
        post = BPStressPost(sp_post)
        assert post.section is sp_post.section
        assert post.material_groups is sp_post.material_groups

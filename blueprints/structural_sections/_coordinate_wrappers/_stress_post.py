"""Stress calculation wrapper using the Blueprints coordinate system.

Coordinate System:

    z (vertical, usually strong axis)
        ↑
        |     x (longitudinal beam direction, into screen)
        |    ↗
        |   /
        |  /
        | /
        |/
    ←-----O
    y (horizontal/side, usually weak axis)

Blueprints coordinate system:
    x — longitudinal beam direction (into the screen)
    y — horizontal, positive to the left
    z — vertical, positive upwards

The underlying ``sectionproperties`` library uses:
    x — horizontal, positive to the right
    y — vertical, positive upwards
    z — longitudinal beam direction (into the screen)

Mapping between the two systems:
    bp_y = -sp_x
    bp_z =  sp_y
    bp_x =  sp_z

This module wraps :class:`sectionproperties.post.stress_post.StressPost` so that
all stress directions and sign conventions are expressed in the Blueprints frame.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np
import numpy.typing as npt

if TYPE_CHECKING:
    import matplotlib.axes
    from sectionproperties.analysis.section import MaterialGroup, Section
    from sectionproperties.post.stress_post import StressPost as SpStressPost
    from sectionproperties.pre.pre import Material


def _neg_array(value: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    """Negate a numpy array."""
    return -value


class BPStressPost:
    """Wrapper for StressPost results expressed in the Blueprints coordinate system.

    This class wraps the :class:`sectionproperties.post.stress_post.StressPost` object
    and converts all stress results from the sectionproperties coordinate system to
    the Blueprints coordinate system.

    Parameters
    ----------
    stress_post : SpStressPost
        The sectionproperties StressPost object to wrap.

    Attributes
    ----------
    _sp_stress_post : SpStressPost
        The underlying sectionproperties StressPost object.
    """

    def __init__(self, stress_post: SpStressPost) -> None:
        """Initialize the BPStressPost wrapper.

        Parameters
        ----------
        stress_post : SpStressPost
            The sectionproperties StressPost object to wrap.
        """
        self._sp_stress_post = stress_post

    def get_stress(self) -> list[dict[str, str | npt.NDArray[np.float64]]]:
        """Return the stresses within each material in Blueprints coordinate system.

        Returns
        -------
        list[dict[str, str | npt.NDArray[np.float64]]]
            A list of dictionaries containing the cross-section stresses at each node
            for each material, expressed in the Blueprints coordinate system.

        Note
        ----
        Each list of stresses in the dictionary contains the stresses at every node
        (order from ``node 0`` to ``node n``) in the entire mesh. As a result, when
        the current material does not exist at a node, a value of zero will be
        reported.

        Dictionary keys and values
        --------------------------
        In general the stresses are described by an action followed by a stress
        direction ``(action)_(stress-direction)``, e.g. ``mx_zy`` represents the
        shear stress in the zy direction caused by the torsion ``mx``.

        The following keys are available in each dictionary:

        - ``"material"`` - material name
        - ``"sig_xx_n"`` - normal stress σ_xx,N from axial load N
        - ``"sig_xx_my"`` - normal stress σ_xx,My from bending moment My
        - ``"sig_xx_mz"`` - normal stress σ_xx,Mz from bending moment Mz
        - ``"sig_xx_m11"`` - normal stress σ_xx,M11 from bending moment M11
        - ``"sig_xx_m22"`` - normal stress σ_xx,M22 from bending moment M22
        - ``"sig_xx_m"`` - normal stress σ_xx,ΣM from all bending moments
        - ``"sig_xy_mx"`` - y component of shear stress σ_xy,Mx from torsion Mx
        - ``"sig_xz_mx"`` - z component of shear stress σ_xz,Mx from torsion Mx
        - ``"sig_xyz_mx"`` - resultant shear stress σ_xyz,Mx from torsion Mx
        - ``"sig_xy_vy"`` - y component of shear stress σ_xy,Vy from shear force Vy
        - ``"sig_xz_vy"`` - z component of shear stress σ_xz,Vy from shear force Vy
        - ``"sig_xyz_vy"`` - resultant shear stress σ_xyz,Vy from shear force Vy
        - ``"sig_xy_vz"`` - y component of shear stress σ_xy,Vz from shear force Vz
        - ``"sig_xz_vz"`` - z component of shear stress σ_xz,Vz from shear force Vz
        - ``"sig_xyz_vz"`` - resultant shear stress σ_xyz,Vz from shear force Vz
        - ``"sig_xy_v"`` - y component of shear stress σ_xy,ΣV from all shear forces
        - ``"sig_xz_v"`` - z component of shear stress σ_xz,ΣV from all shear forces
        - ``"sig_xyz_v"`` - resultant shear stress σ_xyz,ΣV from all shear forces
        - ``"sig_xx"`` - combined normal stress σ_xx from all actions
        - ``"sig_xy"`` - y component of shear stress σ_xy from all actions
        - ``"sig_xz"`` - z component of shear stress σ_xz from all actions
        - ``"sig_xyz"`` - resultant shear stress σ_xyz from all actions
        - ``"sig_11"`` - major principal stress σ_11 from all actions
        - ``"sig_33"`` - minor principal stress σ_33 from all actions
        - ``"sig_vm"`` - von Mises stress σ_vM from all actions
        """
        # Get stress from sectionproperties
        sp_stress_list = self._sp_stress_post.get_stress()

        # Convert each material group's stress to Blueprints coordinate system
        bp_stress_list: list[dict[str, str | npt.NDArray[np.float64]]] = []

        for sp_stress in sp_stress_list:
            # Coordinate transformation:
            # bp_x <-> sp_z (longitudinal)
            # bp_y <-> -sp_x (horizontal, sign flipped)
            # bp_z <-> sp_y (vertical)
            #
            # For stress components:
            # sig_xx (bp) <-> sig_zz (sp) - normal stress in longitudinal direction
            # sig_xy (bp) <-> -sig_zx (sp) - shear stress xy component (sign flipped)
            # sig_xz (bp) <-> sig_zy (sp) - shear stress xz component
            # sig_xyz (bp) <-> sig_zxy (sp) - resultant shear stress magnitude (unchanged)

            bp_stress = {
                "material": sp_stress["material"],
                # Normal stresses from axial force and bending
                "sig_xx_n": sp_stress["sig_zz_n"],
                "sig_xx_my": sp_stress["sig_zz_mxx"],  # My (bp) = Mxx (sp)
                "sig_xx_mz": sp_stress["sig_zz_myy"],  # Mz (bp) = Myy (sp)
                "sig_xx_m11": sp_stress["sig_zz_m11"],
                "sig_xx_m22": sp_stress["sig_zz_m22"],
                "sig_xx_m": sp_stress["sig_zz_m"],
                # Shear stresses from torsion Mx (bp) = Mzz (sp)
                "sig_xy_mx": _neg_array(sp_stress["sig_zx_mzz"]),
                "sig_xz_mx": sp_stress["sig_zy_mzz"],
                "sig_xyz_mx": sp_stress["sig_zxy_mzz"],
                # Shear stresses from shear force Vy (bp) = Vx (sp, but sign flipped)
                "sig_xy_vy": _neg_array(sp_stress["sig_zx_vx"]),
                "sig_xz_vy": sp_stress["sig_zy_vx"],
                "sig_xyz_vy": sp_stress["sig_zxy_vx"],
                # Shear stresses from shear force Vz (bp) = Vy (sp)
                "sig_xy_vz": _neg_array(sp_stress["sig_zx_vy"]),
                "sig_xz_vz": sp_stress["sig_zy_vy"],
                "sig_xyz_vz": sp_stress["sig_zxy_vy"],
                # Combined shear stresses from all shear forces
                "sig_xy_v": _neg_array(sp_stress["sig_zx_v"]),
                "sig_xz_v": sp_stress["sig_zy_v"],
                "sig_xyz_v": sp_stress["sig_zxy_v"],
                # Combined stresses from all actions
                "sig_xx": sp_stress["sig_zz"],
                "sig_xy": _neg_array(sp_stress["sig_zx"]),
                "sig_xz": sp_stress["sig_zy"],
                "sig_xyz": sp_stress["sig_zxy"],
                # Principal stresses (invariant under coordinate transformation)
                "sig_11": sp_stress["sig_11"],
                "sig_33": sp_stress["sig_33"],
                # von Mises stress (invariant under coordinate transformation)
                "sig_vm": sp_stress["sig_vm"],
            }

            bp_stress_list.append(bp_stress)

        return bp_stress_list

    def plot_stress(
        self,
        stress: str,
        title: str | None = None,
        cmap: str = "coolwarm",
        stress_limits: tuple[float, float] | None = None,
        normalize: bool = True,
        fmt: str = "{x:.4e}",
        colorbar_label: str = "Stress",
        alpha: float = 0.5,
        material_list: list[Material] | None = None,
        **kwargs: object,
    ) -> matplotlib.axes.Axes:
        """Plot filled stress contours over the finite element mesh.

        This method converts Blueprints stress labels to sectionproperties labels
        and delegates to the underlying StressPost object.

        Parameters
        ----------
        stress : str
            Type of stress to plot in Blueprints coordinate system.
            See notes below for available options.
        title : str | None
            Plot title. If None, uses default plot title for selected stress.
        cmap : str
            Matplotlib color map. Defaults to "coolwarm".
        stress_limits : tuple[float, float] | None
            Custom colorbar stress limits (sig_min, sig_max).
        normalize : bool
            If True, CenteredNorm is used to scale the colormap. Defaults to True.
        fmt : str
            Number formatting string. Defaults to "{x:.4e}".
        colorbar_label : str
            Colorbar label. Defaults to "Stress".
        alpha : float
            Transparency of the mesh outlines: 0 ≤ alpha ≤ 1. Defaults to 0.5.
        material_list : list[Material] | None
            If specified, only plots materials present in the list.
        **kwargs
            Passed to plotting_context.

        Returns
        -------
        matplotlib.axes.Axes
            Matplotlib axes object.

        Notes
        -----
        Available stress types (Blueprints coordinate system):
        - "n_xx" - normal stress from axial load N
        - "my_xx" - normal stress from bending moment My
        - "mz_xx" - normal stress from bending moment Mz
        - "m11_xx" - normal stress from bending moment M11
        - "m22_xx" - normal stress from bending moment M22
        - "m_xx" - normal stress from all bending moments
        - "mx_xy" - y component of shear stress from torsion Mx
        - "mx_xz" - z component of shear stress from torsion Mx
        - "mx_xyz" - resultant shear stress from torsion Mx
        - "vy_xy" - y component of shear stress from shear force Vy
        - "vy_xz" - z component of shear stress from shear force Vy
        - "vy_xyz" - resultant shear stress from shear force Vy
        - "vz_xy" - y component of shear stress from shear force Vz
        - "vz_xz" - z component of shear stress from shear force Vz
        - "vz_xyz" - resultant shear stress from shear force Vz
        - "v_xy" - y component of shear stress from all shear forces
        - "v_xz" - z component of shear stress from all shear forces
        - "v_xyz" - resultant shear stress from all shear forces
        - "xx" - combined normal stress from all actions
        - "xy" - y component of shear stress from all actions
        - "xz" - z component of shear stress from all actions
        - "xyz" - resultant shear stress from all actions
        - "11" - major principal stress from all actions
        - "33" - minor principal stress from all actions
        - "vm" - von Mises stress from all actions
        """
        # Map Blueprints stress labels to sectionproperties labels
        stress_mapping = {
            # Normal stresses
            "n_xx": "n_zz",
            "my_xx": "mxx_zz",
            "mz_xx": "myy_zz",
            "m11_xx": "m11_zz",
            "m22_xx": "m22_zz",
            "m_xx": "m_zz",
            # Torsion shear stresses
            "mx_xy": "mzz_zx",
            "mx_xz": "mzz_zy",
            "mx_xyz": "mzz_zxy",
            # Shear force Vy stresses
            "vy_xy": "vx_zx",
            "vy_xz": "vx_zy",
            "vy_xyz": "vx_zxy",
            # Shear force Vz stresses
            "vz_xy": "vy_zx",
            "vz_xz": "vy_zy",
            "vz_xyz": "vy_zxy",
            # Combined shear stresses
            "v_xy": "v_zx",
            "v_xz": "v_zy",
            "v_xyz": "v_zxy",
            # Combined stresses
            "xx": "zz",
            "xy": "zx",
            "xz": "zy",
            "xyz": "zxy",
            # Principal stresses
            "11": "11",
            "33": "33",
            # von Mises
            "vm": "vm",
        }

        # Convert stress label to sectionproperties format
        sp_stress = stress_mapping.get(stress, stress)

        # Delegate to underlying StressPost object
        return self._sp_stress_post.plot_stress(
            stress=sp_stress,
            title=title,
            cmap=cmap,
            stress_limits=stress_limits,
            normalize=normalize,
            fmt=fmt,
            colorbar_label=colorbar_label,
            alpha=alpha,
            material_list=material_list,
            **kwargs,
        )

    def plot_mohrs_circles(
        self,
        x: float,
        y: float,
        title: str | None = None,
        **kwargs: object,
    ) -> matplotlib.axes.Axes:
        """Plot Mohr's circles of the 3D stress state at position (x, y).

        Note: The coordinates (x, y) are in the sectionproperties coordinate system.

        Parameters
        ----------
        x : float
            x-coordinate of the point (sectionproperties coordinate system).
        y : float
            y-coordinate of the point (sectionproperties coordinate system).
        title : str | None
            Plot title. If None, uses default plot title.
        **kwargs
            Passed to plotting_context.

        Returns
        -------
        matplotlib.axes.Axes
            Matplotlib axes object.
        """
        return self._sp_stress_post.plot_mohrs_circles(x=x, y=y, title=title, **kwargs)

    def plot_stress_vector(
        self,
        stress: str,
        title: str | None = None,
        cmap: str = "YlOrBr",
        normalize: bool = False,
        alpha: float = 0.5,
        material_list: list[Material] | None = None,
        **kwargs: object,
    ) -> tuple[matplotlib.axes.Axes, Any]:
        """Plot stress vectors over the finite element mesh.

        Parameters
        ----------
        stress : str
            Type of stress to plot. Must be a shear stress with direction components.
        title : str | None
            Plot title. If None, uses default plot title for selected stress.
        cmap : str
            Matplotlib color map. Defaults to "YlOrBr".
        normalize : bool
            If True, CenteredNorm is used. Defaults to False.
        alpha : float
            Transparency of the mesh outlines. Defaults to 0.5.
        material_list : list[Material] | None
            If specified, only plots materials present in the list.
        **kwargs
            Passed to plotting_context.

        Returns
        -------
        tuple[matplotlib.axes.Axes, Any]
            Matplotlib axes object and quiver plot object.
        """
        # Map Blueprints stress labels to sectionproperties labels
        stress_mapping = {
            "mx": "mzz",
            "vy": "vx",
            "vz": "vy",
            "v": "v",
        }

        # Convert stress label
        sp_stress = stress_mapping.get(stress, stress)

        # Delegate to underlying StressPost object
        return self._sp_stress_post.plot_stress_vector(
            stress=sp_stress,
            title=title,
            cmap=cmap,
            normalize=normalize,
            alpha=alpha,
            material_list=material_list,
            **kwargs,
        )

    @property
    def section(self) -> Section:
        """Get the underlying section object."""
        return self._sp_stress_post.section

    @property
    def material_groups(self) -> list[MaterialGroup]:
        """Get the material groups."""
        return self._sp_stress_post.material_groups

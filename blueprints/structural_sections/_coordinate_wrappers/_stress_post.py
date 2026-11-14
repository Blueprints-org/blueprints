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

import copy
from typing import TYPE_CHECKING, Any

import numpy as np
import numpy.typing as npt
from matplotlib.ticker import FuncFormatter

if TYPE_CHECKING:
    import matplotlib.axes
    from sectionproperties.analysis.section import MaterialGroup, Section
    from sectionproperties.post.stress_post import StressPost as SpStressPost
    from sectionproperties.pre.pre import Material

# Blueprints contour label -> (sectionproperties label, stress subscript for the title,
# sectionproperties attribute that has to be negated to get the Blueprints y-component, if any).
_CONTOUR_STRESSES: dict[str, tuple[str, str, str | None]] = {
    "n_xx": ("n_zz", "xx,N", None),
    "my_xx": ("mxx_zz", "xx,My", None),
    "mz_xx": ("myy_zz", "xx,Mz", None),
    "m11_xx": ("m11_zz", "xx,M11", None),
    "m22_xx": ("m22_zz", "xx,M22", None),
    "m_xx": ("m_zz", r"xx,\Sigma M", None),
    "mx_xy": ("mzz_zx", "xy,Mx", "sig_zx_mzz"),
    "mx_xz": ("mzz_zy", "xz,Mx", None),
    "mx_xyz": ("mzz_zxy", "xyz,Mx", None),
    "vy_xy": ("vx_zx", "xy,Vy", "sig_zx_vx"),
    "vy_xz": ("vx_zy", "xz,Vy", None),
    "vy_xyz": ("vx_zxy", "xyz,Vy", None),
    "vz_xy": ("vy_zx", "xy,Vz", "sig_zx_vy"),
    "vz_xz": ("vy_zy", "xz,Vz", None),
    "vz_xyz": ("vy_zxy", "xyz,Vz", None),
    "v_xy": ("v_zx", r"xy,\Sigma V", "sig_zx_v"),
    "v_xz": ("v_zy", r"xz,\Sigma V", None),
    "v_xyz": ("v_zxy", r"xyz,\Sigma V", None),
    "xx": ("zz", "xx", None),
    "xy": ("zx", "xy", "sig_zx"),
    "xz": ("zy", "xz", None),
    "xyz": ("zxy", "xyz", None),
    "11": ("11", "11", None),
    "33": ("33", "33", None),
    "vm": ("vm", "vM", None),
}

# Blueprints vector label -> (sectionproperties label, stress subscript for the title).
# The arrows are drawn on screen, which is the same picture in both coordinate systems, so no sign change is needed.
_VECTOR_STRESSES: dict[str, tuple[str, str]] = {
    "mx_xyz": ("mzz_zxy", "xyz,Mx"),
    "vy_xyz": ("vx_zxy", "xyz,Vy"),
    "vz_xyz": ("vy_zxy", "xyz,Vz"),
    "v_xyz": ("v_zxy", r"xyz,\Sigma V"),
    "xyz": ("zxy", "xyz"),
}


def _neg_array(value: str | npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    """Negate a numpy stress array (the str member only exists in the typing of the stress dictionaries)."""
    return -np.asarray(value, dtype=np.float64)


def _to_blueprints_axes(ax: matplotlib.axes.Axes) -> None:
    """Label the axes of a cross-section plot with the Blueprints coordinates y and z.

    The cross-section is drawn exactly as in sectionproperties (positive sectionproperties x to the right).
    Since bp_y = -sp_x, the tick labels of the horizontal axis are negated so that they show y.
    """
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{-value + 0.0:g}"))
    ax.set_xlabel("y")
    ax.set_ylabel("z")
    ax.figure.canvas.draw_idle()


def _invalid_label(label: str, valid: dict[str, Any]) -> ValueError:
    """Create the error for an unknown Blueprints stress label."""
    return ValueError(f"Unknown stress '{label}'. Choose one of: {', '.join(valid)}.")


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

        - ``"bp_material"`` - material name
        - ``"bp_sig_xx_n"`` - normal stress σ_xx,N from axial load N
        - ``"bp_sig_xx_my"`` - normal stress σ_xx,My from bending moment My
        - ``"bp_sig_xx_mz"`` - normal stress σ_xx,Mz from bending moment Mz
        - ``"bp_sig_xx_m11"`` - normal stress σ_xx,M11 from bending moment M11
        - ``"bp_sig_xx_m22"`` - normal stress σ_xx,M22 from bending moment M22
        - ``"bp_sig_xx_m"`` - normal stress σ_xx,ΣM from all bending moments
        - ``"bp_sig_xy_mx"`` - y component of shear stress σ_xy,Mx from torsion Mx
        - ``"bp_sig_xz_mx"`` - z component of shear stress σ_xz,Mx from torsion Mx
        - ``"bp_sig_xyz_mx"`` - resultant shear stress σ_xyz,Mx from torsion Mx
        - ``"bp_sig_xy_vy"`` - y component of shear stress σ_xy,Vy from shear force Vy
        - ``"bp_sig_xz_vy"`` - z component of shear stress σ_xz,Vy from shear force Vy
        - ``"bp_sig_xyz_vy"`` - resultant shear stress σ_xyz,Vy from shear force Vy
        - ``"bp_sig_xy_vz"`` - y component of shear stress σ_xy,Vz from shear force Vz
        - ``"bp_sig_xz_vz"`` - z component of shear stress σ_xz,Vz from shear force Vz
        - ``"bp_sig_xyz_vz"`` - resultant shear stress σ_xyz,Vz from shear force Vz
        - ``"bp_sig_xy_v"`` - y component of shear stress σ_xy,ΣV from all shear forces
        - ``"bp_sig_xz_v"`` - z component of shear stress σ_xz,ΣV from all shear forces
        - ``"bp_sig_xyz_v"`` - resultant shear stress σ_xyz,ΣV from all shear forces
        - ``"bp_sig_xx"`` - combined normal stress σ_xx from all actions
        - ``"bp_sig_xy"`` - y component of shear stress σ_xy from all actions
        - ``"bp_sig_xz"`` - z component of shear stress σ_xz from all actions
        - ``"bp_sig_xyz"`` - resultant shear stress σ_xyz from all actions
        - ``"bp_sig_11"`` - major principal stress σ_11 from all actions
        - ``"bp_sig_33"`` - minor principal stress σ_33 from all actions
        - ``"bp_sig_vm"`` - von Mises stress σ_vM from all actions
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
            # bp_sig_xx (bp) <-> sig_zz (sp) - normal stress in longitudinal direction
            # bp_sig_xy (bp) <-> -sig_zx (sp) - shear stress xy component (sign flipped)
            # bp_sig_xz (bp) <-> sig_zy (sp) - shear stress xz component
            # bp_sig_xyz (bp) <-> sig_zxy (sp) - resultant shear stress magnitude (unchanged)

            bp_stress = {
                "bp_material": sp_stress["material"],
                # Normal stresses from axial force and bending
                "bp_sig_xx_n": sp_stress["sig_zz_n"],
                "bp_sig_xx_my": sp_stress["sig_zz_mxx"],  # My (bp) = Mxx (sp)
                "bp_sig_xx_mz": sp_stress["sig_zz_myy"],  # Mz (bp) = Myy (sp)
                "bp_sig_xx_m11": sp_stress["sig_zz_m11"],
                "bp_sig_xx_m22": sp_stress["sig_zz_m22"],
                "bp_sig_xx_m": sp_stress["sig_zz_m"],
                # Shear stresses from torsion Mx (bp) = Mzz (sp)
                "bp_sig_xy_mx": _neg_array(sp_stress["sig_zx_mzz"]),
                "bp_sig_xz_mx": sp_stress["sig_zy_mzz"],
                "bp_sig_xyz_mx": sp_stress["sig_zxy_mzz"],
                # Shear stresses from shear force Vy (bp) = Vx (sp, but sign flipped)
                "bp_sig_xy_vy": _neg_array(sp_stress["sig_zx_vx"]),
                "bp_sig_xz_vy": sp_stress["sig_zy_vx"],
                "bp_sig_xyz_vy": sp_stress["sig_zxy_vx"],
                # Shear stresses from shear force Vz (bp) = Vy (sp)
                "bp_sig_xy_vz": _neg_array(sp_stress["sig_zx_vy"]),
                "bp_sig_xz_vz": sp_stress["sig_zy_vy"],
                "bp_sig_xyz_vz": sp_stress["sig_zxy_vy"],
                # Combined shear stresses from all shear forces
                "bp_sig_xy_v": _neg_array(sp_stress["sig_zx_v"]),
                "bp_sig_xz_v": sp_stress["sig_zy_v"],
                "bp_sig_xyz_v": sp_stress["sig_zxy_v"],
                # Combined stresses from all actions
                "bp_sig_xx": sp_stress["sig_zz"],
                "bp_sig_xy": _neg_array(sp_stress["sig_zx"]),
                "bp_sig_xz": sp_stress["sig_zy"],
                "bp_sig_xyz": sp_stress["sig_zxy"],
                # Principal stresses (invariant under coordinate transformation)
                "bp_sig_11": sp_stress["sig_11"],
                "bp_sig_33": sp_stress["sig_33"],
                # von Mises stress (invariant under coordinate transformation)
                "bp_sig_vm": sp_stress["sig_vm"],
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
        and delegates to the underlying StressPost object. The values, the default title
        (e.g. σ_xx,My) and the axes (y and z) are all expressed in the Blueprints coordinate system.

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

        Raises
        ------
        ValueError
            If the stress is not one of the options below.

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
        if stress not in _CONTOUR_STRESSES:
            raise _invalid_label(stress, _CONTOUR_STRESSES)
        sp_stress, subscript, negated_attribute = _CONTOUR_STRESSES[stress]

        # sectionproperties draws the cross-section with its own x-axis to the right, which is the same
        # picture as the Blueprints one (y to the left); only the y-component of the shear stress changes sign.
        sp_post = self._sp_stress_post if negated_attribute is None else self._with_negated_attribute(negated_attribute)

        ax = sp_post.plot_stress(
            stress=sp_stress,
            title=title or rf"Stress Contour Plot - $\sigma_{{{subscript}}}$",
            cmap=cmap,
            stress_limits=stress_limits,
            normalize=normalize,
            fmt=fmt,
            colorbar_label=colorbar_label,
            alpha=alpha,
            material_list=material_list,
            **kwargs,
        )
        _to_blueprints_axes(ax)
        return ax

    def _with_negated_attribute(self, attribute: str) -> SpStressPost:
        """Return a shallow copy of the wrapped StressPost in which one stress result is negated."""
        sp_post = copy.copy(self._sp_stress_post)
        groups = []
        for group in self._sp_stress_post.material_groups:
            group_copy = copy.copy(group)
            group_copy.stress_result = copy.copy(group.stress_result)
            setattr(group_copy.stress_result, attribute, -getattr(group.stress_result, attribute))
            groups.append(group_copy)
        sp_post.material_groups = groups
        return sp_post

    def plot_mohrs_circles(
        self,
        y: float,
        z: float,
        title: str | None = None,
        **kwargs: object,
    ) -> matplotlib.axes.Axes:
        """Plot Mohr's circles of the 3D stress state at position (y, z).

        Parameters
        ----------
        y : float
            y-coordinate of the point (Blueprints coordinate system, positive to the left).
        z : float
            z-coordinate of the point (Blueprints coordinate system, positive upwards).
        title : str | None
            Plot title. If None, uses default plot title.
        **kwargs
            Passed to plotting_context.

        Returns
        -------
        matplotlib.axes.Axes
            Matplotlib axes object.
        """
        # bp_y = -sp_x, bp_z = sp_y
        return self._sp_stress_post.plot_mohrs_circles(
            x=-y,
            y=z,
            title=title or f"Mohr's Circles for 3D Stress State at {(y, z)}",
            **kwargs,
        )

    def plot_stress_vector(
        self,
        stress: str,
        title: str | None = None,
        cmap: str = "YlOrBr",
        normalize: bool = False,
        fmt: str = "{x:.4e}",
        colorbar_label: str = "Stress",
        alpha: float = 0.2,
        **kwargs: object,
    ) -> matplotlib.axes.Axes:
        """Plot shear stress vectors over the finite element mesh.

        Parameters
        ----------
        stress : str
            Shear stress to plot, in the Blueprints coordinate system. One of:

            - ``"mx_xyz"`` - shear stress from torsion Mx
            - ``"vy_xyz"`` - shear stress from shear force Vy
            - ``"vz_xyz"`` - shear stress from shear force Vz
            - ``"v_xyz"`` - shear stress from all shear forces
            - ``"xyz"`` - shear stress from all actions
        title : str | None
            Plot title. If None, uses default plot title for selected stress.
        cmap : str
            Matplotlib color map. Defaults to "YlOrBr".
        normalize : bool
            If True, CenteredNorm is used. Defaults to False.
        fmt : str
            Number formatting string. Defaults to "{x:.4e}".
        colorbar_label : str
            Colorbar label. Defaults to "Stress".
        alpha : float
            Transparency of the mesh outlines. Defaults to 0.2.
        **kwargs
            Passed to plotting_context.

        Returns
        -------
        matplotlib.axes.Axes
            Matplotlib axes object.

        Raises
        ------
        ValueError
            If the stress is not one of the options above.
        """
        if stress not in _VECTOR_STRESSES:
            raise _invalid_label(stress, _VECTOR_STRESSES)
        sp_stress, subscript = _VECTOR_STRESSES[stress]

        ax = self._sp_stress_post.plot_stress_vector(
            stress=sp_stress,
            title=title or rf"Stress Vector Plot - $\sigma_{{{subscript}}}$",
            cmap=cmap,
            normalize=normalize,
            fmt=fmt,
            colorbar_label=colorbar_label,
            alpha=alpha,
            **kwargs,
        )
        _to_blueprints_axes(ax)
        return ax

    @property
    def section(self) -> Section:
        """Get the underlying section object."""
        return self._sp_stress_post.section

    @property
    def material_groups(self) -> list[MaterialGroup]:
        """Get the material groups."""
        return self._sp_stress_post.material_groups

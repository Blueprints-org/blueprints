"""Section properties container using the Blueprints coordinate system.

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

This module wraps :class:`sectionproperties.post.post.SectionProperties` so that all
attribute names, sign conventions and ``plus``/``minus`` fibre labels are expressed in
the Blueprints frame as :class:`BPSectionProperties`. Every attribute carries a ``bp_`` prefix, so a
Blueprints value can never be mistaken for the identically named (but differently oriented)
``sectionproperties`` value, e.g. ``bp_iyy_c`` is the second moment of area about the horizontal
Blueprints y-axis, whereas ``iyy_c`` in ``sectionproperties`` is about the vertical axis.

Properties that are plain scalars without any relation to the axes (e.g. the area or the torsion constant)
are identical in both systems, so they are also available without the prefix: ``area`` and
``bp_area`` return the same value.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np
import numpy.typing as npt
from sectionproperties.post.post import SectionProperties as SpSectionProperties


def _neg(value: float | None) -> float | None:
    """Negate a value if it is not ``None``."""
    return -value if value is not None else None


@dataclass
class BPSectionProperties:
    """Section properties expressed in the Blueprints coordinate system.

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

    All attributes are prefixed with ``bp_``. Only properties that are plain scalars without any
    relation to the axes are also available without the prefix (``area`` and ``bp_area`` are the same):
    ``area``, ``perimeter``, ``mass``, ``ea``, ``ga``, ``nu_eff``, ``e_eff``, ``g_eff``, ``j``,
    ``gamma`` and ``delta_s``. The unprefixed names are read-only and are not included in :meth:`asdict`.

    Units follow the geometry the section was
    built from (Blueprints profiles use mm, so areas are in mm², moments of area in mm⁴,
    section moduli in mm³). Properties that are not calculated (e.g. warping properties
    when ``warping=False``) are ``None``.

    The ``plus``/``minus`` suffix of a section modulus, shape factor or monosymmetry
    constant refers to the side of the axis at which it is evaluated: ``plus`` is the
    fibre at the positive coordinate, ``minus`` the fibre at the negative coordinate,
    both in the Blueprints coordinate system (so ``y`` positive is to the left).

    Attributes
    ----------
    bp_area : float | None
        Cross-sectional area.
    bp_perimeter : float | None
        Cross-sectional perimeter.
    bp_mass : float | None
        Cross-sectional mass.
    bp_ea : float | None
        Modulus weighted area (axial rigidity).
    bp_ga : float | None
        Modulus weighted product of shear modulus and area.
    bp_nu_eff : float | None
        Effective Poisson's ratio.
    bp_e_eff : float | None
        Effective elastic modulus.
    bp_g_eff : float | None
        Effective shear modulus.
    bp_qy : float | None
        First moment of area about the y-axis (∫ z dA).
    bp_qz : float | None
        First moment of area about the z-axis (∫ y dA).
    bp_iyy_g : float | None
        Second moment of area about the global y-axis.
    bp_izz_g : float | None
        Second moment of area about the global z-axis.
    bp_iyz_g : float | None
        Product moment of area about the global yz-axes.
    bp_cy : float | None
        y-coordinate of the elastic centroid.
    bp_cz : float | None
        z-coordinate of the elastic centroid.
    bp_iyy_c : float | None
        Second moment of area about the centroidal y-axis.
    bp_izz_c : float | None
        Second moment of area about the centroidal z-axis.
    bp_iyz_c : float | None
        Product moment of area about the centroidal yz-axes.
    bp_zyy_plus : float | None
        Elastic section modulus about the centroidal y-axis for the fibre at
        positive z (top fibre).
    bp_zyy_minus : float | None
        Elastic section modulus about the centroidal y-axis for the fibre at
        negative z (bottom fibre).
    bp_zzz_plus : float | None
        Elastic section modulus about the centroidal z-axis for the fibre at
        positive y.
    bp_zzz_minus : float | None
        Elastic section modulus about the centroidal z-axis for the fibre at
        negative y.
    bp_ry_c : float | None
        Radius of gyration about the centroidal y-axis.
    bp_rz_c : float | None
        Radius of gyration about the centroidal z-axis.
    bp_i11_c : float | None
        Second moment of area about the centroidal principal 11-axis.
    bp_i22_c : float | None
        Second moment of area about the centroidal principal 22-axis.
    bp_phi : float | None
        Principal axis angle [degrees], measured counter-clockwise from the
        positive y-axis to the positive 11-axis in the Blueprints frame.
    bp_z11_plus : float | None
        Elastic section modulus about the principal 11-axis for the fibre at
        positive 22-coordinate.
    bp_z11_minus : float | None
        Elastic section modulus about the principal 11-axis for the fibre at
        negative 22-coordinate.
    bp_z22_plus : float | None
        Elastic section modulus about the principal 22-axis for the fibre at
        positive 11-coordinate.
    bp_z22_minus : float | None
        Elastic section modulus about the principal 22-axis for the fibre at
        negative 11-coordinate.
    bp_r11_c : float | None
        Radius of gyration about the principal 11-axis.
    bp_r22_c : float | None
        Radius of gyration about the principal 22-axis.
    bp_my_yy : float | None
        Yield moment about the y-axis.
    bp_my_zz : float | None
        Yield moment about the z-axis.
    bp_my_11 : float | None
        Yield moment about the 11-axis.
    bp_my_22 : float | None
        Yield moment about the 22-axis.
    bp_j : float | None
        Torsion constant.
    bp_omega : npt.NDArray[np.float64] | None
        Warping function (per mesh node).
    bp_psi_shear : npt.NDArray[np.float64] | None
        Psi shear function (per mesh node).
    bp_phi_shear : npt.NDArray[np.float64] | None
        Phi shear function (per mesh node).
    bp_delta_s : float | None
        Shear factor.
    bp_y_se : float | None
        y-coordinate of the shear centre (elasticity approach).
    bp_z_se : float | None
        z-coordinate of the shear centre (elasticity approach).
    bp_y11_se : float | None
        11-coordinate of the shear centre (elasticity approach).
    bp_z22_se : float | None
        22-coordinate of the shear centre (elasticity approach).
    bp_y_st : float | None
        y-coordinate of the shear centre (Trefftz's approach).
    bp_z_st : float | None
        z-coordinate of the shear centre (Trefftz's approach).
    bp_gamma : float | None
        Warping constant.
    bp_a_sy : float | None
        Shear area for shear in the y-direction.
    bp_a_sz : float | None
        Shear area for shear in the z-direction.
    bp_a_syz : float | None
        Shear area about the yz-axes.
    bp_a_s11 : float | None
        Shear area about the 11-bending axis.
    bp_a_s22 : float | None
        Shear area about the 22-bending axis.
    bp_beta_y_plus : float | None
        Monosymmetry constant for bending about the y-axis with the top
        flange (positive z) in compression.
    bp_beta_y_minus : float | None
        Monosymmetry constant for bending about the y-axis with the bottom
        flange (negative z) in compression.
    bp_beta_z_plus : float | None
        Monosymmetry constant for bending about the z-axis with the flange
        at positive y in compression.
    bp_beta_z_minus : float | None
        Monosymmetry constant for bending about the z-axis with the flange
        at negative y in compression.
    bp_beta_11_plus : float | None
        Monosymmetry constant for bending about the 11-axis with the
        positive 22-side in compression.
    bp_beta_11_minus : float | None
        Monosymmetry constant for bending about the 11-axis with the
        negative 22-side in compression.
    bp_beta_22_plus : float | None
        Monosymmetry constant for bending about the 22-axis with the
        positive 11-side in compression.
    bp_beta_22_minus : float | None
        Monosymmetry constant for bending about the 22-axis with the
        negative 11-side in compression.
    bp_y_pc : float | None
        y-coordinate of the global plastic centroid.
    bp_z_pc : float | None
        z-coordinate of the global plastic centroid.
    bp_y11_pc : float | None
        11-coordinate of the principal plastic centroid.
    bp_z22_pc : float | None
        22-coordinate of the principal plastic centroid.
    bp_syy : float | None
        Plastic section modulus about the centroidal y-axis.
    bp_szz : float | None
        Plastic section modulus about the centroidal z-axis.
    bp_sf_yy_plus : float | None
        Shape factor for bending about the y-axis with respect to the top
        fibre (positive z).
    bp_sf_yy_minus : float | None
        Shape factor for bending about the y-axis with respect to the
        bottom fibre (negative z).
    bp_sf_zz_plus : float | None
        Shape factor for bending about the z-axis with respect to the
        fibre at positive y.
    bp_sf_zz_minus : float | None
        Shape factor for bending about the z-axis with respect to the
        fibre at negative y.
    bp_s11 : float | None
        Plastic section modulus about the 11-axis.
    bp_s22 : float | None
        Plastic section modulus about the 22-axis.
    bp_sf_11_plus : float | None
        Shape factor for bending about the 11-axis with respect to the
        positive 22-side.
    bp_sf_11_minus : float | None
        Shape factor for bending about the 11-axis with respect to the
        negative 22-side.
    bp_sf_22_plus : float | None
        Shape factor for bending about the 22-axis with respect to the
        positive 11-side.
    bp_sf_22_minus : float | None
        Shape factor for bending about the 22-axis with respect to the
        negative 11-side.
    """

    bp_area: float | None = None
    bp_perimeter: float | None = None
    bp_mass: float | None = None
    bp_ea: float | None = None
    bp_ga: float | None = None
    bp_nu_eff: float | None = None
    bp_e_eff: float | None = None
    bp_g_eff: float | None = None
    bp_qy: float | None = None
    bp_qz: float | None = None
    bp_iyy_g: float | None = None
    bp_izz_g: float | None = None
    bp_iyz_g: float | None = None
    bp_cy: float | None = None
    bp_cz: float | None = None
    bp_iyy_c: float | None = None
    bp_izz_c: float | None = None
    bp_iyz_c: float | None = None
    bp_zyy_plus: float | None = None
    bp_zyy_minus: float | None = None
    bp_zzz_plus: float | None = None
    bp_zzz_minus: float | None = None
    bp_ry_c: float | None = None
    bp_rz_c: float | None = None
    bp_i11_c: float | None = None
    bp_i22_c: float | None = None
    bp_phi: float | None = None
    bp_z11_plus: float | None = None
    bp_z11_minus: float | None = None
    bp_z22_plus: float | None = None
    bp_z22_minus: float | None = None
    bp_r11_c: float | None = None
    bp_r22_c: float | None = None
    bp_my_yy: float | None = None
    bp_my_zz: float | None = None
    bp_my_11: float | None = None
    bp_my_22: float | None = None
    bp_j: float | None = None
    bp_omega: npt.NDArray[np.float64] | None = None
    bp_psi_shear: npt.NDArray[np.float64] | None = None
    bp_phi_shear: npt.NDArray[np.float64] | None = None
    bp_delta_s: float | None = None
    bp_y_se: float | None = None
    bp_z_se: float | None = None
    bp_y11_se: float | None = None
    bp_z22_se: float | None = None
    bp_y_st: float | None = None
    bp_z_st: float | None = None
    bp_gamma: float | None = None
    bp_a_sy: float | None = None
    bp_a_sz: float | None = None
    bp_a_syz: float | None = None
    bp_a_s11: float | None = None
    bp_a_s22: float | None = None
    bp_beta_y_plus: float | None = None
    bp_beta_y_minus: float | None = None
    bp_beta_z_plus: float | None = None
    bp_beta_z_minus: float | None = None
    bp_beta_11_plus: float | None = None
    bp_beta_11_minus: float | None = None
    bp_beta_22_plus: float | None = None
    bp_beta_22_minus: float | None = None
    bp_y_pc: float | None = None
    bp_z_pc: float | None = None
    bp_y11_pc: float | None = None
    bp_z22_pc: float | None = None
    bp_syy: float | None = None
    bp_szz: float | None = None
    bp_sf_yy_plus: float | None = None
    bp_sf_yy_minus: float | None = None
    bp_sf_zz_plus: float | None = None
    bp_sf_zz_minus: float | None = None
    bp_s11: float | None = None
    bp_s22: float | None = None
    bp_sf_11_plus: float | None = None
    bp_sf_11_minus: float | None = None
    bp_sf_22_plus: float | None = None
    bp_sf_22_minus: float | None = None

    @property
    def area(self) -> float | None:
        """Cross-sectional area, same as ``bp_area``."""
        return self.bp_area

    @property
    def perimeter(self) -> float | None:
        """Cross-sectional perimeter, same as ``bp_perimeter``."""
        return self.bp_perimeter

    @property
    def mass(self) -> float | None:
        """Cross-sectional mass, same as ``bp_mass``."""
        return self.bp_mass

    @property
    def ea(self) -> float | None:
        """Modulus weighted area, same as ``bp_ea``."""
        return self.bp_ea

    @property
    def ga(self) -> float | None:
        """Modulus weighted product of shear modulus and area, same as ``bp_ga``."""
        return self.bp_ga

    @property
    def nu_eff(self) -> float | None:
        """Effective Poisson's ratio, same as ``bp_nu_eff``."""
        return self.bp_nu_eff

    @property
    def e_eff(self) -> float | None:
        """Effective elastic modulus, same as ``bp_e_eff``."""
        return self.bp_e_eff

    @property
    def g_eff(self) -> float | None:
        """Effective shear modulus, same as ``bp_g_eff``."""
        return self.bp_g_eff

    @property
    def j(self) -> float | None:
        """Torsion constant, same as ``bp_j``."""
        return self.bp_j

    @property
    def gamma(self) -> float | None:
        """Warping constant, same as ``bp_gamma``."""
        return self.bp_gamma

    @property
    def delta_s(self) -> float | None:
        """Shear factor, same as ``bp_delta_s``."""
        return self.bp_delta_s

    def asdict(self) -> dict[str, Any]:
        """Return the section properties as a dictionary, keyed by the ``bp_`` attribute names."""
        return asdict(self)

    @classmethod
    def from_sectionproperties(cls, props: SpSectionProperties) -> BPSectionProperties:
        """Create a ``BPSectionProperties`` from a raw ``sectionproperties`` result.

        The values are re-labelled and their signs adjusted so that the returned
        object is expressed in the Blueprints coordinate system.

        Parameters
        ----------
        props : SpSectionProperties
            Section properties as calculated by the ``sectionproperties`` library.

        Returns
        -------
        BPSectionProperties
            The same section properties, expressed in the Blueprints coordinate system.
        """
        # bp_y = -sp_x, bp_z = sp_y — see module docstring for the full mapping.
        # Axis-labelled scalars follow the axis rename (sp x/y ↔ bp y/z) with a
        # sign flip whenever an odd power of a horizontal coordinate is involved.
        # The plus/minus fibre labels flip for quantities keyed to the z-axis in
        # bp (because bp's positive y is sp's negative x), and for quantities
        # keyed to the principal 22-axis (because the bp view mirrors sp
        # horizontally, so 90° CCW from +11 in bp points opposite to sp).
        return cls(
            bp_area=props.area,
            bp_perimeter=props.perimeter,
            bp_mass=props.mass,
            bp_ea=props.ea,
            bp_ga=props.ga,
            bp_nu_eff=props.nu_eff,
            bp_e_eff=props.e_eff,
            bp_g_eff=props.g_eff,
            bp_qy=props.qx,
            bp_qz=_neg(props.qy),
            bp_iyy_g=props.ixx_g,
            bp_izz_g=props.iyy_g,
            bp_iyz_g=_neg(props.ixy_g),
            bp_cy=_neg(props.cx),
            bp_cz=props.cy,
            bp_iyy_c=props.ixx_c,
            bp_izz_c=props.iyy_c,
            bp_iyz_c=_neg(props.ixy_c),
            bp_zyy_plus=props.zxx_plus,
            bp_zyy_minus=props.zxx_minus,
            bp_zzz_plus=props.zyy_minus,
            bp_zzz_minus=props.zyy_plus,
            bp_ry_c=props.rx_c,
            bp_rz_c=props.ry_c,
            bp_i11_c=props.i11_c,
            bp_i22_c=props.i22_c,
            bp_phi=_neg(props.phi),
            bp_z11_plus=props.z11_minus,
            bp_z11_minus=props.z11_plus,
            bp_z22_plus=props.z22_plus,
            bp_z22_minus=props.z22_minus,
            bp_r11_c=props.r11_c,
            bp_r22_c=props.r22_c,
            bp_my_yy=props.my_xx,
            bp_my_zz=props.my_yy,
            bp_my_11=props.my_11,
            bp_my_22=props.my_22,
            bp_j=props.j,
            bp_omega=props.omega,
            bp_psi_shear=props.psi_shear,
            bp_phi_shear=props.phi_shear,
            bp_delta_s=props.delta_s,
            bp_y_se=_neg(props.x_se),
            bp_z_se=props.y_se,
            bp_y11_se=props.x11_se,
            bp_z22_se=_neg(props.y22_se),
            bp_y_st=_neg(props.x_st),
            bp_z_st=props.y_st,
            bp_gamma=props.gamma,
            bp_a_sy=props.a_sx,
            bp_a_sz=props.a_sy,
            bp_a_syz=_neg(props.a_sxy),
            bp_a_s11=props.a_s11,
            bp_a_s22=props.a_s22,
            bp_beta_y_plus=props.beta_x_plus,
            bp_beta_y_minus=props.beta_x_minus,
            bp_beta_z_plus=props.beta_y_minus,
            bp_beta_z_minus=props.beta_y_plus,
            bp_beta_11_plus=props.beta_11_minus,
            bp_beta_11_minus=props.beta_11_plus,
            bp_beta_22_plus=props.beta_22_plus,
            bp_beta_22_minus=props.beta_22_minus,
            bp_y_pc=_neg(props.x_pc),
            bp_z_pc=props.y_pc,
            bp_y11_pc=props.x11_pc,
            bp_z22_pc=_neg(props.y22_pc),
            bp_syy=props.sxx,
            bp_szz=props.syy,
            bp_sf_yy_plus=props.sf_xx_plus,
            bp_sf_yy_minus=props.sf_xx_minus,
            bp_sf_zz_plus=props.sf_yy_minus,
            bp_sf_zz_minus=props.sf_yy_plus,
            bp_s11=props.s11,
            bp_s22=props.s22,
            bp_sf_11_plus=props.sf_11_minus,
            bp_sf_11_minus=props.sf_11_plus,
            bp_sf_22_plus=props.sf_22_plus,
            bp_sf_22_minus=props.sf_22_minus,
        )

"""Section properties container using the Blueprints coordinate system.

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

This module wraps :class:`sectionproperties.post.post.SectionProperties` so that
all attribute names, sign conventions and ``plus``/``minus`` fibre labels are
expressed in the Blueprints frame as :class:`SectionProperties`.
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

    Attributes
    ----------
    area : float | None
        Cross-sectional area.
    perimeter : float | None
        Cross-sectional perimeter.
    mass : float | None
        Cross-sectional mass.
    ea : float | None
        Modulus weighted area (axial rigidity).
    ga : float | None
        Modulus weighted product of shear modulus and area.
    nu_eff : float | None
        Effective Poisson's ratio.
    e_eff : float | None
        Effective elastic modulus.
    g_eff : float | None
        Effective shear modulus.
    qy : float | None
        First moment of area about the y-axis (∫ z dA).
    qz : float | None
        First moment of area about the z-axis (∫ y dA).
    iyy_g : float | None
        Second moment of area about the global y-axis.
    izz_g : float | None
        Second moment of area about the global z-axis.
    iyz_g : float | None
        Product moment of area about the global yz-axes.
    cy : float | None
        y-coordinate of the elastic centroid.
    cz : float | None
        z-coordinate of the elastic centroid.
    iyy_c : float | None
        Second moment of area about the centroidal y-axis.
    izz_c : float | None
        Second moment of area about the centroidal z-axis.
    iyz_c : float | None
        Product moment of area about the centroidal yz-axes.
    zyy_plus : float | None
        Section modulus about the centroidal y-axis for stresses at the
        positive extreme of z (top fibre).
    zyy_minus : float | None
        Section modulus about the centroidal y-axis for stresses at the
        negative extreme of z (bottom fibre).
    zzz_plus : float | None
        Section modulus about the centroidal z-axis for stresses at the
        positive extreme of y.
    zzz_minus : float | None
        Section modulus about the centroidal z-axis for stresses at the
        negative extreme of y.
    ry_c : float | None
        Radius of gyration about the centroidal y-axis.
    rz_c : float | None
        Radius of gyration about the centroidal z-axis.
    i11_c : float | None
        Second moment of area about the centroidal 11-axis.
    i22_c : float | None
        Second moment of area about the centroidal 22-axis.
    phi : float | None
        Principal axis angle [rad], measured counter-clockwise from the
        positive y-axis to the positive 11-axis in the Blueprints frame.
    z11_plus : float | None
        Section modulus about the principal 11-axis for stresses at the
        positive extreme of the 22-axis.
    z11_minus : float | None
        Section modulus about the principal 11-axis for stresses at the
        negative extreme of the 22-axis.
    z22_plus : float | None
        Section modulus about the principal 22-axis for stresses at the
        positive extreme of the 11-axis.
    z22_minus : float | None
        Section modulus about the principal 22-axis for stresses at the
        negative extreme of the 11-axis.
    r11_c : float | None
        Radius of gyration about the principal 11-axis.
    r22_c : float | None
        Radius of gyration about the principal 22-axis.
    my_yy : float | None
        Yield moment about the y-axis.
    my_zz : float | None
        Yield moment about the z-axis.
    my_11 : float | None
        Yield moment about the 11-axis.
    my_22 : float | None
        Yield moment about the 22-axis.
    j : float | None
        Torsion constant.
    omega : npt.NDArray[np.float64] | None
        Warping function (per mesh node).
    psi_shear : npt.NDArray[np.float64] | None
        Psi shear function (per mesh node).
    phi_shear : npt.NDArray[np.float64] | None
        Phi shear function (per mesh node).
    delta_s : float | None
        Shear factor.
    y_se : float | None
        y-coordinate of the shear centre (elasticity approach).
    z_se : float | None
        z-coordinate of the shear centre (elasticity approach).
    y11_se : float | None
        11-coordinate of the shear centre (elasticity approach).
    z22_se : float | None
        22-coordinate of the shear centre (elasticity approach).
    y_st : float | None
        y-coordinate of the shear centre (Trefftz's approach).
    z_st : float | None
        z-coordinate of the shear centre (Trefftz's approach).
    gamma : float | None
        Warping constant.
    a_sy : float | None
        Shear area for shear in the y-direction.
    a_sz : float | None
        Shear area for shear in the z-direction.
    a_syz : float | None
        Shear area about the yz-axes.
    a_s11 : float | None
        Shear area about the 11-bending axis.
    a_s22 : float | None
        Shear area about the 22-bending axis.
    beta_y_plus : float | None
        Monosymmetry constant for bending about the y-axis with the top
        flange (positive z) in compression.
    beta_y_minus : float | None
        Monosymmetry constant for bending about the y-axis with the bottom
        flange (negative z) in compression.
    beta_z_plus : float | None
        Monosymmetry constant for bending about the z-axis with the flange
        at positive y in compression.
    beta_z_minus : float | None
        Monosymmetry constant for bending about the z-axis with the flange
        at negative y in compression.
    beta_11_plus : float | None
        Monosymmetry constant for bending about the 11-axis with the
        positive 22-side in compression.
    beta_11_minus : float | None
        Monosymmetry constant for bending about the 11-axis with the
        negative 22-side in compression.
    beta_22_plus : float | None
        Monosymmetry constant for bending about the 22-axis with the
        positive 11-side in compression.
    beta_22_minus : float | None
        Monosymmetry constant for bending about the 22-axis with the
        negative 11-side in compression.
    y_pc : float | None
        y-coordinate of the global plastic centroid.
    z_pc : float | None
        z-coordinate of the global plastic centroid.
    y11_pc : float | None
        11-coordinate of the principal plastic centroid.
    z22_pc : float | None
        22-coordinate of the principal plastic centroid.
    syy : float | None
        Plastic section modulus about the centroidal y-axis.
    szz : float | None
        Plastic section modulus about the centroidal z-axis.
    sf_yy_plus : float | None
        Shape factor for bending about the y-axis with respect to the top
        fibre (positive z).
    sf_yy_minus : float | None
        Shape factor for bending about the y-axis with respect to the
        bottom fibre (negative z).
    sf_zz_plus : float | None
        Shape factor for bending about the z-axis with respect to the
        fibre at positive y.
    sf_zz_minus : float | None
        Shape factor for bending about the z-axis with respect to the
        fibre at negative y.
    s11 : float | None
        Plastic section modulus about the 11-axis.
    s22 : float | None
        Plastic section modulus about the 22-axis.
    sf_11_plus : float | None
        Shape factor for bending about the 11-axis with respect to the
        positive 22-side.
    sf_11_minus : float | None
        Shape factor for bending about the 11-axis with respect to the
        negative 22-side.
    sf_22_plus : float | None
        Shape factor for bending about the 22-axis with respect to the
        positive 11-side.
    sf_22_minus : float | None
        Shape factor for bending about the 22-axis with respect to the
        negative 11-side.
    """

    area: float | None = None
    perimeter: float | None = None
    mass: float | None = None
    ea: float | None = None
    ga: float | None = None
    nu_eff: float | None = None
    e_eff: float | None = None
    g_eff: float | None = None
    qy: float | None = None
    qz: float | None = None
    iyy_g: float | None = None
    izz_g: float | None = None
    iyz_g: float | None = None
    cy: float | None = None
    cz: float | None = None
    iyy_c: float | None = None
    izz_c: float | None = None
    iyz_c: float | None = None
    zyy_plus: float | None = None
    zyy_minus: float | None = None
    zzz_plus: float | None = None
    zzz_minus: float | None = None
    ry_c: float | None = None
    rz_c: float | None = None
    i11_c: float | None = None
    i22_c: float | None = None
    phi: float | None = None
    z11_plus: float | None = None
    z11_minus: float | None = None
    z22_plus: float | None = None
    z22_minus: float | None = None
    r11_c: float | None = None
    r22_c: float | None = None
    my_yy: float | None = None
    my_zz: float | None = None
    my_11: float | None = None
    my_22: float | None = None
    j: float | None = None
    omega: npt.NDArray[np.float64] | None = None
    psi_shear: npt.NDArray[np.float64] | None = None
    phi_shear: npt.NDArray[np.float64] | None = None
    delta_s: float | None = None
    y_se: float | None = None
    z_se: float | None = None
    y11_se: float | None = None
    z22_se: float | None = None
    y_st: float | None = None
    z_st: float | None = None
    gamma: float | None = None
    a_sy: float | None = None
    a_sz: float | None = None
    a_syz: float | None = None
    a_s11: float | None = None
    a_s22: float | None = None
    beta_y_plus: float | None = None
    beta_y_minus: float | None = None
    beta_z_plus: float | None = None
    beta_z_minus: float | None = None
    beta_11_plus: float | None = None
    beta_11_minus: float | None = None
    beta_22_plus: float | None = None
    beta_22_minus: float | None = None
    y_pc: float | None = None
    z_pc: float | None = None
    y11_pc: float | None = None
    z22_pc: float | None = None
    syy: float | None = None
    szz: float | None = None
    sf_yy_plus: float | None = None
    sf_yy_minus: float | None = None
    sf_zz_plus: float | None = None
    sf_zz_minus: float | None = None
    s11: float | None = None
    s22: float | None = None
    sf_11_plus: float | None = None
    sf_11_minus: float | None = None
    sf_22_plus: float | None = None
    sf_22_minus: float | None = None

    def asdict(self) -> dict[str, Any]:
        """Return the section properties as a dictionary."""
        return asdict(self)

    @classmethod
    def from_sectionproperties(cls, props: SpSectionProperties) -> BPSectionProperties:
        """Create a Blueprints ``BPSectionProperties`` from a raw ``sectionproperties`` result.

        The values are re-labelled and their signs adjusted so that the returned
        object is expressed in the Blueprints coordinate system.

        Parameters
        ----------
        props : SpSectionProperties
            Section properties as calculated by the ``sectionproperties`` library.
        """
        # bp_y = -sp_x, bp_z = sp_y — see module docstring for the full mapping.
        # Axis-labelled scalars follow the axis rename (sp x/y ↔ bp y/z) with a
        # sign flip whenever an odd power of a horizontal coordinate is involved.
        # The plus/minus fibre labels flip for quantities keyed to the z-axis in
        # bp (because bp's positive y is sp's negative x), and for quantities
        # keyed to the principal 22-axis (because the bp view mirrors sp
        # horizontally, so 90° CCW from +11 in bp points opposite to sp).
        return cls(
            area=props.area,
            perimeter=props.perimeter,
            mass=props.mass,
            ea=props.ea,
            ga=props.ga,
            nu_eff=props.nu_eff,
            e_eff=props.e_eff,
            g_eff=props.g_eff,
            qy=props.qx,
            qz=_neg(props.qy),
            iyy_g=props.ixx_g,
            izz_g=props.iyy_g,
            iyz_g=_neg(props.ixy_g),
            cy=_neg(props.cx),
            cz=props.cy,
            iyy_c=props.ixx_c,
            izz_c=props.iyy_c,
            iyz_c=_neg(props.ixy_c),
            zyy_plus=props.zxx_plus,
            zyy_minus=props.zxx_minus,
            zzz_plus=props.zyy_minus,
            zzz_minus=props.zyy_plus,
            ry_c=props.rx_c,
            rz_c=props.ry_c,
            i11_c=props.i11_c,
            i22_c=props.i22_c,
            phi=_neg(props.phi),
            z11_plus=props.z11_minus,
            z11_minus=props.z11_plus,
            z22_plus=props.z22_plus,
            z22_minus=props.z22_minus,
            r11_c=props.r11_c,
            r22_c=props.r22_c,
            my_yy=props.my_xx,
            my_zz=props.my_yy,
            my_11=props.my_11,
            my_22=props.my_22,
            j=props.j,
            omega=props.omega,
            psi_shear=props.psi_shear,
            phi_shear=props.phi_shear,
            delta_s=props.delta_s,
            y_se=_neg(props.x_se),
            z_se=props.y_se,
            y11_se=props.x11_se,
            z22_se=_neg(props.y22_se),
            y_st=_neg(props.x_st),
            z_st=props.y_st,
            gamma=props.gamma,
            a_sy=props.a_sx,
            a_sz=props.a_sy,
            a_syz=_neg(props.a_sxy),
            a_s11=props.a_s11,
            a_s22=props.a_s22,
            beta_y_plus=props.beta_x_plus,
            beta_y_minus=props.beta_x_minus,
            beta_z_plus=props.beta_y_minus,
            beta_z_minus=props.beta_y_plus,
            beta_11_plus=props.beta_11_minus,
            beta_11_minus=props.beta_11_plus,
            beta_22_plus=props.beta_22_plus,
            beta_22_minus=props.beta_22_minus,
            y_pc=_neg(props.x_pc),
            z_pc=props.y_pc,
            y11_pc=props.x11_pc,
            z22_pc=_neg(props.y22_pc),
            syy=props.sxx,
            szz=props.syy,
            sf_yy_plus=props.sf_xx_plus,
            sf_yy_minus=props.sf_xx_minus,
            sf_zz_plus=props.sf_yy_minus,
            sf_zz_minus=props.sf_yy_plus,
            s11=props.s11,
            s22=props.s22,
            sf_11_plus=props.sf_11_minus,
            sf_11_minus=props.sf_11_plus,
            sf_22_plus=props.sf_22_plus,
            sf_22_minus=props.sf_22_minus,
        )

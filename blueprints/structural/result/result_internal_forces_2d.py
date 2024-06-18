from dataclasses import dataclass
from blueprints.type_alias import KN_M, KNM_M


@dataclass
class ResultInternalForces2D():
    """
    define properties..
    
    
    Attributes:
    ----------
    n_x : KN
        Axial force in the Y-direction. (negative is compression)
    n_y : KN
        Axial force in the Y-direction. (negative is compression)
    v_y : KN
        Shear force in the y-direction.
    v_z : KN
        Shear force in the z-direction.
    m_x : KNM
        Bending moment around the x-axis. 
        Positive is from Y to Z
    m_y : KNM
        Bending moment around the y-axis.
        Positive is from X to Z (compression in Z-positive)
    m_z : KNM
        Bending moment around the z-axis.
        Positive is from X to Y
    """
    n_x: KN_M = 0
    n_y: KN_M = 0
    n_xy: KN_M = 0
    v_xz: KN_M = 0
    v_yz: KN_M = 0
    m_xx: KNM_M  = 0
    m_yy: KNM_M = 0
    m_xy: KNM_M = 0
    m_yx: KNM_M = 0

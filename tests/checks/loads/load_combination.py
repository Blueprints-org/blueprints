"""Load combination used for a strength or stability checks."""

from dataclasses import dataclass

from blueprints.type_alias import KN, KNM


@dataclass(frozen=True)
class LoadCombination:
    """Load combination used for a strength or stability checks.

                z (vertical, usually strong axis)
                ↑
                |     x (longitudinal beam direction, into screen)
                |    ↗
                |   /
                |  /
                | /
                |/
      ←---------O
       y (horizontal/side, usually weak axis)

        Sign conventions:
        - Normal force N_x: positive = tension, negative = compression
        - Shear force V_y: positive = left (positive y-direction)
        - Shear force V_z: positive = up (positive z-direction)
        - Bending moment M_y: positive = from z to x (rotation around y-axis)
        - Bending moment M_z: positive = from x to y (rotation around z-axis)
        - Torsion M_x: positive = from y to z (twisting around x-axis)

    Attributes
    ----------
    normal_force : KN
        Normal force (positive = tension, negative = compression) [kN].
    shear_force_y : KN
        Shear force in y-axis (horizontal) [kN].
    shear_force_z : KN
        Shear force in z-axis (vertical) [kN].
    bending_moment_y : KNM
        Bending moment around y-axis [kNm].
    bending_moment_z : KNM
        Bending moment around z-axis [kNm].
    torsion : KNM
        Torsional moment [kNm].
    """

    normal_force: KN
    shear_force_y: KN
    shear_force_z: KN
    bending_moment_y: KNM
    bending_moment_z: KNM
    torsion: KNM

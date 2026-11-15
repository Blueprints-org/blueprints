"""How the class 3/4 shear check moves with the mesh.

`CheckStrengthShearClass34` divides the yield stress by the peak elastic shear
stress that the finite element model reports. That peak sits at the root radius,
where the elastic solution is singular, so it does not converge as the mesh is
refined - it keeps climbing. The capacity the check reports is therefore a
function of the mesh at any mesh size, and the value baked into the tests is a
snapshot of the flat 2.0 mm2 mesh rather than a converged answer.

This script prints the capacity as a function of the mesh so the size of that
dependence is visible.
"""

from __future__ import annotations

import argparse
from functools import partial

import _bootstrap  # noqa: F401  # isort: skip  - must run before blueprints imports

from mesh_calibration import min_thickness
from sectionproperties.pre import Geometry

from blueprints.checks.eurocode.steel.strength_shear import CheckStrengthShearClass34
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections._profile import Profile
from blueprints.structural_sections.steel.standard_profiles.heb import HEB
from blueprints.structural_sections.steel.standard_profiles.ipe import IPE
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection

FAMILIES = (HEB, IPE)


def mesh_rule(mesh_size: float):
    """A mesh rule that always returns the same mesh size."""
    return property(lambda self: partial(Geometry.create_mesh, mesh_sizes=mesh_size))


def thickness_rule(divisor: float):
    """A mesh rule based on the thinnest wall of the profile."""
    return property(lambda self: partial(Geometry.create_mesh, mesh_sizes=max(min_thickness(self) / divisor, 1.0) ** 2))


def capacity(profile_name: str, axis: str) -> float:
    """Shear capacity in kN from the class 3/4 check."""
    profiles = {p.name: p for family in FAMILIES for p in family}
    material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    section = SteelCrossSection(profile=profiles[profile_name], material=material)

    return CheckStrengthShearClass34(section, 1.0, axis=axis, gamma_m0=1.0).result().required / 1000


def main() -> None:
    """Print the class 3/4 shear capacity against the mesh rule."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profiles", nargs="*", default=["HEB300", "HEB1000", "IPE300"])
    args = parser.parse_args()

    rules = [
        ("flat 2.0 mm2 (old)", mesh_rule(2.0)),
        ("t/2", thickness_rule(2.0)),
        ("t/4", thickness_rule(4.0)),
        ("t/6", thickness_rule(6.0)),
        ("t/10", thickness_rule(10.0)),
        ("flat 0.5 mm2", mesh_rule(0.5)),
    ]

    for name in args.profiles:
        print(f"\n{name}")
        header = f"  {'mesh rule':<20}{'V_Rd,y [kN]':>14}{'vs old':>10}{'V_Rd,z [kN]':>14}{'vs old':>10}"
        print(header)
        print("  " + "-" * (len(header) - 2))

        reference = {}
        for label, rule in rules:
            Profile.mesh_creator = rule
            values = {axis: capacity(name, axis) for axis in ("Vy", "Vz")}

            if not reference:
                reference = values

            row = f"  {label:<20}"
            for axis in ("Vy", "Vz"):
                change = values[axis] / reference[axis] - 1
                row += f"{values[axis]:>14.1f}{change:>+9.2%} "
            print(row)


if __name__ == "__main__":
    main()

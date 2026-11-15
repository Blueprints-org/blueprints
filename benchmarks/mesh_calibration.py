"""Calibrates a wall-thickness based mesh rule for the steel profiles.

Blueprints meshes every steel profile at a flat ``mesh_sizes=2.0`` mm², which is a
mesh length of 1.41 mm regardless of the section. For an HEB1000, whose thinnest
wall is 19 mm, that is 13 elements across the web; for an IPE80, whose web is
3.8 mm, it is under 3. The mesh is therefore far finer than it needs to be on
large sections and coarser than the house rule on small ones.

The geometric profiles already use the house pattern
``mesh_length = max(t / n, floor)``. This script measures what divisor ``n`` buys
and costs for the steel profiles, against two references:

  * a very fine mesh (``t / 16``), which answers "how accurate is this?"
  * the current flat 2.0 mm² mesh, which answers "how far will my numbers move?"

Usage
-----
    python benchmarks/mesh_calibration.py
    python benchmarks/mesh_calibration.py --divisors 2 3 4 6
"""

from __future__ import annotations

import argparse
import time
from dataclasses import asdict

import _bootstrap  # noqa: F401  # isort: skip  - must run before blueprints imports

from sectionproperties.analysis import Section
from sectionproperties.pre import Geometry

from blueprints.structural_sections.steel.standard_profiles.chs import CHS
from blueprints.structural_sections.steel.standard_profiles.heb import HEB
from blueprints.structural_sections.steel.standard_profiles.ipe import IPE
from blueprints.structural_sections.steel.standard_profiles.lnp import LNP
from blueprints.structural_sections.steel.standard_profiles.rhs import RHS
from blueprints.structural_sections.steel.standard_profiles.unp import UNP

# properties an engineer actually reads off a section
REPORTED = (
    "area",
    "ixx_c",
    "iyy_c",
    "zxx_plus",
    "zyy_plus",
    "i11_c",
    "i22_c",
    "j",
    "gamma",
    "a_sx",
    "a_sy",
    "sxx",
    "syy",
)

REFERENCE_DIVISOR = 16.0
CURRENT_MESH_SIZE = 2.0

FAMILIES = (HEB, IPE, UNP, LNP, CHS, RHS)

SELECTION = [
    "HEB100",
    "HEB300",
    "HEB1000",
    "IPE80",
    "IPE300",
    "IPE600",
    "UNP80",
    "UNP300",
    "LNP 40x40x4",
    "LNP 100x100x10",
    "CHS 21.3x2.3",
    "CHS 273x10",
    "RHS50x30x2.6",
    "RHS200x100x10",
]


def min_thickness(profile) -> float:
    """Thinnest wall of the profile [mm], the dimension a wall-thickness mesh has to resolve."""
    walls = [value for key, value in vars(profile).items() if key.endswith("_thickness")]
    return min(walls, default=profile.max_thickness)


def main_mesh_size(profile) -> float:
    """Mesh size [mm²] of the rule ``Profile.mesh_creator`` ships, sized from the thickest wall."""
    return profile.max_thickness**2 / 32


def lookup() -> dict:
    """Map profile name onto profile for every family used here."""
    profiles = {}
    for family in FAMILIES:
        for profile in family:
            profiles[profile.name] = profile
    return profiles


def analyse(profile, mesh_size: float) -> tuple[dict[str, float], int, float]:
    """Run a full analysis at a given mesh size and return the properties."""
    start = time.perf_counter()

    geom = Geometry(geom=profile.polygon, tol=profile.accuracy)
    geom.create_mesh(mesh_sizes=mesh_size)
    section = Section(geometry=geom)
    section.calculate_geometric_properties()
    section.calculate_warping_properties()
    section.calculate_plastic_properties()

    elapsed = time.perf_counter() - start
    values = asdict(section.section_props)

    return (
        {name: float(values[name]) for name in REPORTED},
        len(section.mesh_elements),
        elapsed,
    )


# dimension of each reported property as a power of length
DIMENSION = {
    "area": 2,
    "ixx_c": 4,
    "iyy_c": 4,
    "zxx_plus": 3,
    "zyy_plus": 3,
    "i11_c": 4,
    "i22_c": 4,
    "j": 4,
    "gamma": 6,
    "a_sx": 2,
    "a_sy": 2,
    "sxx": 3,
    "syy": 3,
}

# a property this small relative to the section scale is numerically zero and its
# relative deviation says nothing. The warping constant of a closed circular tube
# is the case that matters here: it is zero in theory, so every run reports noise.
NEGLIGIBLE = 1e-9


def deviation(values: dict[str, float], reference: dict[str, float]) -> tuple[float, str]:
    """Largest relative deviation of a property set against a reference.

    Properties that are numerically zero for the section are skipped, since a
    relative comparison between two roundoff values is meaningless.
    """
    worst = 0.0
    worst_key = ""
    length = abs(reference["area"]) ** 0.5

    for key, ref in reference.items():
        if abs(ref) < NEGLIGIBLE * length ** DIMENSION[key]:
            continue
        rel = abs(values[key] - ref) / abs(ref)
        if rel > worst:
            worst, worst_key = rel, key

    return worst, worst_key


def main() -> None:
    """Sweep the divisor and report accuracy and time for every profile."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--divisors", nargs="*", type=float, default=[1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0])
    parser.add_argument("--profiles", nargs="*", default=SELECTION)
    args = parser.parse_args()

    profiles = lookup()

    header = f"  {'rule':>14}{'mesh len':>10}{'elements':>10}{'time':>9}{'dev vs fine':>14}{'dev vs 2mm2':>14}  worst"

    for name in args.profiles:
        profile = profiles[name]
        thickness = min_thickness(profile)

        fine, fine_elements, _ = analyse(profile, (thickness / REFERENCE_DIVISOR) ** 2)
        current, current_elements, current_time = analyse(profile, CURRENT_MESH_SIZE)
        current_dev, current_worst = deviation(current, fine)

        print(f"\n{name}  (min wall {thickness:g} mm, reference t/16 = {fine_elements} elements)")
        print(header)
        print("  " + "-" * (len(header) - 2))
        print(
            f"  {'flat 2.0 mm2':>14}{CURRENT_MESH_SIZE**0.5:>10.2f}{current_elements:>10}"
            f"{current_time:>9.3f}{current_dev:>14.2e}{0.0:>14.2e}  {current_worst}"
        )

        main_size = main_mesh_size(profile)
        values, elements, elapsed = analyse(profile, main_size)
        dev_fine, worst_fine = deviation(values, fine)
        dev_current, _ = deviation(values, current)
        print(f"  {'main tmax2/32':>14}{main_size**0.5:>10.2f}{elements:>10}{elapsed:>9.3f}{dev_fine:>14.2e}{dev_current:>14.2e}  {worst_fine}")

        for divisor in args.divisors:
            mesh_length = thickness / divisor
            values, elements, elapsed = analyse(profile, mesh_length**2)
            dev_fine, worst_fine = deviation(values, fine)
            dev_current, _ = deviation(values, current)

            print(
                f"  {'t/' + f'{divisor:g}':>14}{mesh_length:>10.2f}{elements:>10}{elapsed:>9.3f}{dev_fine:>14.2e}{dev_current:>14.2e}  {worst_fine}"
            )


if __name__ == "__main__":
    main()

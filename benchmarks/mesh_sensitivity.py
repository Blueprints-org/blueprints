"""Shows what the mesh density costs and what it buys.

Blueprints meshes every profile at ``mesh_sizes=2.0`` mm², which for an HEB1000
means about 32000 quadratic triangles. The finite element cost is roughly linear
in that number, so the mesh is by far the largest remaining lever on runtime once
the Python overhead has been removed.

This script does not change any default. It measures, for a few profiles, how the
section properties and the runtime move when the mesh is coarsened, so the
accuracy-for-speed trade can be judged on numbers rather than on feel.
"""

from __future__ import annotations

import argparse
import time
from dataclasses import asdict

import _bootstrap  # noqa: F401  # isort: skip  - must run before blueprints imports

from sectionproperties.analysis import Section
from sectionproperties.pre import Geometry

from blueprints.structural_sections.steel.standard_profiles.heb import HEB
from blueprints.structural_sections.steel.standard_profiles.ipe import IPE
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
    "y_se",
)

MESH_SIZES = (2.0, 4.0, 8.0, 16.0, 32.0, 64.0)


def analyse(profile, mesh_size: float) -> tuple[dict[str, float], int, float]:
    """Runs a full analysis at a given mesh size and returns the properties."""
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


def main() -> None:
    """Report property deviation and runtime against mesh size."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profiles", nargs="*", default=["HEB1000", "HEB300", "IPE300", "UNP200"])
    args = parser.parse_args()

    lookup = {}
    for family in (HEB, IPE, UNP):
        for profile in family:
            lookup[profile.name] = profile

    for name in args.profiles:
        profile = lookup[name]
        reference, ref_elements, ref_time = analyse(profile, MESH_SIZES[0])

        print(f"\n{name}  (reference mesh {MESH_SIZES[0]:g} mm², {ref_elements} elements, {ref_time:.3f} s)")
        header = f"  {'mesh':>6}{'elements':>10}{'time':>9}{'speedup':>9}{'max deviation':>16}  worst property"
        print(header)
        print("  " + "-" * (len(header) - 2))

        for mesh_size in MESH_SIZES:
            values, n_elements, elapsed = analyse(profile, mesh_size)

            deviations = {
                key: abs(values[key] - reference[key]) / abs(reference[key])
                for key in REPORTED
                if abs(reference[key]) > 1e-9 * abs(reference["ixx_c"]) ** 0.5
            }
            worst_key = max(deviations, key=lambda k: deviations[k])
            worst = deviations[worst_key]

            print(f"  {mesh_size:>6.0f}{n_elements:>10}{elapsed:>9.3f}{ref_time / elapsed:>8.1f}x{worst:>16.2e}  {worst_key}")


if __name__ == "__main__":
    main()

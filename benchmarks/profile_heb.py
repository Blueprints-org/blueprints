"""Per-stage timing probe for the HEB section-property workload.

Reproduces the ``need_for_speed.py`` scratch workload and splits the wall time
over the four stages so it is clear where the time actually goes:

    mesh   -> Geometry + Section construction (cytriangle + Python element setup)
    geom   -> Section.calculate_geometric_properties
    warp   -> Section.calculate_warping_properties
    plas   -> Section.calculate_plastic_properties

Usage
-----
    python benchmarks/profile_heb.py            # all HEB profiles
    python benchmarks/profile_heb.py --limit 5  # first 5 profiles only
"""

from __future__ import annotations

import argparse
import time

import _bootstrap  # noqa: F401  # isort: skip  - must run before blueprints imports

from blueprints.structural_sections.steel.standard_profiles.heb import HEB


def main() -> None:
    """Run the probe and print a per-profile timing table."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=0, help="only run the first N profiles")
    args = parser.parse_args()

    profiles = list(HEB)
    if args.limit:
        profiles = profiles[: args.limit]

    # warm up: the first analysis in a process pays for imports and, when numba is
    # installed, for JIT compilation. Timing that would flatter the branch that
    # spends less time in the compiled paths.
    warmup = profiles[0]
    warmup_section = warmup._section()
    warmup_section.calculate_geometric_properties()
    warmup_section.calculate_warping_properties()
    warmup_section.calculate_plastic_properties()

    rows = []
    wall_start = time.perf_counter()

    for profile in profiles:
        t0 = time.perf_counter()
        section = profile._section()
        t_mesh = time.perf_counter() - t0

        t0 = time.perf_counter()
        section.calculate_geometric_properties()
        t_geom = time.perf_counter() - t0

        t0 = time.perf_counter()
        section.calculate_warping_properties()
        t_warp = time.perf_counter() - t0

        t0 = time.perf_counter()
        section.calculate_plastic_properties()
        t_plas = time.perf_counter() - t0

        n_el = len(section.mesh_elements)
        rows.append((profile.name, n_el, section.num_nodes, t_mesh, t_geom, t_warp, t_plas))

    wall_total = time.perf_counter() - wall_start

    header = f"{'profile':<14}{'n_el':>8}{'n_nd':>8}{'mesh_s':>10}{'geom_s':>10}{'warp_s':>10}{'plas_s':>10}"
    print(header)
    print("-" * len(header))
    for name, n_el, n_nd, t_mesh, t_geom, t_warp, t_plas in rows:
        print(f"{name:<14}{n_el:>8}{n_nd:>8}{t_mesh:>10.3f}{t_geom:>10.3f}{t_warp:>10.3f}{t_plas:>10.3f}")
    print("-" * len(header))
    print(
        f"{'TOTAL':<14}{sum(r[1] for r in rows):>8}{sum(r[2] for r in rows):>8}"
        f"{sum(r[3] for r in rows):>10.3f}{sum(r[4] for r in rows):>10.3f}"
        f"{sum(r[5] for r in rows):>10.3f}{sum(r[6] for r in rows):>10.3f}"
    )
    print(f"\nwall total: {wall_total:.3f} s over {len(rows)} profiles")


if __name__ == "__main__":
    main()

"""Splits the warping analysis into assembly, linear solve and post-integration.

Wraps the solver entry points so the time spent factorising and solving the
sparse system can be separated from the rest of the warping analysis.
"""

from __future__ import annotations

import argparse
import time

import _bootstrap  # noqa: F401  # isort: skip  - must run before blueprints imports

from sectionproperties.analysis import solver

from blueprints.structural_sections.steel.standard_profiles.heb import HEB

SOLVE_TIME = 0.0


def _instrument() -> None:
    """Wraps the direct solvers so their wall time is accumulated."""
    original_multi = solver.solve_warping_direct
    original_single = solver.solve_direct_lagrange

    def timed_multi(*args, **kwargs):
        global SOLVE_TIME
        start = time.perf_counter()
        result = original_multi(*args, **kwargs)
        SOLVE_TIME += time.perf_counter() - start
        return result

    def timed_single(*args, **kwargs):
        global SOLVE_TIME
        start = time.perf_counter()
        result = original_single(*args, **kwargs)
        SOLVE_TIME += time.perf_counter() - start
        return result

    solver.solve_warping_direct = timed_multi
    solver.solve_direct_lagrange = timed_single


def main() -> None:
    """Time the whole HEB sweep and report how much of it is the linear solve."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-pardiso", action="store_true", help="force the scipy SuperLU path")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    if args.no_pardiso:
        solver._HAS_PARDISO = False
        print("pardiso disabled, using scipy SuperLU\n")
    else:
        print(f"pardiso available: {solver._HAS_PARDISO}\n")

    _instrument()

    profiles = list(HEB)
    if args.limit:
        profiles = profiles[: args.limit]

    t_mesh = t_geom = t_warp = t_plas = 0.0
    start = time.perf_counter()

    for profile in profiles:
        t0 = time.perf_counter()
        section = profile._section()
        t_mesh += time.perf_counter() - t0

        t0 = time.perf_counter()
        section.calculate_geometric_properties()
        t_geom += time.perf_counter() - t0

        t0 = time.perf_counter()
        section.calculate_warping_properties()
        t_warp += time.perf_counter() - t0

        t0 = time.perf_counter()
        section.calculate_plastic_properties()
        t_plas += time.perf_counter() - t0

    total = time.perf_counter() - start

    print(f"{'mesh + Section':<24}{t_mesh:>8.3f} s")
    print(f"{'geometric':<24}{t_geom:>8.3f} s")
    print(f"{'warping':<24}{t_warp:>8.3f} s")
    print(f"{'  of which linear solve':<24}{SOLVE_TIME:>8.3f} s")
    print(f"{'  of which the rest':<24}{t_warp - SOLVE_TIME:>8.3f} s")
    print(f"{'plastic':<24}{t_plas:>8.3f} s")
    print(f"{'TOTAL':<24}{total:>8.3f} s  over {len(profiles)} profiles")


if __name__ == "__main__":
    main()

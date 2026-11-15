"""Back-to-back timing of the HEB sweep under each mesh rule.

This machine throttles: the same sweep has been observed to take anywhere from
10 s to 28 s depending on what the clock is doing at the time, so absolute
timings taken minutes apart cannot be compared. Two things are done about that.

Within a run, the mesh rules are measured alternately in one process, so their
ratio is sound.

Across runs - which is unavoidable, since the two sectionproperties versions
cannot be imported into one process - every timing is divided by a fixed
calibration workload measured in the same process. The normalised numbers are in
units of "reference workloads" rather than seconds, which cancels the clock
speed out.

Run this once on each sectionproperties checkout:

    git -C ../section-properties checkout master
    python benchmarks/headline.py --label "v3.10.2"

    git -C ../section-properties checkout feature/vectorised-analysis
    python benchmarks/headline.py --label "branch"
"""

from __future__ import annotations

import argparse
import statistics
import time
from functools import partial

import numpy as np

import _bootstrap  # noqa: F401  # isort: skip  - must run before blueprints imports

from mesh_calibration import min_thickness
from sectionproperties.pre import Geometry

from blueprints.structural_sections._profile import Profile
from blueprints.structural_sections.steel.standard_profiles.heb import HEB

MAIN_RULE = Profile.mesh_creator
FLAT_RULE = property(lambda self: partial(Geometry.create_mesh, mesh_sizes=2.0))
THICKNESS_RULE = property(lambda self: partial(Geometry.create_mesh, mesh_sizes=max(min_thickness(self) / 4, 1.0) ** 2))

RULES = {"flat 2.0 mm2": FLAT_RULE, "t/4 thickness": THICKNESS_RULE, "max t^2/32": MAIN_RULE}


def calibration() -> float:
    """Time a fixed numerical workload, used to normalise out the CPU clock speed.

    Returns
    -------
        Seconds taken by the reference workload
    """
    rng = np.random.default_rng(0)
    a = rng.random((400, 400))
    b = rng.random((400, 400))

    start = time.perf_counter()
    for _ in range(40):
        a @ b
    return time.perf_counter() - start


def sweep() -> tuple[list[float], int]:
    """Run the full HEB sweep and return the per-stage times and element count."""
    stages = [0.0, 0.0, 0.0, 0.0]
    elements = 0

    for profile in HEB:
        start = time.perf_counter()
        section = profile._section()
        stages[0] += time.perf_counter() - start

        start = time.perf_counter()
        section.calculate_geometric_properties()
        stages[1] += time.perf_counter() - start

        start = time.perf_counter()
        section.calculate_warping_properties()
        stages[2] += time.perf_counter() - start

        start = time.perf_counter()
        section.calculate_plastic_properties()
        stages[3] += time.perf_counter() - start

        elements += len(section.mesh_elements)

    return stages, elements


def main() -> None:
    """Alternate between the mesh rules and report the best of each."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--label", default="current")
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--rules", nargs="*", default=list(RULES), help="mesh rules to time")
    args = parser.parse_args()

    # warm up imports and any lazily built caches
    Profile.mesh_creator = MAIN_RULE
    sweep()
    calibration()

    reference = min(calibration() for _ in range(3))

    selected = {name: RULES[name] for name in args.rules}
    results: dict[str, list[list[float]]] = {name: [] for name in selected}
    elements: dict[str, int] = {}

    for _ in range(args.repeats):
        for name, rule in selected.items():
            Profile.mesh_creator = rule
            stages, count = sweep()
            results[name].append(stages)
            elements[name] = count

    print(f"\n{args.label}: 24 HEB profiles, geometric + warping + plastic")
    header = f"{'mesh rule':<16}{'elements':>10}{'mesh':>9}{'geom':>9}{'warp':>9}{'plastic':>9}{'total':>9}{'normalised':>12}"
    print(header)
    print("-" * len(header))

    totals = {}
    for name, runs in results.items():
        best = min(runs, key=sum)
        totals[name] = sum(best)
        print(f"{name:<16}{elements[name]:>10}" + "".join(f"{value:>9.2f}" for value in best) + f"{sum(best):>9.2f}{sum(best) / reference:>12.1f}")
        spread = [sum(run) for run in runs]
        print(f"{'':<16}{'runs:':>10}  " + "  ".join(f"{value:.2f}" for value in spread) + f"   median {statistics.median(spread):.2f}")

    if "flat 2.0 mm2" in totals:
        flat = totals["flat 2.0 mm2"]
        for name, total in totals.items():
            if name != "flat 2.0 mm2":
                print(f"mesh rule alone, {name}: {flat / total:.2f}x  ({flat:.2f} s -> {total:.2f} s)")


if __name__ == "__main__":
    main()

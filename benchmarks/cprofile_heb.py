"""cProfile a single HEB profile to locate the hot spots inside sectionproperties.

Usage
-----
    python benchmarks/cprofile_heb.py HEB300 --stage warping
"""

from __future__ import annotations

import argparse
import cProfile
import pstats
import time

import _bootstrap  # noqa: F401  # isort: skip  - must run before blueprints imports

from blueprints.structural_sections.steel.standard_profiles.heb import HEB


def main() -> None:
    """Profile one stage of the section-property calculation for a single profile."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", nargs="?", default="HEB300")
    parser.add_argument("--stage", default="warping", choices=["mesh", "geometric", "warping", "plastic", "all"])
    parser.add_argument("--rows", type=int, default=35)
    args = parser.parse_args()

    profile = getattr(HEB, args.profile)

    t0 = time.perf_counter()
    section = profile._section()
    t_mesh = time.perf_counter() - t0
    print(f"{args.profile}: {len(section.elements)} elements, {section.num_nodes} nodes (mesh build {t_mesh:.3f} s)")

    if args.stage in ("geometric", "warping", "plastic", "all"):
        if args.stage == "geometric":
            target = section.calculate_geometric_properties
        else:
            section.calculate_geometric_properties()
            target = {
                "warping": section.calculate_warping_properties,
                "plastic": section.calculate_plastic_properties,
                "all": section.calculate_warping_properties,
            }[args.stage]
    else:
        target = profile._section

    profiler = cProfile.Profile()
    profiler.enable()
    target()
    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats("tottime").print_stats(args.rows)


if __name__ == "__main__":
    main()

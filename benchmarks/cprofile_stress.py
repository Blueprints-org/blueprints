"""cProfile the stress analysis of a single profile."""

from __future__ import annotations

import argparse
import cProfile
import pstats

import _bootstrap  # noqa: F401  # isort: skip  - must run before blueprints imports

from blueprints.structural_sections.steel.standard_profiles.heb import HEB


def main() -> None:
    """Profile Section.calculate_stress for one profile."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", nargs="?", default="HEB600")
    parser.add_argument("--rows", type=int, default=25)
    args = parser.parse_args()

    profile = getattr(HEB, args.profile)
    section = profile._analysed_section(geometric=True, plastic=True, warping=True)
    print(f"{args.profile}: {section.num_elements} elements, {section.num_nodes} nodes")

    profiler = cProfile.Profile()
    profiler.enable()
    section.calculate_stress(n=1, vx=1, vy=1, mxx=1, myy=1, mzz=1)
    profiler.disable()

    pstats.Stats(profiler).sort_stats("tottime").print_stats(args.rows)


if __name__ == "__main__":
    main()

"""cProfile the whole HEB sweep to find what is left to optimise."""

from __future__ import annotations

import argparse
import cProfile
import pstats

import _bootstrap  # noqa: F401  # isort: skip  - must run before blueprints imports

from blueprints.structural_sections.steel.standard_profiles.heb import HEB


def sweep(limit: int) -> None:
    """Run the full section-property calculation for every HEB profile."""
    profiles = list(HEB)
    if limit:
        profiles = profiles[:limit]

    for profile in profiles:
        profile.section_properties(geometric=True, plastic=True, warping=True)


def main() -> None:
    """Profile the sweep and print the hottest functions."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--rows", type=int, default=30)
    args = parser.parse_args()

    # warm up imports and any lazily built caches
    sweep(limit=1)

    profiler = cProfile.Profile()
    profiler.enable()
    sweep(limit=args.limit)
    profiler.disable()

    pstats.Stats(profiler).sort_stats("tottime").print_stats(args.rows)


if __name__ == "__main__":
    main()

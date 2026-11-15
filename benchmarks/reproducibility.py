"""Checks how reproducible the torsion constant is between identical runs."""

from __future__ import annotations

import argparse

import _bootstrap  # noqa: F401  # isort: skip  - must run before blueprints imports

from blueprints.structural_sections.steel.standard_profiles.heb import HEB


def main() -> None:
    """Print the torsion constant of a profile with full precision."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", nargs="?", default="HEB180")
    parser.add_argument("--repeat", type=int, default=2, help="analyses within this process")
    args = parser.parse_args()

    for _ in range(args.repeat):
        profile = getattr(HEB, args.profile)
        section = profile._section()
        section.calculate_geometric_properties()
        section.calculate_warping_properties()
        print(f"{args.profile}  j = {section.get_j()!r}")


if __name__ == "__main__":
    main()

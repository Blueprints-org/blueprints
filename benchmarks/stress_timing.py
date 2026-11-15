"""Times the stress analysis path that the Blueprints shear check depends on."""

from __future__ import annotations

import argparse
import time

import _bootstrap  # noqa: F401  # isort: skip  - must run before blueprints imports

from blueprints.structural_sections.steel.standard_profiles.heb import HEB


def main() -> None:
    """Time the analysis and the stress evaluation separately."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profiles", nargs="*", default=["HEB300", "HEB600", "HEB1000"])
    args = parser.parse_args()

    header = f"{'profile':<10}{'elements':>10}{'analysis':>11}{'calculate_stress':>18}"
    print(header)
    print("-" * len(header))

    for name in args.profiles:
        profile = getattr(HEB, name)

        start = time.perf_counter()
        section = profile._analysed_section(geometric=True, plastic=True, warping=True)
        t_analysis = time.perf_counter() - start

        start = time.perf_counter()
        section.calculate_stress(n=1, vx=1, vy=1, mxx=1, myy=1, mzz=1)
        t_stress = time.perf_counter() - start

        n_elements = len(section.mesh_elements)
        print(f"{name:<10}{n_elements:>10}{t_analysis:>11.3f}{t_stress:>18.3f}")


if __name__ == "__main__":
    main()

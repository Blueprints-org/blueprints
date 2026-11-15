"""Fine-grained breakdown of where the time goes for a single HEB profile."""

from __future__ import annotations

import argparse
import time

import _bootstrap  # noqa: F401  # isort: skip  - must run before blueprints imports

from sectionproperties.analysis import Section
from sectionproperties.pre import Geometry

from blueprints.structural_sections.steel.standard_profiles.heb import HEB


def main() -> None:
    """Time polygon build, meshing, Section construction and each analysis stage."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", nargs="?", default="HEB300")
    args = parser.parse_args()

    profile = getattr(HEB, args.profile)

    t0 = time.perf_counter()
    polygon = profile.polygon
    t_poly = time.perf_counter() - t0

    t0 = time.perf_counter()
    geom = Geometry(geom=polygon, tol=profile.accuracy)
    t_geom_obj = time.perf_counter() - t0

    t0 = time.perf_counter()
    geom = profile.mesh_creator(geom)
    t_mesh = time.perf_counter() - t0

    t0 = time.perf_counter()
    section = Section(geometry=geom)
    t_section = time.perf_counter() - t0

    t0 = time.perf_counter()
    section.calculate_geometric_properties()
    t_geometric = time.perf_counter() - t0

    t0 = time.perf_counter()
    section.calculate_warping_properties()
    t_warping = time.perf_counter() - t0

    t0 = time.perf_counter()
    section.calculate_plastic_properties()
    t_plastic = time.perf_counter() - t0

    total = t_poly + t_geom_obj + t_mesh + t_section + t_geometric + t_warping + t_plastic

    print(f"{args.profile}: {len(section.elements)} elements, {section.num_nodes} nodes")
    for label, value in [
        ("shapely polygon", t_poly),
        ("Geometry()", t_geom_obj),
        ("create_mesh (cytriangle)", t_mesh),
        ("Section()", t_section),
        ("geometric", t_geometric),
        ("warping", t_warping),
        ("plastic", t_plastic),
    ]:
        print(f"  {label:<26}{value:>8.3f} s  ({value / total * 100:>5.1f} %)")
    print(f"  {'TOTAL':<26}{total:>8.3f} s")


if __name__ == "__main__":
    main()

"""Mesh calibration for the peak stresses the Eurocode shear check reads.

`StrengthShear` takes `max(abs(sig_zxy_vy))` from `Profile.unit_stress()`. A peak
nodal stress converges more slowly than an integral property such as `ixx` or
`j`, so the mesh rule has to be judged against it separately.

Usage
-----
    python benchmarks/mesh_calibration_stress.py
"""

from __future__ import annotations

import argparse
import time

import numpy as np

import _bootstrap  # noqa: F401  # isort: skip  - must run before blueprints imports

from mesh_calibration import main_mesh_size, min_thickness
from sectionproperties.analysis import Section
from sectionproperties.pre import Geometry

from blueprints.structural_sections.steel.standard_profiles.chs import CHS
from blueprints.structural_sections.steel.standard_profiles.heb import HEB
from blueprints.structural_sections.steel.standard_profiles.ipe import IPE
from blueprints.structural_sections.steel.standard_profiles.lnp import LNP
from blueprints.structural_sections.steel.standard_profiles.rhs import RHS
from blueprints.structural_sections.steel.standard_profiles.unp import UNP
from blueprints.unit_conversion import KN_TO_N, KNM_TO_NMM

REFERENCE_DIVISOR = 16.0
CURRENT_MESH_SIZE = 2.0

FAMILIES = (HEB, IPE, UNP, LNP, CHS, RHS)

SELECTION = [
    "HEB100",
    "HEB300",
    "HEB1000",
    "IPE80",
    "IPE300",
    "IPE600",
    "UNP80",
    "UNP300",
    "LNP 100x100x10",
    "CHS 273x10",
    "RHS200x100x10",
]

# the unit actions Profile.unit_stress() applies, in sectionproperties' convention
UNIT_ACTIONS = {
    "n": 1.0 * KN_TO_N,
    "vx": -1.0 * KN_TO_N,
    "vy": 1.0 * KN_TO_N,
    "mxx": -1.0 * KNM_TO_NMM,
    "myy": 1.0 * KNM_TO_NMM,
    "mzz": 1.0 * KNM_TO_NMM,
}

PEAKS = ("sig_zxy_vx", "sig_zxy_vy", "sig_zxy_mzz", "sig_zz", "sig_vm")


def lookup() -> dict:
    """Map profile name onto profile for every family used here."""
    profiles = {}
    for family in FAMILIES:
        for profile in family:
            profiles[profile.name] = profile
    return profiles


def peak_stresses(profile, mesh_size: float) -> tuple[dict[str, float], int, float]:
    """Return the peak of each stress component under the unit actions."""
    start = time.perf_counter()

    geom = Geometry(geom=profile.polygon, tol=profile.accuracy)
    geom.create_mesh(mesh_sizes=mesh_size)
    section = Section(geometry=geom)
    section.calculate_geometric_properties()
    section.calculate_warping_properties()
    section.calculate_plastic_properties()
    stress = section.calculate_stress(**UNIT_ACTIONS).get_stress()[0]

    elapsed = time.perf_counter() - start

    peaks = {name: float(np.max(np.abs(stress[name]))) for name in PEAKS}

    return peaks, len(section.mesh_elements), elapsed


def deviation(values: dict[str, float], reference: dict[str, float]) -> tuple[float, str]:
    """Largest relative deviation of a peak set against a reference."""
    worst = 0.0
    worst_key = ""

    for key, ref in reference.items():
        if abs(ref) < 1e-15:
            continue
        rel = abs(values[key] - ref) / abs(ref)
        if rel > worst:
            worst, worst_key = rel, key

    return worst, worst_key


def main() -> None:
    """Sweep the divisor and report peak-stress accuracy for every profile."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--divisors", nargs="*", type=float, default=[2.0, 3.0, 4.0, 6.0])
    parser.add_argument("--profiles", nargs="*", default=SELECTION)
    args = parser.parse_args()

    profiles = lookup()

    header = f"  {'rule':>14}{'elements':>10}{'time':>9}{'dev vs fine':>14}{'dev vs 2mm2':>14}  worst"

    for name in args.profiles:
        profile = profiles[name]
        thickness = min_thickness(profile)

        fine, fine_elements, _ = peak_stresses(profile, (thickness / REFERENCE_DIVISOR) ** 2)
        current, current_elements, current_time = peak_stresses(profile, CURRENT_MESH_SIZE)
        current_dev, current_worst = deviation(current, fine)

        print(f"\n{name}  (min wall {thickness:g} mm, reference t/16 = {fine_elements} elements)")
        print(header)
        print("  " + "-" * (len(header) - 2))
        print(f"  {'flat 2.0 mm2':>14}{current_elements:>10}{current_time:>9.3f}{current_dev:>14.2e}{0.0:>14.2e}  {current_worst}")

        values, elements, elapsed = peak_stresses(profile, main_mesh_size(profile))
        dev_fine, worst_fine = deviation(values, fine)
        dev_current, _ = deviation(values, current)
        print(f"  {'main tmax2/32':>14}{elements:>10}{elapsed:>9.3f}{dev_fine:>14.2e}{dev_current:>14.2e}  {worst_fine}")

        for divisor in args.divisors:
            values, elements, elapsed = peak_stresses(profile, (thickness / divisor) ** 2)
            dev_fine, worst_fine = deviation(values, fine)
            dev_current, _ = deviation(values, current)

            print(f"  {'t/' + f'{divisor:g}':>14}{elements:>10}{elapsed:>9.3f}{dev_fine:>14.2e}{dev_current:>14.2e}  {worst_fine}")


if __name__ == "__main__":
    main()

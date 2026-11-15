"""Numerical reference harness for the sectionproperties speed-up work.

Computes every section property Blueprints exposes for a range of standard
profiles and writes them to JSON.  A later run can be compared against that
reference to prove the optimised sectionproperties still produces the same
numbers.

Usage
-----
    python benchmarks/verify_properties.py --output benchmarks/results/reference.json
    python benchmarks/verify_properties.py --compare benchmarks/results/reference.json

Why the comparison is not a plain relative check
------------------------------------------------
Several section properties are sums of large contributions that cancel almost
completely.  For a doubly symmetric profile ``ixy`` and ``kappa_xy`` are exactly
zero in theory, so what a finite element run reports for them is rounding noise:
``1e-10`` in one run and ``5e-9`` in another are both "zero", even though they
differ by 100% in relative terms.  Comparing those against each other says
nothing about accuracy.

So every property is compared against a tolerance built from the profile's own
characteristic length ``L = sqrt(area)`` raised to the property's dimension.  A
difference only counts when it is large relative to the scale the property lives
on, which is what "the answers did not change" actually means.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np

import _bootstrap  # noqa: F401  # isort: skip  - must run before blueprints imports

from blueprints.structural_sections.steel.standard_profiles.chs import CHS
from blueprints.structural_sections.steel.standard_profiles.hea import HEA
from blueprints.structural_sections.steel.standard_profiles.heb import HEB
from blueprints.structural_sections.steel.standard_profiles.ipe import IPE
from blueprints.structural_sections.steel.standard_profiles.lnp import LNP
from blueprints.structural_sections.steel.standard_profiles.rhs import RHS
from blueprints.structural_sections.steel.standard_profiles.unp import UNP

FAMILIES = {"HEA": HEA, "HEB": HEB, "IPE": IPE, "CHS": CHS, "RHS": RHS, "UNP": UNP, "LNP": LNP}

ARRAY_FIELDS = ("omega", "psi_shear", "phi_shear")

# dimension of each property as a power of length, used to scale its tolerance
DIMENSION: dict[str, int] = {
    # dimensionless
    "nu_eff": 0,
    "e_eff": 0,
    "g_eff": 0,
    "sf_xx_plus": 0,
    "sf_xx_minus": 0,
    "sf_yy_plus": 0,
    "sf_yy_minus": 0,
    "sf_11_plus": 0,
    "sf_11_minus": 0,
    "sf_22_plus": 0,
    "sf_22_minus": 0,
    # lengths
    "perimeter": 1,
    "cx": 1,
    "cy": 1,
    "rx_c": 1,
    "ry_c": 1,
    "r11_c": 1,
    "r22_c": 1,
    "x_se": 1,
    "y_se": 1,
    "x11_se": 1,
    "y22_se": 1,
    "x_st": 1,
    "y_st": 1,
    "x_pc": 1,
    "y_pc": 1,
    "x11_pc": 1,
    "y22_pc": 1,
    "beta_x_plus": 1,
    "beta_x_minus": 1,
    "beta_y_plus": 1,
    "beta_y_minus": 1,
    "beta_11_plus": 1,
    "beta_11_minus": 1,
    "beta_22_plus": 1,
    "beta_22_minus": 1,
    # areas
    "area": 2,
    "mass": 2,
    "ea": 2,
    "ga": 2,
    "a_sx": 2,
    "a_sy": 2,
    "a_s11": 2,
    "a_s22": 2,
    # first moments / section moduli
    "qx": 3,
    "qy": 3,
    "zxx_plus": 3,
    "zxx_minus": 3,
    "zyy_plus": 3,
    "zyy_minus": 3,
    "z11_plus": 3,
    "z11_minus": 3,
    "z22_plus": 3,
    "z22_minus": 3,
    "sxx": 3,
    "syy": 3,
    "s11": 3,
    "s22": 3,
    "my_xx": 3,
    "my_yy": 3,
    "my_11": 3,
    "my_22": 3,
    # second moments of area
    "ixx_g": 4,
    "iyy_g": 4,
    "ixy_g": 4,
    "ixx_c": 4,
    "iyy_c": 4,
    "ixy_c": 4,
    "i11_c": 4,
    "i22_c": 4,
    "j": 4,
    # warping constant and shear factor
    "gamma": 6,
    "delta_s": 8,
    # a_sxy is the reciprocal of a quantity that vanishes for symmetric sections,
    # so it is compared as 1 / a_sxy
    "inv_a_sxy": -2,
}

# tolerance floor as a fraction of the characteristic scale of a property
FLOOR = 1e-11

# A property smaller than this fraction of its own natural scale is zero as far as the
# section is concerned - a shear centre offset of 1e-5 x sqrt(area) is under a micrometre
# on an HEB300 - so a relative comparison against it carries no information.
NEGLIGIBLE = 1e-5

# principal axis angle is compared in degrees
PHI_ATOL_DEG = 1e-6

# When i11 equals i22 every axis is a principal axis, so the principal axis angle
# and everything positioned along it is undetermined: what a run reports for them
# is decided purely by rounding.  A circular hollow section is the obvious case.
#
# The threshold follows from how phi is computed.  Its uncertainty is roughly
# d(ixy) / (i11 - i22), where d(ixy) is the rounding noise on ixy.  For a doubly
# symmetric profile ixy is a sum of large contributions that cancel, leaving a
# noise level of order 1e-14 relative to the second moments.  Asking phi to be
# reproducible to 1e-6 degrees (1.7e-8 rad) therefore requires i11 and i22 to
# differ by more than about 1e-6 relative.  Below that the axis direction carries
# no information.
PRINCIPAL_DEGENERACY = 1e-6

PRINCIPAL_FIELDS = frozenset(
    {
        "phi",
        "x11_se",
        "y22_se",
        "x11_pc",
        "y22_pc",
        "beta_11_plus",
        "beta_11_minus",
        "beta_22_plus",
        "beta_22_minus",
    }
)


def _principal_axis_undetermined(record: dict[str, Any]) -> bool:
    """Whether the profile's principal axis directions are undetermined."""
    i11 = record.get("i11_c")
    i22 = record.get("i22_c")

    if i11 is None or i22 is None:
        return False

    return abs(i11 - i22) <= PRINCIPAL_DEGENERACY * abs(i11)


def _array_summary(values: np.ndarray) -> dict[str, float]:
    """Reduce a nodal result array to order-independent scalars."""
    return {
        "min": float(np.min(values)),
        "max": float(np.max(values)),
        "sum": float(np.sum(values)),
        "l2": float(np.linalg.norm(values)),
    }


def collect(profile: Any) -> dict[str, Any]:
    """Compute all section properties for a single profile."""
    section = profile._section()
    section.calculate_geometric_properties()
    section.calculate_warping_properties()
    section.calculate_plastic_properties()

    record: dict[str, Any] = {
        "num_nodes": section.num_nodes,
        "num_elements": len(section.mesh_elements),
    }

    for key, value in asdict(section.section_props).items():
        if key in ARRAY_FIELDS:
            record[key] = _array_summary(np.asarray(value)) if value is not None else None
        elif value is None:
            record[key] = None
        elif key == "a_sxy":
            record["inv_a_sxy"] = 1.0 / float(value)
        else:
            record[key] = float(value)

    return record


def _tolerance(field: str, record: dict[str, Any], rtol: float) -> float:
    """Absolute tolerance for a field, derived from the profile's own scale."""
    area = record["area"]
    length = math.sqrt(area)
    dimension = DIMENSION.get(field)

    if dimension is None:
        # unknown field: fall back to a pure relative check
        return 0.0

    return FLOOR * length**dimension * (rtol / 1e-6)


def compare(reference: dict[str, Any], current: dict[str, Any], rtol: float) -> int:
    """Print a comparison report and return the number of significant differences."""
    failures = 0
    checked = 0
    skipped = 0
    degenerate: list[str] = []
    worst = (0.0, "")

    for name in sorted(reference):
        if name not in current:
            print(f"MISSING  {name}")
            failures += 1
            continue

        ref = reference[name]
        cur = current[name]

        undetermined = _principal_axis_undetermined(ref)
        if undetermined:
            degenerate.append(name)

        for key in ("num_nodes", "num_elements"):
            if ref[key] != cur[key]:
                print(f"MESH     {name}.{key}: ref={ref[key]} cur={cur[key]}")
                failures += 1

        for field, ref_value in sorted(ref.items()):
            if ref_value is None or field in ("num_nodes", "num_elements"):
                continue

            if undetermined and field in PRINCIPAL_FIELDS:
                skipped += 1
                continue

            cur_value = cur.get(field)

            if isinstance(ref_value, dict):
                # nodal result array: scale by the largest value in the array
                scale = max(abs(ref_value["min"]), abs(ref_value["max"]))
                factors = {
                    "min": 1.0,
                    "max": 1.0,
                    "sum": float(ref["num_nodes"]),
                    "l2": math.sqrt(ref["num_nodes"]),
                }
                for stat, factor in factors.items():
                    checked += 1
                    diff = abs(cur_value[stat] - ref_value[stat])
                    tolerance = max(rtol * abs(ref_value[stat]), FLOOR * scale * factor * (rtol / 1e-6))
                    ratio = diff / tolerance if tolerance else 0.0
                    if ratio > worst[0]:
                        worst = (ratio, f"{name}.{field}.{stat}")
                    if diff > tolerance:
                        print(f"DIFF     {name}.{field}.{stat}: ref={ref_value[stat]!r} cur={cur_value[stat]!r} diff={diff:.3e} tol={tolerance:.3e}")
                        failures += 1
                continue

            checked += 1
            diff = abs(cur_value - ref_value)

            tolerance = PHI_ATOL_DEG if field == "phi" else max(rtol * abs(ref_value), _tolerance(field, ref, rtol))

            ratio = diff / tolerance if tolerance else 0.0
            if ratio > worst[0]:
                worst = (ratio, f"{name}.{field}")

            if diff > tolerance:
                print(f"DIFF     {name}.{field}: ref={ref_value!r} cur={cur_value!r} diff={diff:.3e} tol={tolerance:.3e}")
                failures += 1

    print(f"\nchecked {checked} values across {len(reference)} profiles at rtol={rtol:g}")
    print(f"largest fraction of the allowed tolerance used: {worst[0]:.3e}  ({worst[1]})")

    if skipped:
        print(f"skipped {skipped} principal-axis values on {len(degenerate)} profiles where i11 == i22 makes the axis direction undetermined:")
        for name in degenerate:
            print(f"    {name}")

    print("SIGNIFICANT DIFFERENCES:", failures)
    return failures


def report(reference: dict[str, Any], current: dict[str, Any]) -> None:
    """Print how far every property moved, without a pass or fail judgement.

    Used to quantify a deliberate change such as a different mesh, where the numbers
    are expected to move and the question is by how much.
    """
    moved: dict[str, list[float]] = {}
    negligible = 0

    for name in sorted(reference):
        if name not in current:
            continue

        ref = reference[name]
        cur = current[name]
        undetermined = _principal_axis_undetermined(ref)
        length = abs(ref["area"]) ** 0.5

        for field, ref_value in ref.items():
            if ref_value is None or field in ("num_nodes", "num_elements"):
                continue
            if isinstance(ref_value, dict) or field == "phi":
                continue
            if undetermined and field in PRINCIPAL_FIELDS:
                continue

            dimension = DIMENSION.get(field)
            if dimension is not None and abs(ref_value) < NEGLIGIBLE * length**dimension:
                # numerically zero for this section: the shear centre of a doubly
                # symmetric profile sits on the centroid, so what a run reports for
                # x_se, the monosymmetry constants and 1 / a_sxy is rounding noise
                negligible += 1
                continue

            cur_value = cur.get(field)
            if cur_value is None:
                continue

            moved.setdefault(field, []).append(abs(cur_value - ref_value) / abs(ref_value))

    print()
    print(f"skipped {negligible} values that are numerically zero for their section")
    print(f"{'property':<16}{'max rel change':>16}{'median':>14}{'profiles':>10}")
    print("-" * 56)
    for field in sorted(moved, key=lambda f: max(moved[f]), reverse=True):
        values = sorted(moved[field])
        median = values[len(values) // 2]
        print(f"{field:<16}{max(values):>16.2e}{median:>14.2e}{len(values):>10}")

    overall = [value for values in moved.values() for value in values]
    print()
    print(f"{'ALL':<16}{max(overall):>16.2e}{sorted(overall)[len(overall) // 2]:>14.2e}{len(overall):>10}")


def main() -> int:
    """Run the reference collection or comparison."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=None, help="write the collected values to this JSON file")
    parser.add_argument("--compare", type=Path, default=None, help="compare against a previously written JSON file")
    parser.add_argument("--report", type=Path, default=None, help="report how far every property moved against this file")
    parser.add_argument("--families", nargs="*", default=list(FAMILIES), help="profile families to include")
    parser.add_argument("--limit", type=int, default=0, help="only the first N profiles per family")
    parser.add_argument("--rtol", type=float, default=1e-6, help="relative tolerance for --compare")
    args = parser.parse_args()

    results: dict[str, Any] = {}
    for family_name in args.families:
        family = FAMILIES[family_name]
        profiles = list(family)
        if args.limit:
            profiles = profiles[: args.limit]
        for profile in profiles:
            key = f"{family_name}.{profile.name}"
            print(f"  {key} ...", flush=True)
            results[key] = collect(profile)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(results, indent=2, sort_keys=True))
        print(f"\nwritten to {args.output}")

    if args.report:
        report(json.loads(args.report.read_text()), results)

    if args.compare:
        reference = json.loads(args.compare.read_text())
        return 1 if compare(reference, results, rtol=args.rtol) else 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Reference harness for the stress analysis path.

`Profile.unit_stress()` feeds the Eurocode shear check, so the vectorised stress
analysis has to reproduce the element-wise one node for node.  This script dumps
the full nodal stress field for a few profiles and compares two runs.

Usage
-----
    python benchmarks/verify_stress.py --output benchmarks/results/stress_master.json
    python benchmarks/verify_stress.py --compare benchmarks/results/stress_master.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

import _bootstrap  # noqa: F401  # isort: skip  - must run before blueprints imports

from blueprints.structural_sections.steel.standard_profiles.heb import HEB
from blueprints.structural_sections.steel.standard_profiles.ipe import IPE
from blueprints.structural_sections.steel.standard_profiles.unp import UNP

PROFILES = [("HEB", "HEB300"), ("IPE", "IPE300"), ("UNP", "UNP200"), ("HEB", "HEB1000")]

FAMILIES = {"HEB": HEB, "IPE": IPE, "UNP": UNP}


def collect(family: str, name: str) -> dict[str, Any]:
    """Collect the full nodal stress field of one profile under unit actions."""
    profile = getattr(FAMILIES[family], name)
    stress = profile.unit_stress()

    record: dict[str, Any] = {}
    for key, value in stress.items():
        array = np.asarray(value)
        if array.dtype.kind not in "fiu":
            continue
        record[key] = {
            "min": float(array.min()),
            "max": float(array.max()),
            "sum": float(array.sum()),
            "l2": float(np.linalg.norm(array)),
            "size": int(array.size),
        }

    return record


def compare(reference: dict[str, Any], current: dict[str, Any], rtol: float) -> int:
    """Compare two stress fields and report significant differences."""
    failures = 0
    worst = (0.0, "")

    for name in sorted(reference):
        ref = reference[name]
        cur = current[name]

        for field, ref_stats in sorted(ref.items()):
            cur_stats = cur[field]
            scale = max(abs(ref_stats["min"]), abs(ref_stats["max"]))

            for stat in ("min", "max", "sum", "l2"):
                factor = {
                    "min": 1.0,
                    "max": 1.0,
                    "sum": float(ref_stats["size"]),
                    "l2": float(ref_stats["size"]) ** 0.5,
                }[stat]

                diff = abs(cur_stats[stat] - ref_stats[stat])
                tolerance = max(rtol * abs(ref_stats[stat]), rtol * scale * factor)
                ratio = diff / tolerance if tolerance else 0.0

                if ratio > worst[0]:
                    worst = (ratio, f"{name}.{field}.{stat}")

                if diff > tolerance:
                    print(f"DIFF  {name}.{field}.{stat}: ref={ref_stats[stat]!r} cur={cur_stats[stat]!r} diff={diff:.3e} tol={tolerance:.3e}")
                    failures += 1

    print(f"\nlargest fraction of the allowed tolerance used: {worst[0]:.3e}  ({worst[1]})")
    print("SIGNIFICANT DIFFERENCES:", failures)
    return failures


def main() -> int:
    """Collect or compare the stress reference."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--compare", type=Path, default=None)
    parser.add_argument("--rtol", type=float, default=1e-6)
    args = parser.parse_args()

    results = {}
    for family, name in PROFILES:
        print(f"  {name} ...", flush=True)
        results[name] = collect(family, name)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(results, indent=2, sort_keys=True))
        print(f"\nwritten to {args.output}")

    if args.compare:
        reference = json.loads(args.compare.read_text())
        return 1 if compare(reference, results, rtol=args.rtol) else 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

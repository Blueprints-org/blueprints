"""Runs the HEB sweep across processes.

Every profile is an independent analysis, so a sweep over a catalogue is
embarrassingly parallel. This is not a change to sectionproperties, it is what
the calling script can do once the per-profile cost has been brought down: the
numbers each worker produces are bit for bit the ones a serial run produces.

Usage
-----
    python benchmarks/parallel_sweep.py
    python benchmarks/parallel_sweep.py --workers 4
"""

from __future__ import annotations

import argparse
import os
import time
from concurrent.futures import ProcessPoolExecutor

import _bootstrap  # noqa: F401  # isort: skip  - must run before blueprints imports

from blueprints.structural_sections.steel.standard_profiles.heb import HEB


def analyse(name: str) -> tuple[str, float, float]:
    """Runs the full analysis for one profile and returns a couple of results."""
    profile = getattr(HEB, name)
    props = profile.section_properties(geometric=True, plastic=True, warping=True)

    return name, float(props.ixx_c), float(props.j)


def run_serial(names: list[str]) -> list[tuple[str, float, float]]:
    """Runs every profile in this process."""
    return [analyse(name) for name in names]


def run_parallel(names: list[str], workers: int) -> list[tuple[str, float, float]]:
    """Runs the profiles across a process pool."""
    with ProcessPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(analyse, names))


def main() -> None:
    """Compare serial and parallel wall time and check the results agree."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=0, help="worker processes (default: CPU count)")
    args = parser.parse_args()

    workers = args.workers or (os.cpu_count() or 1)
    names = [profile.name for profile in HEB]

    start = time.perf_counter()
    serial = run_serial(names)
    t_serial = time.perf_counter() - start

    start = time.perf_counter()
    parallel = run_parallel(names, workers=workers)
    t_parallel = time.perf_counter() - start

    identical = serial == parallel

    print(f"profiles           {len(names)}")
    print(f"serial             {t_serial:.3f} s")
    print(f"parallel ({workers:>2} proc) {t_parallel:.3f} s   speedup {t_serial / t_parallel:.1f}x")
    print(f"results identical  {identical}")

    if not identical:
        for a, b in zip(serial, parallel, strict=True):
            if a != b:
                print(f"  {a[0]}: serial={a[1:]!r} parallel={b[1:]!r}")


if __name__ == "__main__":
    main()

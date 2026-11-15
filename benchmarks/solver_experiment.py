"""Compares sparse factorisation strategies for the warping stiffness matrix.

The Lagrangian multiplier formulation appends a completely dense row and column
to an otherwise very sparse finite element matrix.  This script measures what
that costs, and what the alternative (pinning a single degree of freedom and
restoring the constraint afterwards) costs instead.
"""

from __future__ import annotations

import argparse
import time

import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import splu

import _bootstrap  # noqa: F401  # isort: skip  - must run before blueprints imports

from blueprints.structural_sections.steel.standard_profiles.heb import HEB


def timed(label: str, fn) -> object:
    """Runs ``fn`` and prints how long it took."""
    start = time.perf_counter()
    result = fn()
    print(f"  {label:<44}{time.perf_counter() - start:>8.3f} s")
    return result


def main() -> None:
    """Factorise the warping matrix in several ways and compare the timings."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", nargs="?", default="HEB600")
    args = parser.parse_args()

    profile = getattr(HEB, args.profile)
    section = profile._section()
    section.calculate_geometric_properties()

    batch = section.element_batch(origin=section.get_c())
    k_lg, f_torsion = section.assemble_torsion(batch=batch)
    n = section.num_nodes

    print(f"{args.profile}: {section.num_elements} elements, {n} nodes")
    print(f"  k_lg nnz: {k_lg.nnz}")

    # the plain finite element matrix without the Lagrangian row and column
    k = csc_matrix(k_lg[:n, :n])
    c = np.asarray(k_lg[:n, n].todense()).ravel()
    print(f"  k    nnz: {k.nnz}")

    rhs = np.zeros(n + 1)
    rhs[:n] = f_torsion

    for permc in ("COLAMD", "MMD_AT_PLUS_A"):
        lu = timed(f"splu(k_lg) permc_spec={permc}", lambda p=permc: splu(k_lg, permc_spec=p))
        print(f"    fill-in nnz(L)+nnz(U) = {lu.L.nnz + lu.U.nnz}")
        omega_lg = timed("  solve", lambda lu=lu: lu.solve(rhs))[:n]
        del lu

    # pinned formulation: fix the dof with the largest diagonal, then restore the
    # constraint c . omega = 0 by shifting the solution by a constant
    diagonal = k.diagonal()
    pin = int(np.argmax(diagonal))
    keep = np.ones(n, dtype=bool)
    keep[pin] = False
    k_red = csc_matrix(k[keep][:, keep])

    for permc in ("COLAMD", "MMD_AT_PLUS_A"):
        lu = timed(f"splu(k_pinned) permc_spec={permc}", lambda p=permc: splu(k_red, permc_spec=p))
        print(f"    fill-in nnz(L)+nnz(U) = {lu.L.nnz + lu.U.nnz}")
        x = timed("  solve", lambda lu=lu: lu.solve(f_torsion[keep]))
        omega = np.zeros(n)
        omega[keep] = x
        omega -= (c @ omega) / c.sum()
        print(f"    max|omega_pinned - omega_lagrange| = {np.abs(omega - omega_lg).max():.3e}")
        print(f"    max|omega_lagrange|                = {np.abs(omega_lg).max():.3e}")
        del lu


if __name__ == "__main__":
    main()

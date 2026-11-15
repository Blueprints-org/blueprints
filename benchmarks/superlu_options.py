"""Compares SuperLU factorisation options on the pinned warping system.

The pinned stiffness matrix is symmetric positive definite, so SuperLU's
symmetric mode (no partial pivoting, symmetric fill-reducing ordering) should
beat the general purpose defaults.
"""

from __future__ import annotations

import time

import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import splu

import _bootstrap  # noqa: F401  # isort: skip  - must run before blueprints imports

from sectionproperties.analysis import batch as sp_batch

from blueprints.structural_sections.steel.standard_profiles.heb import HEB

PROFILES = ["HEB200", "HEB400", "HEB700", "HEB1000"]

VARIANTS = {
    "COLAMD (current)": {"permc_spec": "COLAMD"},
    "MMD_AT_PLUS_A": {"permc_spec": "MMD_AT_PLUS_A"},
    "symmetric mode": {
        "permc_spec": "MMD_AT_PLUS_A",
        "diag_pivot_thresh": 0.0,
        "options": {"SymmetricMode": True},
    },
    "COLAMD, no pivoting": {"permc_spec": "COLAMD", "diag_pivot_thresh": 0.0},
}


def build_system(name: str):
    """Assembles and pins the warping system of a profile."""
    profile = getattr(HEB, name)
    section = profile._section()
    section.calculate_geometric_properties()

    element_batch = section.element_batch(origin=section.get_c())
    k, _, f_torsion = section.assemble_warping(batch=element_batch)

    ixx, iyy, ixy = section.get_ic()
    f_psi_el, f_phi_el = sp_batch.shear_load_vectors(
        batch=element_batch,
        elastic_modulus=section.element_elastic_modulus,
        ixx=ixx,
        iyy=iyy,
        ixy=ixy,
        nu=0.0,
    )
    flat = element_batch.node_ids.ravel()
    f = np.column_stack(
        (
            f_torsion,
            np.bincount(flat, weights=f_psi_el.ravel(), minlength=section.num_nodes),
            np.bincount(flat, weights=f_phi_el.ravel(), minlength=section.num_nodes),
        )
    )

    n = k.shape[0]
    pinned = int(np.argmax(k.diagonal()))
    free = np.ones(n, dtype=bool)
    free[pinned] = False

    return section.num_nodes, csc_matrix(k.tocsr()[free][:, free]), f[free, :]


def main() -> None:
    """Time each SuperLU option set and check the solutions agree."""
    header = f"{'profile':<10}{'nodes':>8}" + "".join(f"{name:>22}" for name in VARIANTS)
    print(header)
    print("-" * len(header))

    for name in PROFILES:
        n_nodes, k_free, f_free = build_system(name)

        timings = []
        reference = None

        for kwargs in VARIANTS.values():
            start = time.perf_counter()
            lu = splu(k_free, **kwargs)
            x = lu.solve(f_free)
            elapsed = time.perf_counter() - start

            if reference is None:
                reference = x
                diff = 0.0
            else:
                diff = float((np.abs(x - reference).max(axis=0) / np.abs(reference).max(axis=0)).max())

            timings.append(f"{elapsed:.3f} s ({diff:.1e})")
            del lu

        print(f"{name:<10}{n_nodes:>8}" + "".join(f"{value:>22}" for value in timings))


if __name__ == "__main__":
    main()

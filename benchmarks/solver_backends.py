"""Compares the SuperLU and PARDISO backends on the pinned warping system."""

from __future__ import annotations

import time

import numpy as np

import _bootstrap  # noqa: F401  # isort: skip  - must run before blueprints imports

from sectionproperties.analysis import batch as sp_batch
from sectionproperties.analysis import solver

from blueprints.structural_sections.steel.standard_profiles.heb import HEB

PROFILES = ["HEB100", "HEB200", "HEB300", "HEB500", "HEB700", "HEB1000"]


def build_system(name: str):
    """Assembles the warping system of a profile."""
    profile = getattr(HEB, name)
    section = profile._section()
    section.calculate_geometric_properties()

    element_batch = section.element_batch(origin=section.get_c())
    k, c, f_torsion = section.assemble_warping(batch=element_batch)

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
    f_psi = np.bincount(flat, weights=f_psi_el.ravel(), minlength=section.num_nodes)
    f_phi = np.bincount(flat, weights=f_phi_el.ravel(), minlength=section.num_nodes)

    return section, k, c, np.column_stack((f_torsion, f_psi, f_phi))


def main() -> None:
    """Time both backends on identical systems and report the difference."""
    header = f"{'profile':<10}{'nodes':>8}{'SuperLU':>10}{'PARDISO':>10}{'max rel diff':>15}"
    print(header)
    print("-" * len(header))

    for name in PROFILES:
        section, k, c, f = build_system(name)

        solver._HAS_PARDISO = False
        start = time.perf_counter()
        u_superlu = solver.solve_warping_direct(k=k, c=c, f=f)
        t_superlu = time.perf_counter() - start

        solver._HAS_PARDISO = True
        start = time.perf_counter()
        u_pardiso = solver.solve_warping_direct(k=k, c=c, f=f)
        t_pardiso = time.perf_counter() - start

        scale = np.abs(u_superlu).max(axis=0)
        rel = (np.abs(u_superlu - u_pardiso).max(axis=0) / scale).max()

        print(f"{name:<10}{section.num_nodes:>8}{t_superlu:>10.3f}{t_pardiso:>10.3f}{rel:>15.2e}")


if __name__ == "__main__":
    main()

# Section property benchmarks

Measurement and verification harness for the sectionproperties speed-up work.
Everything here runs against the checked-out Blueprints tree and whatever
`sectionproperties` is importable, so switching branches in the
`section-properties` checkout switches what is being measured.

The scripts stub out the three reporting dependencies Blueprints imports at
module load (`googletrans`, `latex2mathml`, `mathml2omml`) via `_bootstrap.py`,
so they run in a bare environment without touching site-packages.

## Measuring

| Script | What it does |
| --- | --- |
| `profile_heb.py` | Per-profile table of mesh, geometric, warping and plastic time over all HEB profiles |
| `solver_split.py` | Same sweep, split into assembly, linear solve and the rest. `--no-pardiso` forces the SuperLU path |
| `breakdown_heb.py` | Single profile, split down to polygon, meshing, `Section()` and each analysis stage |
| `cprofile_heb.py` | `cProfile` of one stage of one profile |
| `cprofile_run.py` | `cProfile` of the whole sweep |
| `solver_backends.py` | SuperLU against PARDISO on identical warping systems |
| `solver_experiment.py` | What the dense Lagrangian row costs a sparse factorisation |
| `superlu_options.py` | SuperLU ordering and pivoting options on the pinned system |
| `mesh_sensitivity.py` | What coarsening the mesh costs in accuracy and buys in time |
| `mesh_calibration.py` | Section properties against a `t/n` mesh rule, referenced to a `t/16` mesh |
| `mesh_calibration_stress.py` | The same for the peak stresses, which do not converge |
| `shear_check_sensitivity.py` | Class 3/4 shear capacity as a function of the mesh rule |
| `headline.py` | Both mesh rules alternated in one process, normalised for CPU clock |
| `parallel_sweep.py` | The same sweep across processes, for comparison |
| `stress_timing.py` | Analysis time against `calculate_stress` time per profile |
| `cprofile_stress.py` | `cProfile` of one stress analysis |
| `reproducibility.py` | How far the torsion constant moves between identical runs |

`RESULTS.md` holds the measurements these produced and the reasoning behind each
change.

## Verifying

`verify_properties.py` computes every section property Blueprints exposes for a
set of standard profiles and either writes them to JSON or compares against a
previously written file. `verify_stress.py` does the same for the full nodal
stress field behind `Profile.unit_stress()`.

```bash
# on the reference branch
python benchmarks/verify_properties.py --families HEB --output benchmarks/results/reference_heb_full.json

# on the branch under test
python benchmarks/verify_properties.py --families HEB --compare benchmarks/results/reference_heb_full.json
```

The comparison is not a plain relative check. Several section properties are
sums of large contributions that cancel almost completely — for a doubly
symmetric profile `ixy` and `kappa_xy` are zero in theory, so what a run reports
for them is rounding noise. Comparing `1e-10` against `5e-9` says nothing about
accuracy. Every property is therefore compared against a tolerance built from the
profile's own characteristic length `L = sqrt(area)` raised to that property's
dimension, and `a_sxy` is compared through its reciprocal. Where `i11` equals
`i22` the principal axis direction is undetermined, and the angle and everything
positioned along it are reported as skipped rather than compared.

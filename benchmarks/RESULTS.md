# Sectionproperties speed-up — results

Branch under test: `feature/vectorised-analysis` in `C:\Python\Andere projecten\section-properties`
(6 local commits on top of `master`, which is upstream v3.10.2). Blueprints changes: one file,
`blueprints/structural_sections/_profile.py`, plus this `benchmarks/` folder.

There are two separate changes here, and they should be reviewed separately.

**The sectionproperties change** is held to: same mesh, results equal to within 1e-6 relative,
numpy and scipy only, no new dependencies. It is verified against unmodified v3.10.2 at both
mesh rules and passes at 1e-6 with room to spare.

**The Blueprints mesh change** deliberately moves the numbers. It is calibrated against a much
finer reference mesh rather than against the old one, and its effect is quantified below. One
consequence needs an engineering decision rather than a code review; it is called out under
"the class 3/4 shear check".

**Not shipped.** Main has since adopted its own mesh rule, `mesh_sizes = max_thickness**2 / 32`,
and this branch now uses that one. The headline has been re-measured with main's rule, and its
accuracy has been calibrated against the same `t/16` reference, under "main's rule". Every
other number below labelled "wall-thickness mesh" or "t/4" was measured with the `t/4` rule
described under "the mesh rule" and has not been re-measured.

## Which interpreter you are running

The numbers below were measured on the global Python 3.13 interpreter, where this branch is
installed editable **and `pypardiso` happens to be installed**. The project's own uv environment
has neither: `uv run` installs `sectionproperties` from PyPI and has no `pypardiso`.

That matters a great deal, because `pypardiso` is what kept the old dense-Lagrangian solve from
being catastrophic. Same script, same uv environment, same wall-thickness mesh, only the
sectionproperties build differing:

| `uv run` with              | `need_for_speed.py` |
|----------------------------|--------------------:|
| sectionproperties 3.10.2 from PyPI |         408.2 s |
| this branch                | **1.46 / 1.78 / 2.04 s** |

So in the environment the project actually ships, the improvement is far larger than it is with
PARDISO, because the baseline there is the unaccelerated solver path. The headline below is
measured in that environment.

`uv run` re-syncs the environment from `uv.lock` on every invocation, so an editable install put
there by hand is silently replaced by the PyPI build on the next run. `pyproject.toml` therefore
names the source explicitly:

```toml
[tool.uv.sources]
sectionproperties = { path = "../section-properties", editable = true }
```

With that in place plain `uv run` resolves to the branch, and `uv.lock` records the checkout
rather than the PyPI wheel. Both files are part of this change.

**This expects the `section-properties` repository to sit next to this one, and fails anywhere it
does not — CI included.** It has to come back out, or point at a released version, before this is
merged.

## Headline

Re-measured on 2026-11-10 with `benchmarks/headline.py`, after main adopted its own mesh rule.
24 HEB profiles, geometric + warping + plastic, in the project's uv environment, so **without
`pypardiso`**. Best of three runs on the branch, one run on v3.10.2.

|                       | flat 2.0 mm² | t/4 thickness | main: max t² / 32 |
|-----------------------|-------------:|--------------:|------------------:|
| elements              |      339 937 |        66 776 |            44 404 |
| v3.10.2               |     1805.7 s |       183.8 s |            79.2 s |
| this branch           |       23.9 s |         5.6 s |        **4.40 s** |
| code factor           |          76x |           33x |               18x |
| mesh factor, branch   |            - |         4.30x |             5.42x |
| mesh factor, v3.10.2  |            - |          9.8x |             22.8x |

What ships is the last column: main's mesh rule with this branch's code. Against v3.10.2 on
that same mesh the code is **18x** faster. The mesh factors are measured within one process,
with the rules alternated, and are the reliable numbers here.

The code factors are taken across two processes and are not. `headline.py` divides every
timing by a fixed calibration workload, and that workload ran 4.4x slower in the branch run
than in the v3.10.2 run. Normalised, the code factor at main's mesh comes out at 79x instead
of 18x. The raw seconds above are the conservative reading; run both on a quiet machine for
a clean number.

Without `pypardiso` the old code is dominated by the dense-Lagrangian warping solve (1492 s of
the 1806 s at the flat mesh), which is why the code factor grows with the element count.

Main's rule sizes the mesh from the thickest wall, so for an I-profile it is coarser over the
web than `t/4`. It still stays below 1e-4 against a `t/16` reference on every profile
measured, see "main's rule" under "the mesh rule".

## Where the time went, and where it goes now

Sum over the 24 HEB profiles at the **old flat mesh** — 339 937 elements, 702 555 nodes — after a
warm-up analysis, on a quiet machine. This isolates the code change from the mesh change:

| stage                            |     v3.10.2 | this branch |  factor |
|----------------------------------|------------:|------------:|--------:|
| mesh + `Section()`               |     18.60 s |      1.26 s |     15x |
| `calculate_geometric_properties` |     38.12 s |      0.32 s |    118x |
| `calculate_warping_properties`   |    127.98 s |      4.38 s |     29x |
| `calculate_plastic_properties`   |      0.53 s |      0.23 s |    2.3x |
| **wall total**                   | **185.2 s** |  **6.18 s** | **30x** |

The stress path, which the Eurocode shear check reaches through `Profile.unit_stress()`:

| `Section.calculate_stress` | v3.10.2 | this branch | factor |
|----------------------------|--------:|------------:|-------:|
| HEB300                     |  3.98 s |      0.13 s |    30x |
| HEB600                     |  5.79 s |      0.39 s |    15x |
| HEB1000                    | 13.87 s |      0.60 s |    23x |

## What was changed, and the measurement behind each change

### 1. The element loops became array operations

`Tri6` evaluates one element at a time: an HEB1000 mesh has 31 729 elements and every analysis
walked all of them in Python, four Gauss points at a time, through a `functools.cache` keyed on a
12-tuple of coordinates. A new module `sectionproperties/analysis/batch.py` computes the same shape
functions, Jacobians, strain matrices and integrals for the whole mesh in a handful of array
operations. The maths mirrors `Tri6` one-to-one; only the loop structure differs, and
`tests/analysis/test_batch.py` asserts that element by element.

`Section` now keeps the mesh as arrays (`element_coords`, per-element material properties) and
builds the `Tri6` objects, the material-group element lists and the `STRtree` only when something
asks for them. Nothing in an analysis asks for them any more.

### 2. The warping analysis stopped building a second `Section`

`calculate_warping_properties` used to construct a whole second `Section` from the same geometry —
including a shapely `STRtree` over every triangle — purely to shift the element coordinates to the
centroid. That was 1.17 s of the 6.25 s an HEB300 warping analysis took. It now shifts the
coordinate array instead.

### 3. One factorisation instead of three

The warping function and the two shear functions solve the same matrix with three different right
hand sides. All three right hand sides are now assembled before the first solve, and the matrix is
factorised once.

### 4. The dense Lagrangian row was the real bottleneck

The constraint that removes the constant from the warping function was imposed by appending a
**fully dense** row and column to an otherwise very sparse finite element matrix. Eliminating that
row during factorisation is catastrophic. Measured on HEB300 (24 610 nodes, `k` has 276 052
non-zeros):

| system                       | SuperLU factorisation | fill-in, nnz(L)+nnz(U) |
|------------------------------|----------------------:|-----------------------:|
| Lagrangian, COLAMD (v3.10.2) |                5.58 s |             39 447 582 |
| Lagrangian, MMD_AT_PLUS_A    |                2.20 s |             10 438 551 |
| **one dof pinned, COLAMD**   |            **0.20 s** |          **1 553 317** |

`solver.solve_warping_direct` now fixes the best-conditioned degree of freedom, solves the resulting
positive definite system, and shifts the solution by the constant that satisfies the constraint.
Mathematically the same solution; the difference against the Lagrangian result is 2e-12 relative.

The consequence for a stock install is dramatic. Without `pypardiso` — which is an optional extra,
not a dependency — the sweep spent **183 s of 193 s inside `scipy.sparse.linalg.spsolve`**. It now
spends about 3 s there.

It also inverts the solver choice. On the pinned system SuperLU beats PARDISO at every size tested:

| profile |  nodes | SuperLU | PARDISO |
|---------|-------:|--------:|--------:|
| HEB100  |  4 574 | 0.026 s | 0.205 s |
| HEB300  | 24 610 | 0.137 s | 0.255 s |
| HEB700  | 49 959 | 0.300 s | 0.469 s |
| HEB1000 | 65 172 | 0.406 s | 0.637 s |

So PARDISO is no longer used for the warping solve even when installed. `solver.USE_PARDISO_FOR_WARPING = True`
switches it back. PARDISO is still used for the Lagrangian entry points, where it genuinely helps.

Since the pinned matrix is symmetric positive definite, SuperLU is now called in symmetric mode
(symmetric ordering, no partial pivoting), worth another 1.2–1.4x on the factorisation.

### 5. Two remaining Python loops over all mesh nodes

`post.calculate_centroidal_properties` looped over every mesh node to find the extreme fibres in
principal coordinates — 1.27 s of the sweep and 1.4 million `min`/`max` calls. The yield-moment loop
in `calculate_geometric_properties` walked every node of every element. Both are now array
expressions.

### 6. The stress analysis

`Tri6.element_stress` was 74% of `calculate_stress`, and `StressPost` deep-copied every `Tri6` object
in the section (another 13%). The stress kernel is vectorised and `StressPost` now shares the element
objects with the `Section` instead of copying them; each group still gets its own `StressResult`.

### 7. Blueprints: one mesh per profile

`Profile.calculate_stress` built a fresh `Section` and re-ran the geometric, plastic and warping
analyses on every call, and `section_properties()` did the same once per flag combination. A profile
now keeps one meshed `Section` and runs each analysis at most once.

## Verification

Everything was compared against the numbers produced by unmodified v3.10.2 on the same machine.

| check                        | scope                                   | mesh           | result                            |
|------------------------------|-----------------------------------------|----------------|-----------------------------------|
| section properties           | 24 HEB profiles, 2 088 values           | flat 2.0 mm²   | 0 differences, worst 82% of tol.  |
| section properties           | 48 profiles, six families, 4 104 values | flat 2.0 mm²   | 0 differences, worst 21% of tol.  |
| section properties           | 24 HEB profiles, 2 088 values           | wall thickness | 0 differences, worst 32% of tol.  |
| section properties           | 48 profiles, six families, 4 104 values | wall thickness | 0 differences, worst 20% of tol.  |
| full nodal stress field      | HEB300, HEB1000, IPE300, UNP200         | flat 2.0 mm²   | 0 differences, worst 7e-5 of tol. |
| full nodal stress field      | HEB300, HEB1000, IPE300, UNP200         | wall thickness | 0 differences, worst 2e-5 of tol. |
| sectionproperties test suite | `tests/`, minus the benchmark suite     | —              | 156 passed, 5 pre-existing fails  |
| blueprints test suite        | `tests/`, minus `test_cli.py`           | wall thickness | 7 560 passed                      |

The 5 sectionproperties failures are `ImportError` for the optional `cad_to_shapely` and `rhino3dm`
packages; they fail identically on `master`. The 6 `test_cli.py` failures in Blueprints are a
typer/click problem in this environment — confirmed by stashing my change and re-running.

The comparison is not a plain relative check, and that matters for reading the result. Several
section properties are sums of large contributions that cancel almost completely: for a doubly
symmetric profile `ixy` and `kappa_xy` are zero in theory, so what a run reports for them is rounding
noise, and `1e-10` against `5e-9` is a 100% relative difference between two zeroes. Every property is
therefore compared against a tolerance built from the profile's own characteristic length
`L = sqrt(area)` raised to that property's dimension, `a_sxy` is compared through its reciprocal, and
for the circular sections — where `i11 == i22` makes the principal axis direction undetermined — the
axis angle and everything positioned along it are reported as skipped rather than compared. The rules
and the reasoning are in `verify_properties.py`.

**On reproducibility**: the torsion constant is not bit-reproducible between identical runs on either
branch — threaded BLAS changes the summation order. Measured for HEB180 over six runs:

```
master:  422697.5398302078  422697.53982963413  422697.5398300588 ...
branch:  422697.5398264453  422697.5398272127   422697.5398264453 ...
```

Spread within a branch ~1e-12 relative; offset between branches ~9e-12 relative. Both are six orders
below the 1e-6 requirement, and the noise is pre-existing.

## The 100x question

Not by this branch alone. With PARDISO the code change measured about 24x at the flat mesh; the
rest has to come from a coarser mesh, and the mesh change that ships is now main's, not this
branch's. Without PARDISO the flat-mesh sweep goes from 1806 s to 4.40 s, about 410x, but 23x
of that is main's mesh rule and the comparison is against the unaccelerated solver path.

With the mesh held fixed, 100x was not available. Of the 8.76 s the flat-mesh sweep now takes on
this branch, roughly 1.7 s is mesh generation in CyTriangle and roughly 5 s is the sparse
factorisation — a 65 172-dof system for HEB1000, already factorised once instead of three times,
without the dense Lagrangian row, in symmetric mode. That is a hard floor of around 6.5 s against
a 209 s baseline, so about 30x, and the branch is at 24x. The Python overhead that vectorisation
removes is essentially gone; what is left is the numerical work itself.

The remaining factor has to come from solving a smaller problem, which is what a mesh rule does.
The `t/4` rule measured below removes elements that were not buying any accuracy, and for the
small profiles it makes the mesh *finer*. Main's rule removes more elements still, at a cost
of up to a factor two in accuracy on I and U profiles, still a factor ten inside 0.1%.

## The mesh rule (measured, not shipped)

Blueprints used to mesh every steel profile at a flat `mesh_sizes=2.0` mm², a mesh length of
1.41 mm regardless of the section. That is thirteen quadratic elements across the web of an
HEB1000 and under three across the web of an IPE80, so the accuracy varied by a factor of
250 across the catalogue while the cost tracked the section size.

The rule measured here is the one the geometric profiles already use, sized from the thinnest wall:

```python
mesh_length = max(min_thickness / 4, 1.0)  # mm
mesh_sizes = mesh_length**2  # mm²
```

The benchmark scripts take the thinnest wall from the profile's `*_thickness` fields, see
`min_thickness` in `benchmarks/mesh_calibration.py`. Main ships `max_thickness**2 / 32`
instead, which sizes the mesh from the thickest wall.

Over the 24 HEB profiles this takes the mesh from 339 937 elements to 66 776.

### Why four elements across the wall

Measured against a `t/16` reference mesh, on fourteen profiles spanning six families. The
governing property is always the torsion constant; every other property is either exactly
integrated or converges faster.

| rule               | HEB1000 |  IPE300 |  UNP300 | LNP 100x100x10 | RHS200x100x10 |
|--------------------|--------:|--------:|--------:|---------------:|--------------:|
| flat 2.0 mm² (old) | 1.4e-06 | 2.7e-05 | 8.1e-06 |        1.7e-05 |       4.2e-06 |
| t/2                | 3.5e-04 | 4.3e-04 | 3.1e-04 |        6.1e-04 |       1.7e-05 |
| **t/4**            | 4.1e-05 | 4.7e-05 | 4.0e-05 |        8.3e-05 |       1.2e-05 |
| t/6                | 1.2e-05 | 1.6e-05 | 1.0e-05 |        2.3e-05 |       5.8e-06 |

`t/4` lands at 3e-05 to 9e-05 everywhere, a factor twenty inside the 0.1% the existing profile
mesh rules are fitted to, and it makes the accuracy uniform instead of size dependent. `t/6`
buys another factor three in accuracy for roughly double the elements; `t/2` is too coarse.
`benchmarks/mesh_calibration.py` reproduces the table.

### Main's rule

Main ships `mesh_sizes = max_thickness**2 / 32`, which is a mesh length of `max_thickness / 5.66`.
Measured against the same `t/16` reference, on the same fourteen profiles. The governing
property is again the torsion constant for the open sections and the warping constant for the
tubes:

| rule               | HEB1000 |  IPE80  |  IPE300 |  UNP300 | LNP 100x100x10 | RHS200x100x10 |
|--------------------|--------:|--------:|--------:|--------:|---------------:|--------------:|
| t/4                | 4.1e-05 | 9.3e-05 | 4.7e-05 | 4.0e-05 |        8.3e-05 |       1.2e-05 |
| **main**           | 9.5e-05 | 9.6e-05 | 6.1e-05 | 6.1e-05 |        3.2e-05 |       6.3e-06 |
| elements, t/4      |    2980 |    1533 |    2722 |    1709 |            700 |          1801 |
| elements, main     |    1838 |    1623 |    2421 |    1403 |           1133 |          3040 |

The worst case over all fourteen profiles is 9.6e-05, a factor ten inside 0.1%. Main's rule
is not uniformly coarser than `t/4`:

* **I and U profiles**, where the flanges are thicker than the web: from HEB100, IPE300 and
  UNP300 upwards main meshes the web coarser, with 10 to 40% fewer elements, and the torsion
  constant is up to 2.3x less accurate (HEB1000). On the smallest ones (IPE80, UNP80) the two
  rules coincide. This is the only place where main's rule loses accuracy against `t/4`.
* **Single-thickness sections** (angles, tubes): `max_thickness` is the only wall, so main's
  rule is `t/5.66`, finer than `t/4`. Angles and RHS come out 2x to 2.6x more accurate; the
  large CHS is already at 2e-08 under both.

The CHS 21.3x2.3 row shows a relative deviation of 0.4 to 1.0 in `gamma` under every rule,
including the flat mesh. That is not an error: the warping constant of a circular tube is
zero in theory, and on this small section the `NEGLIGIBLE` filter in the script does not
catch the rounding noise. Its other properties sit at the same level as the other profiles.

**Peak stresses**, measured with `benchmarks/mesh_calibration_stress.py` on eleven profiles:
main's rule lands within 0.3 percentage points of `t/4` and `t/6` on every profile. The deviation from the
`t/16` reference is 0.01% to 4% under every rule, flat included, and barely changes between
`t/4` and `t/6`: the peaks sit at re-entrant corners and fillets, where the elastic solution is
singular and does not converge. For the weak-axis shear peak of HEB300 and HEB1000
(`sig_zxy_vx`) main's rule moves the stress by the same 1.8 to 2.3% against the flat mesh as
`t/4` does, so the class 3/4 shear check below reads the same 1405 kN for an HEB300 under both
rules.

Both scripts print main's rule as the `main tmax2/32` row.

### What the numbers actually did

Comparing the whole property set against the old flat mesh, on the same sectionproperties
build so only the mesh differs:

| property                    |             24 HEB profiles | 48 profiles across six other families |
|-----------------------------|----------------------------:|--------------------------------------:|
| `j` torsion constant        | max 4.0e-05, median 3.1e-05 |           max 2.7e-04, median 1.5e-05 |
| `a_sx`, `a_s11` shear areas |                 max 3.2e-06 |                           max 5.4e-06 |
| `a_sy`, `a_s22`             |                 max 1.9e-06 |                           max 3.8e-06 |
| `gamma` warping constant    |                 max 6.4e-07 |                           max 8.9e-06 |
| everything else             |                   ≤ 1.6e-13 |                             ≤ 1.6e-13 |

Only the four properties that come out of the finite element solve move at all. Area, the
second moments, the section moduli, the plastic moduli, the radii of gyration and the yield
moments are unchanged to rounding, because a quadratic triangle integrates them exactly over
a straight-sided triangulation of the same polygon — the mesh density genuinely does not
enter. `benchmarks/verify_properties.py --report` reproduces both columns.

### Speed

Measured back to back in one process, alternating the two mesh rules, so the ratio is not
affected by the machine's clock:

|             | flat 2.0 mm² | t/4 thickness |    factor |
|-------------|-------------:|--------------:|----------:|
| v3.10.2     |     209.30 s |       42.56 s | **4.92x** |
| this branch |       8.76 s |        1.71 s | **5.13x** |

### The one thing that did move: the class 3/4 shear check

`CheckStrengthShearClass34` divides the yield stress by `max(abs(sig_zxy_vx))` taken over
every node. For shear about the weak axis of an I-profile that maximum sits at the
flange-to-web fillet, where the elastic solution is singular, so it does not converge — it
keeps climbing as the mesh is refined. Measured on an HEB300:

| mesh               | V_Rd,y [kN] | vs old | V_Rd,z [kN] | vs old |
|--------------------|------------:|-------:|------------:|-------:|
| flat 2.0 mm² (old) |      1379.0 |      — |       607.2 |      — |
| t/2                |      1404.8 | +1.87% |       607.2 | −0.01% |
| **t/4**            |      1404.9 | +1.88% |       607.2 | −0.00% |
| t/6                |      1404.6 | +1.86% |       607.2 | −0.00% |
| t/10               |      1382.7 | +0.27% |       607.2 | +0.00% |
| flat 0.5 mm²       |      1364.9 | −1.02% |       607.2 | +0.00% |

The strong-axis resistance does not move at all — its peak sits in the web, away from the
fillet — and neither does the weak-axis resistance of an IPE300 (−0.00%). What moves is the
weak-axis resistance of the HEB family, by about 1.9%, in the less conservative direction.

Two expectations in `tests/checks/eurocode/steel/test_strength_shear.py` were snapshots of
the old mesh and have been updated from 1379 kN to 1405 kN, with the reasoning recorded in
the test docstring. **This is the one change in this branch that needs an engineering
sign-off rather than a code review**, because no mesh gives a "correct" answer here: 1379 kN
had no more claim to being right than 1405 kN. The underlying question — whether this check
should read a singular corner stress at all, rather than the VS/(It) stress that
EN 1993-1-1 6.2.6 describes — is a design decision in Blueprints that I have not touched.
`benchmarks/shear_check_sensitivity.py` reproduces the table.

## Process-level parallelism: measured and rejected

The 24 profiles are independent, so a process pool looks obvious. It is 3x *slower*:

|           | serial | 4 processes | 12 processes |
|-----------|-------:|------------:|-------------:|
| wall time |  7.8 s |      22.7 s |       41.7 s |

On Windows every worker re-imports numpy, scipy, shapely and blueprints. Now that a profile costs
about 0.3 s, start-up dominates completely. Worth revisiting only for a much larger catalogue and
with a persistent pool. `parallel_sweep.py` reproduces this.

## Behaviour changes worth a look during review

1. `Section.elements`, `Section.material_groups` and `Section.mesh_search_tree` are properties now,
   built on first access. Code that mutated `section.elements[i].coords` *before* an analysis no
   longer influences that analysis — the analyses read `Section.element_coords`. Upstream did exactly
   this internally, which is why the warping analysis needed a second `Section`; nothing does it now.
2. `StressPost.material_groups` shares the `Tri6` objects with the `Section` rather than deep-copying
   them. Each group still gets its own `StressResult`.
3. `Section.assemble_torsion` gained a `batch` argument and there is a new `Section.assemble_warping`
   that returns the stiffness matrix without the Lagrangian row.
4. A disjoint mesh still warns rather than fails, and now pins one degree of freedom per connected
   region instead of handing a singular system to the solver.
5. `pypardiso`, when installed, is no longer used for the warping solve. See
   `solver.USE_PARDISO_FOR_WARPING`.
6. Blueprints: because a profile now reuses one analysed `Section`, a `SectionProperties` returned by
   `section_properties(warping=False)` may carry warping fields as well if an earlier call asked for
   them. Every value that is computed is unchanged; some fields are simply no longer `None`.
7. Blueprints: `Profile.mesh_creator` is main's `max_thickness**2 / 32`; this branch does not
   change it.
8. Blueprints: with the mesh rule left to main, no section property moves against main. The
   amounts tabulated above are what the `t/4` rule would have moved.

## Reproducing

```bash
# per-stage timings
python benchmarks/profile_heb.py

# assembly / solve / post split, and the scipy-only path
python benchmarks/solver_split.py
python benchmarks/solver_split.py --no-pardiso

# numerical equivalence against a reference captured on master
python benchmarks/verify_properties.py --families HEB --compare benchmarks/results/reference_heb_full.json
python benchmarks/verify_properties.py --families HEA IPE CHS RHS UNP LNP --limit 8 --compare benchmarks/results/reference_broad.json
python benchmarks/verify_stress.py --compare benchmarks/results/stress_master.json

# the evidence behind the solver change
python benchmarks/solver_experiment.py HEB300
python benchmarks/solver_backends.py
python benchmarks/superlu_options.py

# the mesh rule: calibration, what it did to the properties, and to the shear check
python benchmarks/mesh_calibration.py
python benchmarks/mesh_calibration_stress.py
python benchmarks/verify_properties.py --families HEB --report benchmarks/results/reference_heb_full.json
python benchmarks/shear_check_sensitivity.py

# mesh rule against code change, back to back in one process
python benchmarks/headline.py --label branch
```

The `results/` folder holds four references captured on unmodified v3.10.2: `reference_heb_full`
and `reference_broad` at the old flat mesh, `reference_heb_thickness` and
`reference_broad_thickness` at the new one, plus the two stress references. Comparing against the
same-mesh pair isolates the code change; the `--report` mode against the flat-mesh pair measures
the mesh change.

To recapture a reference, check out `master` in the sectionproperties repo and run the same command
with `--output` instead of `--compare`.

## Commits

```
7198f80 perf: use the pinned warping solve for the fibre section export
014d1a8 fix: keep disjoint meshes running with a warning and satisfy the linter
115d8f6 perf: vectorise the stress analysis and stop copying elements into StressPost
596aa7f perf: vectorise centroidal properties and pin the warping dof in place
ab0ba91 perf: solve the warping system without the dense Lagrangian row
5050e4a perf: vectorise section analysis over the whole mesh
```

`ruff check` and `ruff format --check` pass on the whole package.

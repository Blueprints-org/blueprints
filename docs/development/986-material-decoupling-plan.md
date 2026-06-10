# Implementation plan — Issue #986: generic, code-agnostic Concrete/Steel materials

> Branch: `986-generic-material-decoupling`
> Status: design proposal — to be reviewed before coding.

## 1. Problem

`ConcreteMaterial`, `SteelMaterial` and `ReinforcementSteelMaterial` are *config
containers that compute Eurocode formulas inline*. The characteristic values are
derived from an enum strength-class string (`re.search(r"C(\d+)/")`,
`value[1:-1]`, …), so:

- you cannot build an off-standard concrete mix or a non-EN steel alloy directly;
- the discrete strength-class lists and EC formulas are baked into the data type;
- there is no shared material contract — concrete exposes `e_c`/`e_cm`, steel
  `e_modulus`, reinforcement `e_s`, and concrete has no `poisson_ratio` /
  `shear_modulus` at all.

The issue asks us to **separate the material *data* from the *construction logic*.**

## 2. What we learned from prior art

Four reference implementations were studied (see Appendix for detail).

### 2.1 BAM dd-core / dd-concrete / dd-steel — the house pattern (primary target)
- `dd_core.protocols.material.Material` — a `@runtime_checkable` Protocol with the
  *minimal FEA surface*: `name`, `density`, `modulus_of_elasticity`,
  `poisson_ratio`, `shear_modulus`. Material-specific strengths are deliberately
  **not** in the protocol (concrete = scalars, steel = thickness-dependent).
- `Concrete` / `Steel` are `@dataclass(frozen=True)` data containers storing
  pre-computed characteristic values as plain fields.
- All code formulas move into a `@classmethod from_ec2(...)` / `from_en10025(...)`
  factory; only trivial derivations of stored fields stay as `@property`
  (`f_cd = f_ck / material_factor`, `shear_modulus`, …).
- Thickness-dependent steel strengths are modelled as ordered
  `tuple[StrengthRow(max_thickness, strength), ...]` with a generic `_lookup`,
  instead of hardcoded `≤40 / 40–80 / >80` branches.

### 2.2 robbievanleeuwen/section-properties — the FE-minimal data carrier
- `Material` is `@dataclass(eq=True, frozen=True)` → **immutable & hashable** so
  instances can key mesh regions by material.
- Fields: `name, elastic_modulus, poissons_ratio, yield_strength, density, color`;
  `shear_modulus` is a derived `@property` (`E / (2(1+ν))`, isotropy assumed).
- **Minimum to participate in elastic FE = `elastic_modulus` + `poissons_ratio`.**
  `yield_strength` is plastic-only, `density` is mass-only, `name`/`color` are metadata.
- A neutral `DEFAULT_MATERIAL = (E=1, ν=0, σy=1, ρ=1)` makes "no material" and
  "geometric-only" collapse to one code path; `None` is coerced to it.
- Zero design-code content in the material — it is just floats in a user-chosen
  unit system. Any code logic lives in a *separate* layer that *produces* materials.

### 2.3 robbievanleeuwen/concrete-properties — data/behaviour separation via strategy
- `Material` holds `name, density, colour, meshed` plus a composed
  `StressStrainProfile`; `elastic_modulus` is **derived** in `__post_init__` from
  the profile, never stored as an input (single source of truth).
- Constitutive models are separate `StressStrainProfile` objects (strategy
  pattern) reduced to `(strains, stresses)` with a stable API
  (`get_stress(strain)`, `get_elastic_modulus()`, …); analysis never branches on
  model type.
- All code-specific construction lives behind `DesignCode` factory classes
  (`AS3600`, `NZS3101`) with a **one-way dependency**: `design_codes/` imports
  `material`, never the reverse.

### 2.4 Convergent lessons
1. Material = immutable, hashable, code-agnostic **value object**.
2. Define a **minimal shared contract** (`E`, `ν` → `G`; plus `name`, `density`).
3. **Derive, don't store** redundant quantities (`shear_modulus`, `f_cd`).
4. **One-way dependency**: code logic *produces* materials; materials never import code logic.
5. Material-specific strengths stay *off* the shared contract (their shape differs).

## 3. Target design for blueprints

### 3.1 New shared contract — `blueprints/materials/_material.py`
Mirror `dd_core.protocols.material.Material` using blueprints' own
`type_alias` aliases (`MPA`, `KG_M3`, `RATIO`):

```python
@runtime_checkable
class Material(Protocol):
    @property
    def name(self) -> str: ...
    @property
    def density(self) -> KG_M3: ...
    @property
    def modulus_of_elasticity(self) -> MPA: ...
    @property
    def poisson_ratio(self) -> RATIO: ...
    @property
    def shear_modulus(self) -> MPA: ...
```

This both matches the house pattern and is a superset of the section-properties
FE-minimum, so blueprints materials become drop-in compatible with FE/section
tooling later.

### 3.2 Concrete — `blueprints/materials/concrete.py`
Add a `@dataclass(frozen=True) Concrete` data container alongside (initially) the
existing `ConcreteMaterial`:
- **Stored fields** (pre-computed data): `name, f_ck, f_ck_cube, f_cm, f_ctm,
  f_ctk_0_05, f_ctk_0_95, e_cm, density=2500.0, poisson_ratio=0.2,
  material_factor=1.5, eps_c1/cu1/c2/cu2/c3/cu3, n_factor, cement_class,
  cement_type, aggregate_type, aggregate_size, diagram_type,
  plain_concrete_diagram, thermal_coefficient`.
- **Derived `@property`**: `f_cd = f_ck / material_factor`,
  `f_ctd = f_ctk_0_05 / material_factor` (fixes the current hardcoded `/1.5`),
  `f_cm_cube`, `sigma_cr`, `strain_cr`, `modulus_of_elasticity` (→ `e_cm`),
  `shear_modulus`; method `rho_min(f_yd)`.
- **Factory** `@classmethod from_ec2(concrete_class=C30/37, *, name="", e_cm=None,
  …) -> Concrete` carrying the Table-3.1 math currently inlined in the properties.

### 3.3 Steel — `blueprints/materials/steel.py`
Add `@dataclass(frozen=True) StrengthRow(max_thickness, strength)` and
`@dataclass(frozen=True) Steel`:
- Stored: `name, f_y_table: tuple[StrengthRow, ...], f_u_table: tuple[StrengthRow, ...],
  density=7850.0, e_modulus=210000.0, poisson_ratio=0.3,
  thermal_coefficient=1.2e-5, material_factor=1.0`.
- Methods: `f_yk(thickness)`, `f_uk(thickness)`, `f_yd(thickness)`, generic
  `_lookup`; properties `modulus_of_elasticity`, `shear_modulus`, `unit_weight`.
- **Factory** `from_en10025(grade=S355, *, …)` building the tables from the
  existing `Table3Dot1NominalValuesHotRolledStructuralSteel` data (reuse it — do
  not duplicate the strength numbers). This replaces the hardcoded `≤40/40–80`
  branching with `StrengthRow` rows.
- Requires adding `KG_TO_KN` to `blueprints/unit_conversion.py` (currently absent)
  if we port `unit_weight`.

### 3.4 Reinforcement steel — `blueprints/materials/reinforcement_steel.py`
Add a `@dataclass(frozen=True) ReinforcementSteel` container +
`from_ec2(steel_quality, …)` factory. blueprints is *ahead* of the engine here
(it already has `f_yd`/`material_factor`), so this is mostly: lift the string
parsing (`f_yk = float(value[1:-1])`, ductility dicts) into the factory, align the
modulus name (`e_s` → `modulus_of_elasticity`) and add `poisson_ratio`/`shear_modulus`.

## 4. Key decisions to confirm before coding

1. **Factory style — `@classmethod` vs free function.** The issue text prefers
   *external factory functions* (Option B). The house dd-pattern uses a
   `@classmethod from_ec2`. **Recommendation: `@classmethod`** — it keeps the
   factory discoverable from the type, matches dd-concrete/dd-steel, and still
   satisfies every acceptance criterion (the *container* embeds no code logic or
   discrete lists). Flag this in the issue thread; cheap to switch.
2. **Migration vs shims.** Production coupling is small (concrete → `.f_ck`,
   `.concrete_class.value`; steel → `.yield_strength(t)`, `.ultimate_strength(t)`,
   `.density`; reinforcement → `.density`, `.name`). The heavy surface is in
   `tests/materials/`. **Recommendation: land the new containers + factories first
   with the old classes kept as thin deprecated shims, then migrate consumers in
   follow-up PRs** — keeps each PR under the 100%-coverage gate.
3. **Method naming.** New steel uses `f_yk/f_uk/f_yd(thickness)` (house pattern)
   vs current `yield_strength/ultimate_strength(thickness)`. Decide whether to
   alias the old names on the shim for one release.
4. **Stress-strain profiles (concrete-properties model).** Adopting separate
   `StressStrainProfile` strategy objects is a larger change. **Recommendation:
   out of scope for #986** — but keep `diagram_type` as a field so we don't
   *preclude* a later profile-object refactor.
5. **Enum source & language.** blueprints enums are English; dd engines are Dutch.
   Plotters render `concrete_class.value`. Keep blueprints' English enums; do not
   import engine enums.

## 5. Phased work breakdown

- **Phase 0 — scaffolding**: add `Material` Protocol (`_material.py`); add
  `KG_TO_KN` to `unit_conversion.py`. Tests for the protocol + conversion.
- **Phase 1 — Concrete**: add frozen `Concrete` + `from_ec2`; port property tests;
  prove `Concrete.from_ec2(C30/37)` reproduces every value of today's
  `ConcreteMaterial`. 100% coverage.
- **Phase 2 — Steel**: add `StrengthRow` + `Steel` + `from_en10025` reusing
  `table_3_1`; parity tests across thickness bands.
- **Phase 3 — ReinforcementSteel**: add frozen container + `from_ec2`.
- **Phase 4 — consumer migration**: switch `structural_sections`, `checks`,
  `chapter_4_durability_and_cover` to the new types; deprecate old classes.
- **Phase 5 — cleanup**: remove shims (separate release), update docs/examples.

Each phase: `make lint`, `make typecheck`, `make check-coverage` (100% required);
review with the `dd-core-conventions` skill before PR.

## 6. Acceptance-criteria mapping

| Issue AC | Covered by |
|---|---|
| Material contains only physical properties | §3.2/3.3/3.4 stored data fields |
| No Eurocode/Blueprint module dependencies in the container | §3 one-way dependency; formulas live in `from_*` |
| No embedded discrete material lists | strength-class enums consumed only by `from_*` factories |
| Construction via classmethod or external factory | §4.1 `from_ec2` / `from_en10025` |
| Structural calculations depend solely on Material | §3.1 `Material` Protocol contract |
| Existing functionality preserved | §5 parity tests + shim phase |

## Appendix — reference file pointers

- BAM: `engines/dd-core/dd_core/protocols/material.py`;
  `engines/dd-concrete/dd_concrete/material/concrete/concrete.py` (`Concrete`,
  `from_ec2`); `engines/dd-steel/dd_steel/steel/steel_material.py` (`StrengthRow`,
  `Steel`, `from_en10025`).
- section-properties: `src/sectionproperties/pre/pre.py` (`Material`,
  `DEFAULT_MATERIAL`).
- concrete-properties: `src/concreteproperties/material.py`;
  `src/concreteproperties/stress_strain_profile.py`;
  `src/concreteproperties/design_codes/` (`DesignCode`, `AS3600`, `NZS3101`).
- Current blueprints: `blueprints/materials/{concrete,steel,reinforcement_steel}.py`;
  strengths in `blueprints/codes/eurocode/en_1993_1_1_2005/chapter_3_materials/table_3_1.py`;
  aliases in `blueprints/type_alias.py`; constants in `blueprints/unit_conversion.py`.

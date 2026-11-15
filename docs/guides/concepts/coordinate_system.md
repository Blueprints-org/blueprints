# Coordinate System of Section Properties and Stresses

Blueprints uses the coordinate system that is common in structural analysis. The underlying [sectionproperties](https://sectionproperties.readthedocs.io) library uses a different one. To prevent mix-ups, Blueprints wraps the results of `sectionproperties` and **always returns them in the Blueprints coordinate system**. This is the default behaviour: there is nothing to enable.

```
    z (vertical, usually strong axis)
        ↑
        |     x (longitudinal beam direction, into screen)
        |    ↗
        |   /
        |  /
        | /
        |/
    ←-----O
    y (horizontal/side, usually weak axis)
```

| Axis | Blueprints                                  | sectionproperties                      |
|------|---------------------------------------------|----------------------------------------|
| x    | longitudinal beam direction (into screen)   | horizontal, positive to the right      |
| y    | horizontal, **positive to the left**        | vertical, positive upwards             |
| z    | vertical, positive upwards                  | longitudinal beam direction            |

The mapping between both systems is:

```
bp_y = -sp_x
bp_z =  sp_y
bp_x =  sp_z
```

## Section properties

`Profile.section_properties()` returns a [`BPSectionProperties`][blueprints.structural_sections.BPSectionProperties] object. **Every attribute starts with `bp_`**, so a Blueprints value cannot be confused with the identically named, but differently oriented, `sectionproperties` value. For example, `iyy_c` in `sectionproperties` is the second moment of area about the *vertical* axis, whereas `bp_iyy_c` is the second moment of area about the *horizontal* Blueprints y-axis.

Plain scalars that have nothing to do with the axes are identical in both systems. These also work **without** the prefix, so `area` and `bp_area` return the same value: `area`, `perimeter`, `mass`, `ea`, `ga`, `nu_eff`, `e_eff`, `g_eff`, `j`, `gamma` and `delta_s`. The unprefixed names are read-only and `asdict()` only contains the `bp_` names. Everything else, including everything related to an axis (such as `iyy_c`, `zyy_plus`, `cy`, or the principal-axis values `i11_c` and `r11_c`), is only available with the `bp_` prefix.

```python
from blueprints.structural_sections.geometric_profiles import RectangularProfile

profile = RectangularProfile(name="Rectangle", width=100.0, height=200.0)
properties = profile.section_properties()

print(properties.bp_area)  # 20000.0 mm²
print(properties.bp_iyy_c)  # about the horizontal y-axis: 100 * 200³ / 12 = 66666666.7 mm⁴
print(properties.bp_izz_c)  # about the vertical z-axis: 200 * 100³ / 12 = 16666666.7 mm⁴
print(properties.bp_zyy_plus)  # elastic section modulus about y, top fibre (positive z)
print(properties.bp_syy)  # plastic section modulus about y
print(properties.asdict())  # all properties, keyed by their bp_ names
```

Properties that were not calculated (for example the warping properties when `warping=False`) are `None`.

### Naming convention

| Blueprints name                      | sectionproperties name | Remark                                             |
|--------------------------------------|------------------------|----------------------------------------------------|
| `bp_area`, `bp_perimeter`, `bp_j`, … | same without `bp_`     | independent of the orientation, also work without `bp_` |
| `bp_iyy_c`                           | `ixx_c`                | second moment of area about the horizontal axis    |
| `bp_izz_c`                           | `iyy_c`                | second moment of area about the vertical axis      |
| `bp_iyz_c`                           | `ixy_c` (sign flipped) | product moment of area                             |
| `bp_cy`, `bp_cz`                     | `cx` (sign flipped), `cy` | centroid                                        |
| `bp_zyy_plus` / `bp_zyy_minus`       | `zxx_plus` / `zxx_minus` | section modulus, top / bottom fibre              |
| `bp_zzz_plus` / `bp_zzz_minus`       | `zyy_minus` / `zyy_plus` | section modulus, fibre at positive / negative y  |
| `bp_syy`, `bp_szz`                   | `sxx`, `syy`           | plastic section moduli                             |
| `bp_a_sy`, `bp_a_sz`                 | `a_sx`, `a_sy`         | shear areas                                        |

`plus` and `minus` always refer to the fibre at the positive or negative coordinate **in the Blueprints coordinate system**. Because positive y points to the left, the `plus`/`minus` labels of quantities about the z-axis are swapped with respect to `sectionproperties`.

## Stresses

`Profile.calculate_stress(...)` returns a [`BPStressPost`][blueprints.structural_sections.BPStressPost] object. Forces and moments are given in the Blueprints axes (`n`, `v_y`, `v_z` in kN and `m_x`, `m_y`, `m_z` in kNm) and all results are reported in the Blueprints axes as well:

- `get_stress()` returns the stresses per material. Like the section properties, every key starts with `bp_`, for example `bp_sig_xx_n`, `bp_sig_xx_my`, `bp_sig_xx_mz`, `bp_sig_xy_vy`, `bp_sig_xz_vz`, `bp_sig_xyz`, `bp_sig_vm` and `bp_material` (x is the longitudinal direction).
- `plot_stress(stress=...)` takes the Blueprints labels, e.g. `"my_xx"`, `"vz_xyz"` or `"vm"`. `plot_stress_vector(stress=...)` takes `"mx_xyz"`, `"vy_xyz"`, `"vz_xyz"`, `"v_xyz"` or `"xyz"`. Any other label (including `sectionproperties` labels such as `"zz"`) raises a `ValueError`.
- `plot_mohrs_circles(y=..., z=...)` takes a position in Blueprints coordinates.

```python
stress_post = profile.calculate_stress(n=100.0, m_y=50.0)
stress = stress_post.get_stress()[0]
print(stress["bp_sig_xx"].max())  # maximum normal stress in N/mm²
stress_post.plot_stress(stress="xx")
```

!!! note "Plots"
    The plots are Blueprints plots: the contour values, titles (e.g. $\sigma_{xx,My}$) and axis labels (`y`, `z`) are all expressed in the Blueprints coordinate system. The cross-section is drawn as you see it when looking along the beam axis, with positive y to the left, so the tick labels of the horizontal axis increase towards the left.

## Reference

::: blueprints.structural_sections.BPSectionProperties
    options:
      show_source: false
      heading_level: 3

::: blueprints.structural_sections.BPStressPost
    options:
      show_source: false
      heading_level: 3

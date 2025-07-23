---
hide:
    - toc
---
# Steel Profile Shapes

Steel profiles are essential components in structural engineering, and their properties are critical for designing safe and efficient structures. This example demonstrates how to work with various steel profile shapes using `Blueprints`. The library provides predefined standard profiles as well as the ability to define custom profiles.

Follow the steps below to explore the usage of different steel profile shapes (or [go to the full code example](#full-code-example)):

## Define the Steel Class

Start by defining the steel material to be used for the profiles:

```python
--8<-- "examples/_code/steel_profile_shapes.py:20:21"
```

## Circular Hollow Section (CHS) Profiles

### Standard CHS Profile

Structual parameters are automatically calculated and can be obtained with:

```python
--8<-- "examples/_code/steel_profile_shapes.py:23:29"
```

A plot of this profile can be generated using the `plot` method. A show=True makes the plot appear:
```python
---8<-- "examples/_code/steel_profile_shapes.py:31:31"
```
![CHS273x5 with 4mm corrosion](./_images/steel_profile_chs_273_5_corrosion_4.png)

Its properties can be accessed as follows:
```python
---8<-- "examples/_code/steel_profile_shapes.py:32:32"
```
```terminaloutput
Steel class: SteelMaterial(steel_class=<SteelStrengthClass.S355: (<SteelStandardGroup.EN_10025_2: 'NEN-EN 10025-2'>, 'S 355')>, density=7850.0, diagram_type=<DiagramType.BI_LINEAR: 'Bi-Linear'>, quality_class=None, custom_name=None, custom_e_modulus=None, custom_poisson_ratio=None, custom_thermal_coefficient=None, custom_yield_strength=None, custom_ultimate_strength=None)
Moment of inertia about y-axis: 7225666.244849178 mm⁴
Moment of inertia about z-axis: 7225666.244849178 mm⁴
Elastic section modulus about y-axis: 54533.330149803856 mm³
Elastic section modulus about z-axis: 54533.330149805726 mm³
Area: 829.2971942462827 mm²
All section properties: SectionProperties(area=np.float64(829.2971942461268), perimeter=832.5011573032386, mass=np.float64(829.2971942461268), ea=np.float64(829.2971942461268), ga=np.float64(414.6485971230634), nu_eff=np.float64(0.0), e_eff=np.float64(1.0), g_eff=np.float64(0.5), qx=np.float64(4.3074166455880913e-10), qy=np.float64(-3.233822098991368e-10), ixx_g=np.float64(7224215.4793896265), iyy_g=np.float64(7224215.479389725), ixy_g=np.float64(4.0245140553452075e-09), cx=np.float64(-3.8994730977367847e-13), cy=np.float64(5.194056697012886e-13), ixx_c=np.float64(7224215.4793896265), iyy_c=np.float64(7224215.479389725), ixy_c=np.float64(4.024514055345375e-09), zxx_plus=np.float64(54522.380976525696), zxx_minus=np.float64(54522.38097652527), zyy_plus=np.float64(54522.38097652607), zyy_minus=np.float64(54522.380976526394), rx_c=np.float64(93.33407929017395), ry_c=np.float64(93.3340792901746), i11_c=np.float64(7224215.479389725), i22_c=np.float64(7224215.4793896265), phi=0.0, z11_plus=np.float64(54522.38097652644), z11_minus=np.float64(54522.380976526016), z22_plus=np.float64(54522.38097652532), z22_minus=np.float64(54522.380976525645), r11_c=np.float64(93.3340792901746), r22_c=np.float64(93.33407929017395), j=np.float64(14448167.595345043), my_xx=np.float64(54522.38097652528), my_yy=np.float64(54522.38097652607), my_11=np.float64(54522.380976526016), my_22=np.float64(54522.38097652532), omega=array([ 2.04760733e-10,  2.07633017e-10,  1.02287231e-10, ...,
       -1.26543947e-10,  2.88707706e-01, -2.88707706e-01], shape=(3072,)), psi_shear=array([3.32165264e+13, 3.31865108e+13, 3.31365048e+13, ...,
       3.19117738e+13, 3.19678036e+13, 3.18545452e+13], shape=(3072,)), phi_shear=array([-8.15419953e+11, -1.63034873e+12, -2.44429544e+12, ...,
        9.25424290e+12,  9.05879232e+12,  9.44934585e+12], shape=(3072,)), delta_s=np.float64(104378578585306.81), x_se=np.float64(-4.287278156736595e-13), y_se=np.float64(1.5268937569383123e-13), x11_se=np.float64(-4.287278156736595e-13), y22_se=np.float64(1.5268937569383123e-13), x_st=np.float64(-4.438877969720056e-13), y_st=np.float64(1.3230599407707244e-13), gamma=np.float64(10.205573098603223), a_sx=np.float64(414.6509511553843), a_sy=np.float64(414.650951156514), a_sxy=np.float64(-2.2009910751450052e+16), a_s11=np.float64(414.6509511553843), a_s22=np.float64(414.650951156514), beta_x_plus=np.float64(1.528218837860486e-12), beta_x_minus=np.float64(-1.528218837860486e-12), beta_y_plus=np.float64(-1.6028524348880673e-12), beta_y_minus=np.float64(1.6028524348880673e-12), beta_11_plus=np.float64(1.5282188378604693e-12), beta_11_minus=np.float64(-1.5282188378604693e-12), beta_22_plus=np.float64(-1.6028524348880776e-12), beta_22_minus=np.float64(1.6028524348880776e-12), x_pc=9.947598300641403e-13, y_pc=-1.9895196601282805e-12, x11_pc=9.947598300641403e-13, y22_pc=-1.9895196601282805e-12, sxx=69685.83771705313, syy=69685.83771705022, sf_xx_plus=np.float64(1.278114353572636), sf_xx_minus=np.float64(1.278114353572646), sf_yy_plus=np.float64(1.278114353572574), sf_yy_minus=np.float64(1.2781143535725663), s11=np.float64(69685.83771705313), s22=np.float64(69685.83771705022), sf_11_plus=np.float64(1.2781143535726187), sf_11_minus=np.float64(1.2781143535726287), sf_22_plus=np.float64(1.2781143535725916), sf_22_minus=np.float64(1.2781143535725839))
```


### Custom CHS Profile

Alternatively, define a custom CHS profile by specifying its dimensions:

```python
--8<-- "examples/_code/steel_profile_shapes.py:34:39"
```

A plot of this custom profile can be generated using the `plot` method. A show=True makes the plot appear:
```python
---8<-- "examples/_code/steel_profile_shapes.py:41:41"
```
![Custom CHS Profile](./_images/steel_profile_custom_chs.png)

Its properties can be accessed as follows:
```python
---8<-- "examples/_code/steel_profile_shapes.py:42:42"
```
```terminaloutput
All section properties of custom CHS profile: SectionProperties(area=np.float64(4397.788151305911), perimeter=471.2270701716454, mass=np.float64(4397.788151305911), ea=np.float64(4397.788151305911), ga=np.float64(2198.8940756529555), nu_eff=np.float64(0.0), e_eff=np.float64(1.0), g_eff=np.float64(0.5), qx=np.float64(-4.3075942812720314e-10), qy=np.float64(-2.837632351315733e-10), ixx_g=np.float64(10828466.102927726), iyy_g=np.float64(10828466.10292771), ixy_g=np.float64(-2.5585791263438296e-09), cx=np.float64(-6.452408014408574e-14), cy=np.float64(-9.79491083487708e-14), ixx_c=np.float64(10828466.102927726), iyy_c=np.float64(10828466.10292771), ixy_c=np.float64(-2.5585791263438573e-09), zxx_plus=np.float64(144379.54803903616), zxx_minus=np.float64(144379.54803903654), zyy_plus=np.float64(144379.54803903602), zyy_minus=np.float64(144379.54803903628), rx_c=np.float64(49.621092091432914), ry_c=np.float64(49.621092091432885), i11_c=np.float64(10828466.102927726), i22_c=np.float64(10828466.10292771), phi=0.0, z11_plus=np.float64(144379.54803903616), z11_minus=np.float64(144379.54803903654), z22_plus=np.float64(144379.54803903602), z22_minus=np.float64(144379.54803903628), r11_c=np.float64(49.621092091432914), r22_c=np.float64(49.621092091432885), j=np.float64(21656932.205855437), my_xx=np.float64(144379.54803903613), my_yy=np.float64(144379.54803903602), my_11=np.float64(144379.54803903613), my_22=np.float64(144379.54803903602), omega=array([-1.16366227e-11, -2.61335265e-11, -1.27721256e-11, ...,
        2.31547037e-11, -1.47929815e-11, -1.48006859e-12], shape=(7344,)), psi_shear=array([ 7.42767796e+12,  7.42096832e+12,  7.40978515e+12, ...,
       -3.87534772e+12, -2.06937744e+12, -7.42857993e+12], shape=(7344,)), phi_shear=array([-1.82340107e+11, -3.64567906e+11, -5.46578754e+11, ...,
       -6.33666689e+12, -7.13591715e+12,  9.24234081e+10], shape=(7344,)), delta_s=np.float64(234511356284509.22), x_se=np.float64(-9.174268640419628e-14), y_se=np.float64(-3.276676183509186e-14), x11_se=np.float64(-9.174268640419628e-14), y22_se=np.float64(-3.276676183509186e-14), x_st=np.float64(-9.174268640419806e-14), y_st=np.float64(-3.2766761835045005e-14), gamma=np.float64(1.3814656236624803e-18), a_sx=np.float64(2217.559969536245), a_sy=np.float64(2217.559969250143), a_sxy=np.float64(77085614657103.05), a_s11=np.float64(2217.559969536245), a_s22=np.float64(2217.559969250143), beta_x_plus=np.float64(-2.569740856175257e-13), beta_x_minus=np.float64(2.569740856175257e-13), beta_y_plus=np.float64(-2.923845281775058e-13), beta_y_minus=np.float64(2.923845281775058e-13), beta_11_plus=np.float64(-2.569740856175257e-13), beta_11_minus=np.float64(2.569740856175257e-13), beta_22_plus=np.float64(-2.923845281775058e-13), beta_22_minus=np.float64(2.923845281775058e-13), x_pc=0.0, y_pc=0.0, x11_pc=0.0, y22_pc=0.0, sxx=196303.7673686788, syy=196303.7673686782, sf_xx_plus=np.float64(1.3596369432850959), sf_xx_minus=np.float64(1.3596369432850923), sf_yy_plus=np.float64(1.3596369432850932), sf_yy_minus=np.float64(1.3596369432850908), s11=np.float64(196303.7673686788), s22=np.float64(196303.7673686782), sf_11_plus=np.float64(1.3596369432850959), sf_11_minus=np.float64(1.3596369432850923), sf_22_plus=np.float64(1.3596369432850932), sf_22_minus=np.float64(1.3596369432850908))
```

## Strip Profiles

### Standard Strip Profile

Predefined strip profiles are also available:

```python
--8<-- "examples/_code/steel_profile_shapes.py:44:49"
```

A plot of this profile can be generated using the `plot` method. A show=True makes the plot appear:
```python
---8<-- "examples/_code/steel_profile_shapes.py:51:51"
```

![Standard Strip Profile](./_images/steel_profile_strip_160_5_corrosion_1.png)

Its properties can be accessed as follows:
```python
---8<-- "examples/_code/steel_profile_shapes.py:52:52"
```

### Custom Strip Profile

Define a custom strip profile by specifying its width and height:

```python
--8<-- "examples/_code/steel_profile_shapes.py:54:59"
```

A plot of this custom profile can be generated using the `plot` method. A show=True makes the plot appear:
```python
---8<-- "examples/_code/steel_profile_shapes.py:61:61"
```

![Custom Strip Profile](./_images/steel_profile_custom_strip.png)

Its properties can be accessed as follows:
```python
---8<-- "examples/_code/steel_profile_shapes.py:62:62"
```

## I Profiles (IPE, HEA, HEB, etc.)

### Standard I Profile

Predefined I profiles are also available:

```python
--8<-- "examples/_code/steel_profile_shapes.py:64:69"
```

A plot of this profile can be generated using the `plot` method. A show=True makes the plot appear:
```python
---8<-- "examples/_code/steel_profile_shapes.py:71:71"
```
![Standard I Profile](./_images/steel_profile_heb600_corrosion_7.png)

Its properties can be accessed as follows:
```python
---8<-- "examples/_code/steel_profile_shapes.py:72:72"
```

It you desire to use a different standard profile, you can change the `profile_name` parameter in the `IProfile` constructor.
There are many standard profiles available, such as `IPE`, `HEA`, `HEB`, `HEM`, etc. to be used as the `profile_name`.
Check all available profiles in this package: `blueprints.structural_sections.steel.steel_cross_sections.standard_profiles`.

### Custom I Profile

Define a custom I profile by specifying its width and height:

```python
--8<-- "examples/_code/steel_profile_shapes.py:74:85"
```

A plot of this custom profile can be generated using the `plot` method. A show=True makes the plot appear:
```python
---8<-- "examples/_code/steel_profile_shapes.py:87:87"
```

![Custom I Profile](./_images/steel_profile_custom_i_profile.png)

Its properties can be accessed as follows:
```python
---8<-- "examples/_code/steel_profile_shapes.py:88:88"
```

## Rectangular Hollow Profiles (RHS, SHS, RHSCF, SHSCF)

### Standard RHS Profile

Predefined RHS profiles are also available:

```python
--8<-- "examples/_code/steel_profile_shapes.py:90:96"
```

A plot of this profile can be generated using the `plot` method. A show=True makes the plot appear:
```python
---8<-- "examples/_code/steel_profile_shapes.py:98:98"
```
![Standard I Profile](./_images/steel_profile_rhs_400x200x16_corrosion_0.png)

Its properties can be accessed as follows:
```python
---8<-- "examples/_code/steel_profile_shapes.py:99:99"
```

It you desire to use a different standard profile, you can change the `profile_name` parameter in the `IProfile` constructor.
There are many standard profiles available, such as `SHS`, `RHS`, `SHSCF`, `RHSCF`, etc. to be used as the `profile_name`.
Check all available profiles in this package: `blueprints.structural_sections.steel.steel_cross_sections.standard_profiles`.

### Custom RHS Profile

Define a custom RHS profile by specifying its width and height:

```python
--8<-- "examples/_code/steel_profile_shapes.py:101:118"
```

A plot of this custom profile can be generated using the `plot` method. A show=True makes the plot appear:
```python
---8<-- "examples/_code/steel_profile_shapes.py:120:120"
```

![Custom RHS Profile](./_images/steel_profile_custom_rhs.png)

Its properties can be accessed as follows:
```python
---8<-- "examples/_code/steel_profile_shapes.py:121:121"
```

<a name="full-code-example">
## Full Code Example

```python
--8<-- "examples/_code/steel_profile_shapes.py"
```
</a>
---
hide:
    - toc
---
# Steel Profile Shapes

Steel profiles are essential components in structural engineering, and their properties are critical for designing safe and efficient structures. This example demonstrates how to work with various steel profile shapes using `Blueprints`. The library provides predefined standard profiles as well as the ability to define custom profiles.

Follow the steps below to explore the usage of different steel profile shapes (or [go to the full code example](#full-code-example)):

## Define the Steel Class

Start by importing the needed elements and defining the steel material to be used for the profiles:

```python
--8<-- "examples/_code/steel_profile_shapes/i_profile.py:12:13"
```

## I Profiles (IPE, HEA, HEB, etc.)

### Standard I Profile

Predefined I profiles are also available:

```python
--8<-- "examples/_code/steel_profile_shapes/i_profile.py:15:20"
```

A plot of this profile can be generated using the `plot` method. A show=True makes the plot appear:
```python
---8<-- "examples/_code/steel_profile_shapes/i_profile.py:22:22"
```
![Standard I Profile](./_images/steel_profile_shapes/steel_profile_heb600_corrosion_7.png)

Its properties can be accessed as follows:
```python
---8<-- "examples/_code/steel_profile_shapes/i_profile.py:23:23"
```

It you desire to use a different standard profile, you can change the `profile_name` parameter in the `IProfile` constructor.
There are many standard profiles available, such as `IPE`, `HEA`, `HEB`, `HEM`, etc. to be used as the `profile_name`.
Check all available profiles in this package: `blueprints.structural_sections.steel.steel_cross_sections.standard_profiles`.

### Custom I Profile

Define a custom I profile by specifying its width and height:

```python
--8<-- "examples/_code/steel_profile_shapes/i_profile.py:25:36"
```

A plot of this custom profile can be generated using the `plot` method. A show=True makes the plot appear:
```python
---8<-- "examples/_code/steel_profile_shapes/i_profile.py:38:38"
```

![Custom I Profile](./_images/steel_profile_shapes/steel_profile_custom_i_profile.png)

Its properties can be accessed as follows:
```python
---8<-- "examples/_code/steel_profile_shapes/i_profile.py:39:39"
```

<a name="full-code-example">
## Full Code Example

```python
--8<-- "examples/_code/steel_profile_shapes/i_profile.py"
```
</a>
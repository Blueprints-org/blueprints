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
--8<-- "examples/_code/steel_profile_shapes/strip_profile.py:12:13"
```

## Strip Profiles

### Standard Strip Profile

Predefined strip profiles are also available:

```python
--8<-- "examples/_code/steel_profile_shapes/strip_profile.py:15:20"
```

A plot of this profile can be generated using the `plot` method. A show=True makes the plot appear:
```python
---8<-- "examples/_code/steel_profile_shapes/strip_profile.py:22:22"
```

![Standard Strip Profile](./_images/steel_profile_shapes/steel_profile_strip_160_5_corrosion_1.png)

Its properties can be accessed as follows:
```python
---8<-- "examples/_code/steel_profile_shapes/strip_profile.py:23:23"
```

### Custom Strip Profile

Define a custom strip profile by specifying its width and height:

```python
--8<-- "examples/_code/steel_profile_shapes/strip_profile.py:25:30"
```

A plot of this custom profile can be generated using the `plot` method. A show=True makes the plot appear:
```python
---8<-- "examples/_code/steel_profile_shapes/strip_profile.py:32:32"
```

![Custom Strip Profile](./_images/steel_profile_shapes/steel_profile_custom_strip.png)

Its properties can be accessed as follows:
```python
---8<-- "examples/_code/steel_profile_shapes/strip_profile.py:33:33"
```

<a name="full-code-example">
## Full Code Example

```python
--8<-- "examples/_code/steel_profile_shapes/strip_profile.py"
```
</a>
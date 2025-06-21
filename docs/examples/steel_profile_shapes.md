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
--8<-- "examples/_code/steel_profile_shapes.py:23:36"
```

### Custom CHS Profile

Alternatively, define a custom CHS profile by specifying its dimensions:

```python
--8<-- "examples/_code/steel_profile_shapes.py:38:44"
```

## Strip Profiles

### Standard Strip Profile

Predefined strip profiles are also available:

```python
--8<-- "examples/_code/steel_profile_shapes.py:46:52"
```

### Custom Strip Profile

Define a custom strip profile by specifying its width and height:

```python
--8<-- "examples/_code/steel_profile_shapes.py:54:60"
```

## Strip Profiles

### Standard I Profile

Predefined I profiles are also available:

```python
--8<-- "examples/_code/steel_profile_shapes.py:62:68"
```

### Custom I Profile

Define a custom I profile by specifying its width, height, thickness and radii:

```python
--8<-- "examples/_code/steel_profile_shapes.py:70:82"
```

### Standard RHS/SHS/RHSCF/SHSCF Profile

Predefined RHS/SHS/RHSCF/SHSCF profiles are also available:

```python
--8<-- "examples/_code/steel_profile_shapes.py:84:91"
```

### Custom RHS/SHS/RHSCF/SHSCF Profile

Define a custom RHS/SHS/RHSCF/SHSCF profile by specifying its width, height, thickness and radii:

```python
--8<-- "examples/_code/steel_profile_shapes.py:93:111"
```

## Visualizing Profiles

For each profile, the `plot` method is used to visualize the shape. The plots will display the geometry of the profiles, making it easier to understand their dimensions and configurations.

<a name="full-code-example">
## Full Code Example

```python
--8<-- "examples/_code/steel_profile_shapes.py"
```
</a>
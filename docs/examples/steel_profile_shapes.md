---
hide:
    - toc
---
# Steel Profile Shapes

Steel profiles are essential components in structural engineering, and their properties are critical for designing safe and efficient structures. This example demonstrates how to work with various steel profile shapes using `Blueprints`. The library provides predefined standard profiles as well as the ability to define custom profiles.

Follow the steps below to explore the usage of different steel profile shapes (or [go to the full code example](#full-code-example)):

## Define the Steel Class

Start by defining the steel class to be used for the profiles:

```python
--8<-- "examples/_code/steel_profile_shapes.py:17:18"
```

## Circular Hollow Section (CHS) Profiles

### Standard CHS Profile

Structual parameters are automatically calculated and can be obtained with:

```python
--8<-- "examples/_code/steel_profile_shapes.py:20:28"
```

### Custom CHS Profile

Alternatively, define a custom CHS profile by specifying its dimensions:

```python
--8<-- "examples/_code/steel_profile_shapes.py:30:32"
```

## Rectangular Hollow Section (RHS) Profiles

### Standard RHS Profile

Predefined RHS profiles are available for use:

```python
--8<-- "examples/_code/steel_profile_shapes.py:34:36"
```

### Custom RHS Profile

Define a custom RHS profile by specifying its height, width, and thickness:

```python
--8<-- "examples/_code/steel_profile_shapes.py:38:40"
```

## I-Section Profiles (HEB)

### Standard I-Profile

Use predefined I-profiles such as HEB profiles:

```python
--8<-- "examples/_code/steel_profile_shapes.py:42:44"
```

### Custom I-Profile

Define a custom I-profile by specifying its flange and web dimensions:

```python
--8<-- "examples/_code/steel_profile_shapes.py:46:58"
```

## Strip Profiles

### Standard Strip Profile

Predefined strip profiles are also available:

```python
--8<-- "examples/_code/steel_profile_shapes.py:60:62"
```

### Custom Strip Profile

Define a custom strip profile by specifying its width and height:

```python
--8<-- "examples/_code/steel_profile_shapes.py:64:70"
```

## Visualizing Profiles

For each profile, the `plot` method is used to visualize the shape. The plots will display the geometry of the profiles, making it easier to understand their dimensions and configurations.

<a name="full-code-example">
## Full Code Example

```python
--8<-- "examples/_code/steel_profile_shapes.py"
```
</a>
# Installation

## Requirements

Blueprints requires **Python 3.12 or higher**.

Before installing, ensure you have a compatible Python version:

```bash
python --version
```

## Basic Installation

!!! warning "Package Name"
    The package is installed as **`blue-prints`** (with a dash), but you import it as **`blueprints`** (without a dash) in your Python code.

### Installing the Latest Release

To install the latest stable release from PyPI:

=== "pip"
    ```bash
    pip install blue-prints
    ```

=== "uv"
    ```bash
    uv add blue-prints
    ```

### Installing a Specific Version

To install a specific version of Blueprints:

=== "pip"
    ```bash
    pip install blue-prints==0.5.2
    ```

=== "uv"
    ```bash
    uv add blue-prints==0.5.2
    ```

!!! tip
    You can find all available versions on the [PyPI releases page](https://pypi.org/project/blue-prints/#history) or [GitHub releases](https://github.com/Blueprints-org/blueprints/releases).

### Installing the Development Version

To install the actively developed version directly from GitHub:

=== "pip"
    ```bash
    pip install git+https://github.com/Blueprints-org/blueprints.git
    ```

=== "uv"
    ```bash
    uv add git+https://github.com/Blueprints-org/blueprints.git
    ```

## Verifying Installation

After installation, verify that Blueprints is correctly installed:

```python
import blueprints
print(blueprints.__version__)
```

## Core Dependencies

Blueprints automatically installs the following required dependencies:

- **matplotlib** - For plotting and visualization
- **numpy** - For numerical computations
- **sectionproperties** - For cross-section analysis
- **shapely** - For geometric operations

These dependencies are installed automatically and are required for the core functionality of Blueprints.

## Troubleshooting

### Python Version Issues

If you encounter errors related to Python version, ensure you're using Python 3.12 or higher:

```bash
python --version
```

## Next Steps

Now that you have Blueprints installed, you can:

- Check out the [Quick Start Guide](quick_start.md) to begin using Blueprints
- Explore the [API Reference](../API reference/) for detailed documentation
- Browse [Examples](../guides/examples/) to see Blueprints in action

## Getting Help

If you encounter any installation issues:

- Check the [GitHub Issues](https://github.com/Blueprints-org/blueprints/issues) page
- Join our [Discord community](https://discord.gg/hBZBqegEzA) for support
- Review the [changelog](https://github.com/Blueprints-org/blueprints/releases) for version-specific information
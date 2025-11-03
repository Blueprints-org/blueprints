[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/company/blueprints-org)
[![Run Tests](https://github.com/Blueprints-org/blueprints/actions/workflows/test.yaml/badge.svg)](https://github.com/Blueprints-org/blueprints/actions/workflows/test.yaml)
[![Read the Docs](https://img.shields.io/readthedocs/blueprints?logo=readthedocs&label=Read%20the%20docs&link=https%3A%2F%2Fblueprints.readthedocs.io%2Fen%2Flatest%2F)](https://blueprints.readthedocs.io/en/latest/)
[![codecov](https://codecov.io/gh/Blueprints-org/blueprints/branch/main/graph/badge.svg?token=vwYQBShr9q)](https://codecov.io/gh/Blueprints-org/blueprints)
[![PyPI](https://img.shields.io/pypi/v/blue-prints?color=green)](https://pypi.org/project/blue-prints/)
[![GitHub](https://img.shields.io/github/license/Blueprints-org/blueprints?color=green)](https://github.com/Blueprints-org/blueprints/blob/main/LICENSE)
[![Python versions](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue?style=flat&logo=python)](https://badge.fury.io/py/blueprints)


<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/_overrides/assets/images/blueprints_banner.png">
  <source media="(prefers-color-scheme: light)" srcset="docs/_overrides/assets/images/blueprints_banner.png">
  <img alt="blueprints banner" src="docs/_overrides/assets/images/blueprints_banner.png">
</picture>

---

**Documentation**: <a href="https://blueprints.readthedocs.io" target="_blank">https://blueprints.readthedocs.io</a>

**Source Code**: <a href="https://github.com/Blueprints-org/blueprints" target="_blank">https://github.com/Blueprints-org/blueprints</a>

**LinkedIn**: <a href="https://www.linkedin.com/company/blueprints-org" target="_blank">https://www.linkedin.com/company/blueprints-org</a>

---

Welcome to `Blueprints`, the go-to repository for civil engineering professionals and enthusiasts!

It includes programmable engineering standards, formulas, tables, and checks across a variety of structural and geotechnical disciplines. We offer 
tools for materials, geometry, and section checks, as well as a foundation of essential use cases designed to meet all key engineering needs.

Blueprints is a collaborative effort between several engineering companies to streamline code, documentation, and knowledge sharing—helping you focus on the work that matters most.

Stop coding civil engineering logic from scratch, ditch Excel, and start collaborating to shape the future of civil engineering! 🚀

See our [ROADMAP](https://blueprints.readthedocs.io/en/latest/roadmap) for detailed feature status and upcoming developments.

## Installation

Python >=3.12 is required.

For the last release:

```shell
pip install blue-prints
```

For the actively developed version:

```shell
pip install git+https://github.com/Blueprints-org/blueprints.git
```

## Quick Start

```python
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality

# Calculate concrete properties
concrete = ConcreteMaterial(concrete_class=ConcreteStrengthClass.C30_37)  # C30/37 concrete
print(f"Design strength: {concrete.f_cd} MPa")

# Check reinforcement
rebar = ReinforcementSteelMaterial(steel_quality=ReinforcementSteelQuality.B500B)  # B500B rebar
print(f"Design yield strength: {rebar.f_yd} MPa")
```

Output:
```
Design strength: 20.0 MPa
Design yield strength: 434.7826086956522 MPa
```

## Key Features

- **Eurocode Implementations**: EN 1992 (Concrete), EN 1993 (Steel), EN 1997 (Geotechnical), etc.
- **Material Definitions**: Concrete, steel, rebar, and soil properties
- **Steel Profile Database**: HEA, HEB, IPE, CHS, RHS, UNP profiles, etc.
- **Shape Building Blocks**: Rectangle, circle, tube, triangle, hexagon, etc.
- **Engineering Checks**: Shear, torsion, punching, anchorage, concrete cover, etc.
- **100% Test Coverage**: Reliable, well-tested implementations

## Mission

Our mission is to reduce the cost and time associated with civil engineering calculations by:

- Offering a robust suite of tools that encapsulate both basic and advanced engineering tasks
- Providing an open-source alternative to expensive proprietary tools with full transparency
- Standardizing programmable civil engineering implementations, minimizing redundancy
- Fostering a community where sharing knowledge and best practices is the norm
- Ensuring 100% code coverage and high-quality documentation

## Documentation

Full documentation is available at [blueprints.readthedocs.io](https://blueprints.readthedocs.io/en/latest/).

## How to Contribute

We welcome contributions from developers and engineers of all skill levels! Here's how you can contribute:

- Fork the Repository: Create your own fork of the project.
- Create a Branch: Make a feature branch (git checkout -b feature/new-feature).
- Make Your Changes: Write clear, concise code and ensure it's fully covered with tests.
- Run Tests: Use pytest to ensure all tests pass.
- Submit a Pull Request: Push your branch and open a pull request against main.

To learn more, see our full [Contributor Guide](https://blueprints.readthedocs.io/en/latest/contribute).

## License

Blueprints is free and open source software. Distributed under the terms of the [MIT license](LICENSE).

## Support

If you have found a bug 🐛, or have a feature request ✨, raise an issue on the
GitHub [issue tracker](https://github.com/Blueprints-org/blueprints/issues).
Alternatively you can get support on the [discussions](https://github.com/orgs/Blueprints-org/discussions) page.

## Disclaimer

Users are responsible for verifying results and ensuring compliance with applicable codes and regulations. See our full [disclaimer](DISCLAIMER.md) for details.

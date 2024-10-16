[![Run Tests](https://github.com/Blueprints-org/blueprints/actions/workflows/test.yaml/badge.svg)](https://github.com/Blueprints-org/blueprints/actions/workflows/test.yaml)
[![Read the Docs](https://img.shields.io/readthedocs/blueprints?logo=readthedocs&label=Read%20the%20docs&link=https%3A%2F%2Fblueprints.readthedocs.io%2Fen%2Flatest%2F)](https://blueprints.readthedocs.io/en/latest/)
[![codecov](https://codecov.io/gh/Blueprints-org/blueprints/branch/main/graph/badge.svg?token=vwYQBShr9q)](https://codecov.io/gh/Blueprints-org/blueprints)
[![PyPI](https://img.shields.io/pypi/v/blue-prints?color=green)](https://pypi.org/project/blue-prints/)
[![GitHub](https://img.shields.io/github/license/Blueprints-org/blueprints?color=green)](https://github.com/Blueprints-org/blueprints/blob/main/LICENSE)
[![Python versions](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue?style=flat&logo=python)](https://badge.fury.io/py/blueprints)



<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/source/_static/blueprints_banner.png">
  <source media="(prefers-color-scheme: light)" srcset="docs/source/_static/blueprints_banner.png">
  <img alt="blueprints banner" src="docs/source/_static/blueprints_banner.png">
</picture>

Welcome to `Blueprints`, the go-to repository for civil engineering professionals and enthusiasts!

It includes programmable engineering standards, formulas, tables, and checks across a variety of structural and geotechnical disciplines. We offer 
tools for materials, geometry, and section checks, as well as a foundation of essential use cases designed to meet all key engineering needs.

Blueprints is a collaborative effort between several engineering companies to streamline code, documentation, and knowledge sharing—helping you focus on the work that matters most.

Blueprints is more than just a tool, it's a growing community of engineers working together to solve real-world challenges. We believe that by 
sharing knowledge and collaborating, we can eliminate inefficiencies like re-inventing the wheel or relying on cumbersome tools like Excel for complex calculations.

Join us in this effort to build a future where engineering standards are programmable, accessible, and shared. Whether you're an industry expert or a curious enthusiast, your contributions can help drive innovation and reduce the technical overhead we all face.

Stop coding civil engineering logic from scratch, ditch Excel, and start collaborating to shape the future of civil engineering! 🚀

## Mission

Our mission is to reduce the cost and time associated with civil engineering calculations by:

- Offering a robust suite of tools that encapsulate both basic and advanced engineering tasks.
- Providing an open-source alternative to expensive proprietary tools, with a high level of accuracy and full transparency.
- Standardizing programmable civil engineering implementations, minimizing redundancy and eliminating knowledge silos.
- Fostering a community where sharing knowledge and best practices is the norm, not the exception.
- Ensuring 100% code coverage and high-quality documentation for a seamless user experience.

## (Upcoming) Features

* Eurocode formulas:
  * NEN-EN 1992-1-1+C2:2011 :construction:
  * NEN-EN 1993-1-1+C2+A1:2016 :construction:
  * NEN-EN 1993-1-9+C2:2012 :construction:
  * NEN-EN 1993-5:2008 :construction:        
  * NEN 9997-1+C2:2017 :construction:

* Reinforced Concrete Section :construction:
    * Rectangular section :heavy_check_mark:
    * Circular section :x:

* Strain-stress analysis for reinforced concrete sections:
  * Rectangular section :construction:
  * Circular section :x:

* Concrete checks:
  * Nominal concrete cover (NEN-EN 1992-1-1: Chapter 4) :construction:

* Common calculations:
  * L-walls :x:
  * Spring constants calculations for piles :x:
  * Sheet-pile checks (strength, stability, deflection, local buckling, etc.) :x:

## Installation

For the last release:

```shell
pip install blue-prints
```

For the actively developed version:

```shell
pip install git+https://github.com/Blueprints-org/blueprints.git
```

## Read the docs!

Documentation is available at [blueprints.readthedocs.io](https://blueprints.readthedocs.io/en/latest/).

## Quick Reference to Blueprint's Objects

This table serves as a quick navigator to the key elements of the code within Blueprints, offering immediate links to its formulas, tables, and
figures for streamlined access and reference.

| Document                   | Description                                                                                 |                            Formulas                             |                            Tables                             |                            Figures                             |
|:---------------------------|:--------------------------------------------------------------------------------------------|:---------------------------------------------------------------:|:-------------------------------------------------------------:|:--------------------------------------------------------------:|
| NEN-EN 1992-1-1+C2:2011    | Eurocode 2: Design of concrete structures – Part 1-1: General rules and rules for buildings ([code](blueprints/codes/eurocode/nen_en_1992_1_1_c2_2011)) | [304](docs/source/codes/eurocode/ec2_1992_1_1_2011/formulas.md) | [38](docs/source/codes/eurocode/ec2_1992_1_1_2011/tables.md)  | [104](docs/source/codes/eurocode/ec2_1992_1_1_2011/figures.md) |
| NEN-EN 1993-1-1+C2+A1:2016 | Eurocode 3: Design of steel structures – Part 1-1: General rules and rules for buildings ([code](blueprints/codes/eurocode/nen_en_1993_1_1_c2_a1_2016))    | [108](docs/source/codes/eurocode/ec3_1993_1_1_2016/formulas.md) | [20](docs/source/codes/eurocode/ec3_1993_1_1_2016/tables.md)  | [28](docs/source/codes/eurocode/ec3_1993_1_1_2016/figures.md)  |
| NEN 9997-1+C2:2017         | Eurocode 7: Geotechnical design of structures - Part 1: General rules ([code](blueprints/codes/eurocode/nen_9997_1_c2_2017))                      | [88](docs/source/codes/eurocode/nen_9997_1_c2_2017/formulas.md) | [11](docs/source/codes/eurocode/nen_9997_1_c2_2017/tables.md) | [25](docs/source/codes/eurocode/nen_9997_1_c2_2017/figures.md) |
| NEN-EN 1993-5:2008         | Eurocode 3: Design of steel structures – Part 5: Piling ([code](blueprints/codes/eurocode/nen_en_1993_5_2008))                                    | [63](docs/source/codes/eurocode/nen_en_1993_5_2008/formulas.md) | [0](docs/source/codes/eurocode/nen_en_1993_5_2008/tables.md)  | [0](docs/source/codes/eurocode/nen_en_1993_5_2008/figures.md)  |

## Contributing

We welcome contributions from developers and engineers of all skill levels! Here’s how you can contribute:

- Fork the Repository: Create your own fork of the project.
- Create a Branch: Make a feature branch (git checkout -b feature/new-feature).
- Make Your Changes: Write clear, concise code and ensure it’s fully covered with tests.
- Run Tests: Use pytest to ensure all tests pass.
- Submit a Pull Request: Push your branch and open a pull request against main.

To learn more, see the [Contributor Guide](CONTRIBUTING.md).

## License

Blueprints is free and open source software. Distributed under the terms of the [LGPL-2.1 license](LICENSE).

## Support

If you have found a bug 🐛, or have a feature request ✨, raise an issue on the
GitHub [issue tracker](https://github.com/Blueprints-org/blueprints/issues).
Alternatively you can get support on the [discussions](https://github.com/orgs/Blueprints-org/discussions) page.

## Disclaimer

Blueprints is an open source engineering tool that continues to benefit from the collaboration of many contributors. Although efforts have been
made to ensure the that relevant engineering theories have been correctly implemented, it remains the user's responsibility to confirm and accept
the output. Refer to the [license](LICENSE) for clarification of the conditions of use.

By using the Blueprints package, you are agreeing to the following:

1. **Usage Risk**: The usage (i.e. downloading, installing, running, modifying the code, or some or all of the above) of Blueprints is entirely at your own risk as a user and/or contributor. All maintainers and contributors to Blueprints are not responsible for and cannot be held responsible or liable for any direct or indirect damages, injuries, death, faults, mistakes, or omissions that result from the usage of the package.

2. **Adherence to Laws and Regulations**: At all times, the user is fully responsible for the adherence to (local) laws and regulations. It is the user's responsibility to ensure that their use of Blueprints complies with all relevant legal and regulatory requirements.

3. **Outdated Results**: Results may be outdated due to circumstances, changes in rules and regulations, and/or changes in the codes and/or national 
   annexes. Users should always verify the results and not solely rely on the output from Blueprints.

4. **Agreement to Terms**: When using Blueprints, you agree to the terms and conditions of the [license](LICENSE) and this disclaimer.

5. **Warranties**: Blueprints is provided as is without any warranties of any kind, either expressed or implied.

Please note that this disclaimer is intended to be as broad and inclusive as permitted by the law of the jurisdiction in which you reside. If any portion of this disclaimer is held invalid, the remainder shall continue in full legal force and effect.

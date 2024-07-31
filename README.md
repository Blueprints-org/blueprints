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

Can someone explain to me why Eurocode is not publicly available in code and that all of us are coding Eurocode with massive maintenance costs 
and shortages in technical personnel? Well, no longer!

Welcome to Blueprints, the cornerstone repository for civil engineering professionals and enthusiasts alike!

Blueprints is a collaboration of several engineering companies which contains programmable Eurocode information such as tables, figures and 
formulas. It also provides materials, geometry and even section checks. The basis as well as the implemented use cases provide all key 
necessities for the civil engineer.

## Mission

Our mission is to:

- Offer a robust suite of tools and libraries that encapsulate common and advanced engineering tasks.
- Foster a community where sharing knowledge and best practices is the norm, not the exception.
- Provide a solid foundation of code and documentation that adheres to the highest quality standards (100% code coverage).

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

Contributions are very welcome. To learn more, see the [Contributor Guide](CONTRIBUTING.md).

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

3. **Outdated Results**: Results may be outdated due to circumstances, changes in rules and regulations, and/or changes in the Eurocodes and/or national annexes. Users should always verify the results and not solely rely on the output from the Blueprints package.

4. **Agreement to Terms**: When using Blueprints, you agree to the terms and conditions of the [license](LICENSE) and this disclaimer. If you do not agree with these terms, please do not use the Blueprints package.

5. **Warrenties**: The Blueprins package is provided as is without any warrenties of any kind, either expressed or implied.

Please note that this disclaimer is intended to be as broad and inclusive as permitted by the law of the jurisdiction in which you reside. If any portion of this disclaimer is held invalid, the remainder shall continue in full legal force and effect.

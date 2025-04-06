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

* Eurocode formulas [templates for making formula](https://github.com/orgs/Blueprints-org/discussions/432)
    - [ ] NEN-EN 1992-1-1+C2:2011 ![](https://img.shields.io/badge/50-%25-grey?style=plastic&labelColor=yellow)
    - [ ] NEN-EN 1993-1-1+C2+A1:2016 ![](https://img.shields.io/badge/20%25-grey?style=plastic&labelColor=orange)       
    - [ ] NEN-EN 1993-1-9+C2:2012 ![](https://img.shields.io/badge/20%25-grey?style=plastic&labelColor=orange)    
    - [ ] NEN-EN 1993-5:2008 ![](https://img.shields.io/badge/20%25-grey?style=plastic&labelColor=orange)           
    - [ ] NEN 9997-1+C2:2017 ![](https://img.shields.io/badge/20%25-grey?style=plastic&labelColor=orange)
 
* Material definitions
    - [x] Concrete (NEN-EN 1992) ✔️
    - [x] Rebar Steel (NEN-EN 1992) ✔️
    - [x] Soil (NEN-EN 1997) ✔️

* Reinforced Concrete Section
    - [x] Rectangular section ✔️
    - [ ] Circular section

* Strain-stress analysis for reinforced concrete sections:
  - [ ] Rectangular section ![](https://img.shields.io/badge/20%25-grey?style=plastic&labelColor=orange)
  - [ ] Circular section

* Concrete checks
  - [x] Nominal concrete cover (NEN-EN 1992-1-1: Chapter 4) ✔️
  - [ ] Anchorage- and Laplengths (NEN-EN 1992-1-1: Chapter 8)
  - [ ] Shear Resistance (NEN-EN 1992-1-1: Chapter 6.2)
  - [ ] Shear Resistance circular shapes;
  - [ ] Torsion (NEN-EN 1992-1-1: Chapter 6.3)
  - [ ] Punching Shear (NEN-EN 1992-1-1: Chapter 6.4)
  - [ ] Fatigue (NEN-EN 1992-1-1: Chapter 6.8)
  - [ ] Crack Control (NEN-EN 1992-1-1: Chapter 7.3)
  - [ ] Creep and Shrinkage (NEN-EN 1992-1-1: Chapter 3.1.4)

* Timber checks (NEN-EN 1995)
   - *To Be Determined*

* Steel checks (NEN-EN 1993)
  - *To Be Determined*

* Geotechnical checks (NEN-EN 9997-1)
  - *To Be Determined*

* Common calculations
  - [ ] Sheet-pile checks (strength and local buckling) ![](https://img.shields.io/badge/20%25-grey?style=plastic&labelColor=orange)
  - [ ] L-walls
  - [ ] Spring constants calculations for piles
 
<details>

<summary> Progress definitions </summary>

<table border="1">
  <thead>
    <tr>
      <th>Icon</th>
      <th>Definition</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><img src="https://img.shields.io/badge/20%25-grey?style=plastic&labelColor=orange" alt="20% Icon"></td>
      <td>Just started</td>
    </tr>
    <tr>
      <td><img src="https://img.shields.io/badge/50-%25-grey?style=plastic&labelColor=yellow" alt="50% Icon"></td>
      <td>Making progress</td>
    </tr>
    <tr>
      <td><img src="https://img.shields.io/badge/80%25--grey?style=plastic&labelColor=yellowgreen" alt="80% Icon"></td>
      <td>In Review</td>
    </tr>
    <tr>
      <td>✔️</td>
      <td>Done</td>
    </tr>
  </tbody>
</table>

</details>

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

<table>
  <thead>
    <tr>
      <th>Document</th>
      <th>Description</th>
      <th>Formulas</th>
      <th>Tables</th>
      <th>Figures</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>NEN-EN 1992-1-1+C2:2011</td>
      <td>
        Eurocode 2: Design of concrete structures – Part 1-1: General rules and rules for buildings
        (<a href="blueprints/codes/eurocode/nen_en_1992_1_1_c2_2011">code</a>)
      </td>
      <td><a href="docs/objects_overview/eurocode/ec2_1992_1_1_2011/formulas.md">304</a></td>
      <td><a href="docs/objects_overview/eurocode/ec2_1992_1_1_2011/tables.md">38</a></td>
      <td><a href="docs/objects_overview/eurocode/ec2_1992_1_1_2011/figures.md">104</a></td>
    </tr>
    <tr>
      <td>NEN-EN 1993-1-1+C2+A1:2016</td>
      <td>
        NEN-EN 1993-1-1+C2+A1:2016 | Eurocode 3: Design of steel structures – Part 1-1: General rules and rules for buildings
        (<a href="blueprints/codes/eurocode/nen_en_1993_1_1_c2_a1_2016">code</a>)
      </td>
      <td><a href="docs/objects_overview/eurocode/ec3_1993_1_1_2016/formulas.md">108</a></td>
      <td><a href="docs/objects_overview/eurocode/ec3_1993_1_1_2016/tables.md">20</a></td>
      <td><a href="docs/objects_overview/eurocode/ec3_1993_1_1_2016/figures.md">28</a></td>
    </tr>
    <tr>
      <td>NEN-EN 1993-5:2008</td>
      <td>
        Eurocode 3: Design of steel structures – Part 5: Piling
        (<a href="blueprints/codes/eurocode/nen_en_1993_5_2008">code</a>)
      </td>
      <td><a href="docs/objects_overview/eurocode/nen_en_1993_5_2008/formulas.md">63</a></td>
      <td><a href="docs/objects_overview/eurocode/nen_en_1993_5_2008/tables.md">0</a></td>
      <td><a href="docs/objects_overview/eurocode/nen_en_1993_5_2008/figures.md">0</a></td>
    </tr>
    <tr>
      <td>NEN 9997-1+C2:2017</td>
      <td>
        Eurocode 7: Geotechnical design of structures - Part 1: General rules
        (<a href="blueprints/codes/eurocode/nen_9997_1_c2_2017">code</a>)
      </td>
      <td><a href="docs/objects_overview/eurocode/nen_9997_1_c2_2017/formulas.md">88</a></td>
      <td><a href="docs/objects_overview/eurocode/nen_9997_1_c2_2017/tables.md">11</a></td>
      <td><a href="docs/objects_overview/eurocode/nen_9997_1_c2_2017/figures.md">25</a></td>
    </tr>
  </tbody>
</table>

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

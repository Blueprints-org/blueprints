# Library Organization

## Philosophy: Organization by Engineering Standards

Blueprints is organized around engineering standards and codes rather than purely by technical domain. Instead of generic *concrete calculations* or *steel design* modules, the library is structured according to the source documents that define the engineering logic.

This document-centric approach offers several critical advantages for engineering practice.

## Why Organize by Document?

### Version-Specific Engineering Logic

Engineering codes evolve over time. A calculation in Eurocode 2:2004 might differ from Eurocode 2:2023. By organizing by document and version, Blueprints can:

- Maintain multiple versions of the same standard simultaneously
- Ensure accuracy by matching calculations to exact code versions
- Support legacy projects that must comply with older codes
- Track changes between code revisions transparently

For example, both `en_1995_1_1_2004` and `en_1995_1_1_2023` exist in the library, each containing the specific formulas as written in that edition.

### Traceability and Verification

When calculations are organized by source document:

- Engineers can verify implementations against the original standard
- Code references are clear and unambiguous
- Quality assurance is straightforward
- Documentation aligns with professional practice
- Engineering reports are reproducible with exact formula versions

If you're working to EN 1992-1-1:2004, you know exactly where to find the formulas and can verify they match your code book.

#### Reproducibility in Engineering Reports

When you use a formula from `blueprints.codes.eurocode.en_1992_1_1_2004`, your calculation history captures the exact version of the exact formula used. Years later, anyone can reproduce your calculation, verify against the same code version, and audit your work with complete transparency.

This is essential for engineering liability, peer review, and regulatory compliance.

### Multi-Code Support

Different regions and projects use different standards. By organizing around documents:

- Multiple standards coexist without conflict
- Switching between codes is explicit and intentional
- Regional variations (like NEN-EN combinations) are clearly identified
- Project requirements dictate which code module you import

### Future-Proofing

When a new version of a code is released:

- New versions are added as separate modules without breaking existing code
- Your projects remain stable - updating is a deliberate choice
- Old versions can be marked deprecated while remaining functional
- Migration paths can be documented between versions

### Checking Existing Structures

When verifying or modifying existing buildings, the structure was designed using a specific code version. Current standards may have changed, but you can use the original design code to verify the existing structure, then optionally compare with current standards if needed.

This is essential in practice - the design code isn't necessarily the latest standard. Blueprints allows you to work with both, making informed decisions about when to apply which version.

## Trade-offs and Challenges

Document-based organization comes with trade-offs:

- More complexity: more modules to maintain, longer import paths, harder initial discovery
- Maintenance overhead: bug fixes may need applying across multiple code versions
- Learning curve: users must know which engineering standard applies to their project

Despite these challenges, we believe this is the right approach. The complexity reflects the reality of engineering practice - simplifying would sacrifice accuracy, traceability, and reproducibility. We're building a system that respects the rigor of civil engineering, not just a calculator.

We're continuously working to mitigate these challenges through better documentation, examples, and tooling. We highly value your ideas and feedback for further improvements - reach out via [Discord](https://discord.gg/hBZBqegEzA) or [GitHub](https://github.com/Blueprints-org/blueprints/issues).

## Practical Organization Structure

### Document Hierarchy

Code-based functionality follows a hierarchical structure:

```
blueprints/
  codes/
    eurocode/
      en_1992_1_1_2004/    # Eurocode 2, Part 1-1, 2004 edition
      en_1993_1_1_2005/    # Eurocode 3, Part 1-1, 2005 edition
      nen_en_1992_1_1_a1_2020/  # Dutch national annex
    cur/
      cur_228/             # CUR Recommendation 228
```

Each folder contains the formulas, checks, and logic defined in that particular standard.

### When Organization Differs

Not all of Blueprints is organized by document. Modules providing fundamental building blocks are organized differently:

- `blueprints.materials`: Generic material property definitions
- `blueprints.geometry`: Universal geometric operations and shapes
- `blueprints.structural_sections`: Cross-section definitions used across multiple codes

These foundational modules provide the common language that code-specific modules build upon.

#### Evolution Toward Standard-Specific Organization

The library can and likely will evolve to make more components standard-specific when appropriate. Material definitions, section properties, and design parameters are often standard-specific and may benefit from this organization.

As Blueprints matures, we expect more standard-specific organization where it adds value. This evolution may result in some breaking changes in early versions. Techniques like dependency injection may provide elegant solutions.

The goal is finding the right balance: generic enough to avoid duplication, specific enough to ensure accuracy and traceability. This is an ongoing process that will evolve based on real-world usage and community feedback.

## Benefits for Users

As an engineer using Blueprints, you work the same way you work with physical standards:

1. Identify your applicable code (e.g., EN 1992-1-1:2004)
2. Import from that specific module
3. Apply the formulas knowing they match your code book
4. Document your calculations with clear code references

Because the organization mirrors engineering practice:

- Peer review is easier - reviewers can trace calculations to specific clauses
- Compliance is demonstrable - it's clear which code version you're using
- Updates are transparent - changes are isolated and explicit
- Mixing codes is intentional - visible in your imports

## Finding What You Need

Rather than maintaining a detailed table of contents here, Blueprints provides better discovery methods:

- API reference: Complete documentation of all modules, classes, and functions
- Code exploration: Navigate `blueprints.codes` to see supported standards
- Examples: Practical demonstrations of specific codes
- Autocomplete: Your IDE shows available modules when you type `blueprints.codes.eurocode.`

If you know which engineering standard you need, you already know where to look.

### Can't Find What You're Looking For?

If you can't find a specific standard, formula, or functionality:

- Join our [Discord community](https://discord.gg/hBZBqegEzA) for help and discussion
- Open a [GitHub issue](https://github.com/Blueprints-org/blueprints/issues) to request features
- Reach out to the maintainers - we're interested in understanding what engineers need

Your input helps shape the future of Blueprints!
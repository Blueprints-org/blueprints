# The Formula Object: Design and Architecture

The Formula object is a fundamental component of `blueprints`, designed to seamlessly integrate engineering calculations with comprehensive documentation and traceability capabilities. 

This document examines the architectural design decisions and implementation rationale behind the Formula object.

## Design Requirements

The Formula object architecture addresses key challenges in engineering software development:

- **Native Integration**: Formula results should integrate seamlessly with standard Python syntax and operations making it easy to use
- **Rich Metadata**: Each calculation must preserve its origin including source references, parameters, and documentation
- **Automatic Documentation**: Formulas should generate technical documentation without manual intervention
- **Reliable Behavior**: The object should behave predictably and intuitively in all contexts
- **Compositional Design**: Formula results must be injectable into other formulas to enable modular calculations

## Architectural Overview

The Formula class implements five core capabilities:

1. **Float Inheritance**: Formula objects behave identically to Python's native numeric types in mathematical operations
2. **Metadata Preservation**: Each formula maintains comprehensive information about its source, parameters, and calculation methodology
3. **Compositional Architecture**: Formula results can serve as inputs to other formulas, enabling complex calculation workflows
4. **Automatic LaTeX Generation**: Built-in capability to produce mathematical notation for technical documentation
5. **Immutable Design**: Formula objects cannot be modified after initialization, ensuring calculation integrity and preventing unintended side effects

The following sections demonstrate these capabilities through practical examples using real Eurocode implementations.

## Import Required Components

We'll import concrete implementations from the Eurocode NEN-EN 1992-1-1 standard. Formula 4.2 calculates minimum concrete cover based on bond and durability requirements, while Formula 4.1 calculates nominal concrete cover by adding construction tolerance. These formulas have a natural composition relationship.

```python exec="on" source="material-block" title="formulas.py" session="formulas"
# Import actual Eurocode formulas for concrete cover calculations
from blueprints.codes.eurocode.nen_en_1992_1_1_a1_2020.chapter_4_durability_and_cover.formula_4_1 import Form4Dot1NominalConcreteCover
from blueprints.codes.eurocode.nen_en_1992_1_1_a1_2020.chapter_4_durability_and_cover.formula_4_2 import Form4Dot2MinimumConcreteCover
from blueprints.codes.formula import Formula
```

## Formula Object Creation

Let's create a Formula object using an actual implementation from the Eurocode standards. Formula 4.1 calculates the nominal concrete cover based on minimum cover and construction tolerance.

```python exec="on" source="material-block" session="formulas" result="ansi"
# Create a Formula instance using Eurocode formula 4.1: c_nom = c_min + Δc_dev
c_min = 25.0  # mm
delta_c_dev = 10.0  # mm
concrete_cover = Form4Dot1NominalConcreteCover(c_min=c_min, delta_c_dev=delta_c_dev)

print(f"Formula result: {concrete_cover} mm")
print(f"Type: {type(concrete_cover).__name__}")
print(f"Is float instance: {isinstance(concrete_cover, float)}")
print(f"Is Formula instance: {isinstance(concrete_cover, Formula)}")
print(f"Formula label: {concrete_cover.label}")
print(f"Source document: {concrete_cover.source_document}")
print(f"Stored parameters: c_min={concrete_cover.c_min}, delta_c_dev={concrete_cover.delta_c_dev}")
print("\n💡 Key insight: The object IS the result (35.0) but carries rich metadata")
```

## Float Inheritance Behavior

One of the key design features is that Formula objects inherit from Python's `float` type. This means they can be used in mathematical operations exactly like built-in numeric types, making them seamlessly integrate into existing Python code.

```python exec="on" source="material-block" session="formulas" result="ansi"
# Mathematical operations work directly with Formula objects
print(f"Original value: {concrete_cover}")
print(f"Addition: {concrete_cover + 5.0}")
print(f"Multiplication: {concrete_cover * 1.2}")
print(f"Comparison: {concrete_cover > 30}")

# Formula objects work anywhere floats are expected
values = [concrete_cover, 40.0, 50.0]
print(f"Maximum: {max(values)}")
print(f"Sum: {sum([concrete_cover, 10, 20])}")

# Important: Assignment operators create new references and lose Formula metadata!
original_formula = concrete_cover  # Keep reference to original Formula
concrete_cover += 5.0  # This creates a new float object
print("\nAfter += operation:")
print(f"  Result: {concrete_cover}, type: {type(concrete_cover).__name__}")
print(f"  Is Formula instance: {isinstance(concrete_cover, Formula)}")
print(f"  Original formula still intact: {original_formula} (type: {type(original_formula).__name__})")
```

## Formula Composition

The real power of the Formula design becomes apparent when composing formulas. Since Formula objects behave like native Python numbers, they can be seamlessly used as inputs to other formulas. Let's demonstrate this with actual Eurocode formulas where Formula 4.2 (minimum concrete cover) feeds into Formula 4.1 (nominal concrete cover).

```python exec="on" source="material-block" session="formulas" result="ansi"
# Demonstrate composition using real Eurocode formulas
# Formula 4.2 calculates minimum concrete cover
c_min_b = 16.0  # mm - minimum cover for bond requirements
c_min_dur = 20.0  # mm - minimum cover for durability
min_cover = Form4Dot2MinimumConcreteCover(
    c_min_b=c_min_b,
    c_min_dur=c_min_dur,
    delta_c_dur_gamma=0,  # reduction for stainless steel
    delta_c_dur_st=0,  # reduction for additional protection
    delta_c_dur_add=0,  # reduction for additional measures
)

# Formula 4.1 uses the result of Formula 4.2 as input
# Notice how we pass the entire Formula object, not just its value
delta_c_dev = 10.0  # mm - construction tolerance
nominal_cover = Form4Dot1NominalConcreteCover(
    c_min=min_cover,  # This is a Formula object!
    delta_c_dev=delta_c_dev,
)

print(f"Minimum cover (Formula 4.2): {min_cover} mm")
print(f"Nominal cover (Formula 4.1): {nominal_cover} mm")
print("\nComposition verification:")
print(f"  Formula 4.1 received c_min as: {nominal_cover.c_min}")
print(f"  Type of c_min input: {type(nominal_cover.c_min).__name__}")
print(f"  Original Formula 4.2 label: {nominal_cover.c_min.label}")
```

## Key Insights from Composition

**Transparent Composition:** Formula 4.1 doesn't need to know it received a Formula object - it works seamlessly because Formula inherits from `float`. This enables plug-and-play modularity where any calculation can accept either raw values or Formula objects.

**Calculation History Preservation:** The immutable design means you can recursively retrieve the complete calculation history of any result. Each Formula object maintains references to its inputs, creating a directed acyclic graph of the entire calculation workflow.

**Engineering Traceability:** This design provides full audit trails for engineering calculations - crucial for regulatory compliance, peer review, and quality assurance in professional engineering applications.

## Metadata and Traceability

Beyond the numerical result, each Formula object carries rich metadata that enables full traceability of calculations. This is crucial for engineering applications where you need to document the source and methodology of every calculation.

```python exec="on" source="material-block" session="formulas" result="ansi"
# Examine metadata available in our composed Formula objects
formulas = [min_cover, nominal_cover]
names = ["Minimum Cover (4.2)", "Nominal Cover (4.1)"]

for name, formula in zip(names, formulas):
    print(f"\n{name}:")
    print(f"  Result: {formula} mm")
    print(f"  Formula Label: {formula.label}")
    print(f"  Source Document: {formula.source_document}")
    print(f"  Implementation: {formula.__class__.__name__}")
    print(f"  Module: {formula.__class__.__module__}")

    # Show stored input parameters with their types
    print("  Input Parameters:")
    for attr_name in ["c_min_b", "c_min_dur", "c_min", "delta_c_dev"]:
        if hasattr(formula, attr_name):
            attr_value = getattr(formula, attr_name)
            value_type = type(attr_value).__name__
            print(f"    {attr_name}: {attr_value} ({value_type})")

# Demonstrate immutability protection
print("\nImmutability Protection:")
try:
    nominal_cover.c_min = 999  # This should fail
    print("❌ ERROR: Modification should have been prevented!")
except AttributeError:
    print("✅ Modification prevented: Formula objects are immutable after creation")
    print("   This ensures calculation integrity and prevents accidental parameter changes.")
```

## LaTeX Documentation Generation

A major benefit of the Formula design is automatic LaTeX generation for technical documentation. Every formula can generate its mathematical representation, eliminating the need for manual equation formatting in reports and documentation.

```python exec="on" source="material-block" session="formulas" result="ansi"
# Generate LaTeX representations for our Eurocode formulas
latex_min = min_cover.latex()
latex_nom = nominal_cover.latex()

print("LaTeX Generation for Eurocode Formulas:")
print("\nFormula 4.2 (Minimum Cover):")
print(f"  Complete equation: {latex_min.complete}")
print(f"  Return symbol: {latex_min.return_symbol}")
print(f"  Symbolic equation: {latex_min.equation}")
print(f"  Numeric equation: {latex_min.numeric_equation}")

print("\nFormula 4.1 (Nominal Cover):")
print(f"  Complete equation: {latex_nom.complete}")
print(f"  Return symbol: {latex_nom.return_symbol}")
print(f"  Symbolic equation: {latex_nom.equation}")

print("\nLaTeX Structure:")
print("  Each LatexFormula object contains:")
print("    • return_symbol: Left-hand side of equation (e.g., 'c_nom')")
print("    • equation: Right-hand side with symbols (e.g., 'c_min + \\Delta c_dev')")
print("    • numeric_equation: Equation with actual values")
print("    • result: Final calculated result")
print("    • complete: Full formatted equation for documentation")

print("  This enables automatic generation of technical reports and documentation")
print("  without manual LaTeX formatting, ensuring consistency across all calculations.")
```

## Summary: Key Benefits and Implementation

### Practical Advantages

The Formula object design provides several practical advantages:

### 1. Seamless Integration
- Formula objects work in mathematical operations like native Python numbers
- No special handling required when using formulas as inputs to calculations
- Compatible with Python's built-in functions (`max()`, `sum()`, etc.)

### 2. Calculation Traceability  
- Each formula maintains its label and source document reference
- Input parameters are preserved for verification and debugging
- Full audit trail from result back to original calculation

### 3. Automatic Documentation
- LaTeX generation eliminates manual equation formatting
- Consistent mathematical notation across all calculations
- Direct integration with technical documentation workflows

### 4. Modular Architecture
- Complex calculations built from simple, testable components
- Formula objects can be reused in different calculation contexts
- Easy to modify individual calculation steps without affecting others

### 5. Data Integrity
- Immutable objects prevent accidental modification of critical calculations
- Type safety through abstract base class enforcement
- Consistent interface across all formula implementations
- 
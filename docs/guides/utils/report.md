# Creating Reports with Blueprints

The `LatexReport` class helps you build professional engineering reports with text, equations, tables, and figures. The output is LaTeX-formatted and ready to use in Overleaf, compile locally, or convert to Word documents.

??? info "Complete Example"

    Use the following code to create a simple (mock) engineering report:
    
    ```python exec="on" source="tabbed-left"
    from blueprints.utils.report import LatexReport
    from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import formula_6_5
    
    # Create report
    report = LatexReport(title="Design Verification")
    
    # Add content
    report.add_section("Introduction")
    report.add_text("This report verifies the tensile capacity of the steel member.")
    
    report.add_section("Design Checks")
    report.add_text("Unity check for tensile strength:", bold=True).add_newline()
    
    formula = formula_6_5.Form6Dot5UnityCheckTensileStrength(n_ed=150000, n_t_rd=200000)
    report.add_formula(formula, options="complete")
    
    report.add_text("Result: Check PASSED", bold=True)
    
    report.add_section("Summary")
    report.add_itemize([
        "Applied force: 150 kN",
        "Resistance: 200 kN",
        "Utilization: 75%",
    ])
    
    # Get LaTeX document
    latex = report.to_document()
    print(latex)
    ```

??? info "Tips"

    - Use **method chaining** for cleaner code: `report.add_section(...).add_text(...).add_newline()`
    - Use raw strings (`r"..."`) for LaTeX commands to avoid escape issues
    - Call `.to_document()` only when you need the final output
    - Call `.add_formula()` on formulas from Blueprints to automatically include source and formula numbers in the tag

## Quick Start

Create a report and add content using [method chaining](https://www.geeksforgeeks.org/python/method-chaining-in-python/):

```python exec="on" session="report_quick_start" source="tabbed-left"
from blueprints.utils.report import LatexReport
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import formula_6_5

# Create a report
report = LatexReport(title="Steel Connection Analysis")

# Add sections and content
report.add_section("Design Checks")
report.add_text("We verify the tensile strength capacity:")

# Add a formula
formula = formula_6_5.Form6Dot5UnityCheckTensileStrength(
    n_ed=150000,  # Applied force (kN)
    n_t_rd=200000,  # Resistance (kN)
)
report.add_formula(formula, options="complete")

# Generate the complete LaTeX document
latex_code = report.to_document()
```

## Getting Your Report

### View Report Summary

```python exec="on" session="report_quick_start" source="tabbed-left"
# Quick overview of what's in your report
print(report)
```

### Export to LaTeX

```python exec="on" session="report_quick_start" source="tabbed-left"
# Get the complete LaTeX document (ready for Overleaf or pdflatex)
latex_document = report.to_document()

# Save to file
# with open("report.tex", "w") as f:
#     f.write(latex_document)
```

### Export to Word (Optional)

The LaTeX output can be converted to .docx format using external tools. We will cover this in future documentation.

## Common Tasks

### Add Text

```python exec="on" source="tabbed-left"
from blueprints.utils.report import LatexReport

# Create a report
report = LatexReport(title="My report")

report.add_text("This is regular text.")
report.add_text("This is bold text.", bold=True)
report.add_text("This is italic text.", italic=True)
report.add_text("This is bold and italic.", bold=True, italic=True)
```

### Add Sections

```python exec="on" source="tabbed-left"
from blueprints.utils.report import LatexReport

# Create a report
report = LatexReport(title="My report")

report.add_section("Introduction")
report.add_subsection("Background")
report.add_subsubsection("Technical Details")
```

### Add Equations

**Standalone equation:**
```python exec="on" source="tabbed-left"
from blueprints.utils.report import LatexReport

# Create a report
report = LatexReport(title="My report")

report.add_equation("a^2 + b^2 = c^2", tag="Pythagoras")
```

**Inline equation (within text):**
```python exec="on" source="tabbed-left"
from blueprints.utils.report import LatexReport

# Create a report
report = LatexReport(title="My report")

report.add_text("The resistance is ").add_equation(r"\frac{F_y \cdot A}{1.0}", inline=True).add_text(" kN")
```

### Add Blueprints Formulas

```python exec="on" source="tabbed-left"
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state import formula_6_6n
from blueprints.utils.report import LatexReport

# Create a report
report = LatexReport(title="My report")

formula = formula_6_6n.Form6Dot6nStrengthReductionFactor(35)

# Add with different detail levels
report.add_formula(formula, options="short")  # Just result
report.add_formula(formula, options="complete")  # Full derivation
report.add_formula(formula, options="complete_with_units")  # With unit labels

# Control what's shown in the tag
report.add_formula(
    formula,
    options="complete",
    include_source=True,  # Show "EN 1992-1-1:2004"
    include_formula_number=True,  # Show "6.6n"
)
```

### Add Tables

```python exec="on" source="tabbed-left"
from blueprints.utils.report import LatexReport

# Create a report
report = LatexReport(title="My report")

report.add_table(
    headers=["Check", "Utilization", "Status"],
    rows=[
        [r"\text{Shear capacity}", "0.588", r"\text{PASS}"],
        [r"\text{Torsion capacity}", "0.925", r"\text{PASS}"],
    ]
)
```

### Add Figures

```python exec="on" source="tabbed-left"
from blueprints.utils.report import LatexReport

# Create a report
report = LatexReport(title="My report")

# Simple figure
report.add_figure("diagram.png", width=0.6)

# Figure with caption
report.add_figure("stress_plot.png", width=0.7, caption="Stress distribution under load")
```

### Add Lists

```python exec="on" source="tabbed-left"
from blueprints.utils.report import LatexReport

# Create a report
report = LatexReport(title="My report")

# Bullet list
report.add_itemize(["Check 1 passed", "Check 2 passed", "Check 3 failed"])

# Numbered list
report.add_enumerate(["First step: verify inputs", "Second step: run calculations", "Third step: review results"])
```

### Add Spacing

```python exec="on" source="tabbed-left"
from blueprints.utils.report import LatexReport

# Create a report
report = LatexReport(title="My report")

report.add_newline()  # Single new line
report.add_newline(n=3)  # Three new lines
```
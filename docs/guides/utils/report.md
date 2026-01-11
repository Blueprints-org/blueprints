# Creating Reports with Blueprints

The `Report` class helps you build professional engineering reports with text, equations, tables, and figures. 


??? info "Complete Example"

    Use the following code to create a simple (mock) engineering report:
    
    ```python exec="on" source="tabbed-left" result="console"
    from blueprints.utils.report import Report
    from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import formula_6_5
    
    # Create report
    report = Report(title="Design Verification")
    
    # Add content
    report.add_heading("Introduction")
    report.add_paragraph("This report verifies the tensile capacity of the steel member.")
    
    report.add_heading("Design Checks")
    report.add_paragraph("Unity check for tensile strength:", bold=True).add_newline()
    
    formula = formula_6_5.Form6Dot5UnityCheckTensileStrength(n_ed=150000, n_t_rd=200000)
    report.add_formula(formula, options="complete")
    
    report.add_paragraph("Result: Check PASSED", bold=True)
    
    report.add_heading("Summary")
    report.add_list([
        "Applied force: 150 kN",
        "Resistance: 200 kN",
        "Utilization: 75%",
    ], style="bulleted")
    
    # Get LaTeX document
    latex = report.to_latex()
    print(latex)
    ```

??? info "Tips"

    - Use **method chaining** for cleaner code: `report.add_heading(...).add_paragraph(...).add_newline()`
    - Use raw strings (`r"..."`) for LaTeX commands to avoid escape issues
    - Call `.to_latex()` for a final Latex-formatted output
    - Call `.to_word()` to export directly to a Word document
    - Call `.add_formula()` on formulas from Blueprints to automatically include source and formula numbers in the tag

## Quick Start

Create a report and add content using [method chaining](https://www.geeksforgeeks.org/python/method-chaining-in-python/):

```python exec="on" session="report_quick_start" source="tabbed-left" result="console"
from blueprints.utils.report import Report
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import formula_6_5

# Create a report
report = Report(title="Steel Connection Analysis")

# Add sections and content
report.add_heading("Design Checks")
report.add_paragraph("We verify the tensile strength capacity:")

# Add a formula
formula = formula_6_5.Form6Dot5UnityCheckTensileStrength(
    n_ed=150000,  # Applied force (N)
    n_t_rd=200000,  # Resistance (N)
)
report.add_formula(formula, options="complete")

# Generate the complete LaTeX document
latex_code = report.to_latex()
print(latex_code)
```

## Getting Your Report

### Export to LaTeX

```python exec="on" session="report_quick_start" source="tabbed-left" result="console"
# Save the complete LaTeX document to your local disk (ready for Overleaf or pdflatex)
report.to_latex('report.tex')
```

### Export to Word

You can convert your report to a Word document directly in three ways:

**Save to a file path:**

```python exec="on" source="tabbed-left" result="console"
from blueprints.utils.report import Report

# Create a report
report = Report(title="My report")
report.add_heading("Introduction")
report.add_paragraph("Some content here.")

# Save to file
report.to_word("report.docx")
```

**Write to bytes (for in-memory processing):**

```python exec="on" source="tabbed-left" result="console"
from blueprints.utils.report import Report
from io import BytesIO

# Create a report
report = Report(title="My report")
report.add_heading("Introduction")
report.add_paragraph("Some content here.")

# Write to bytes (useful for web downloads, email attachments, etc.)
docx_bytes = report.to_word()

print(f"Document size: {len(docx_bytes)} bytes")
```

**Get bytes directly (useful for streaming or email):**

```python exec="on" source="tabbed-left" result="console"
from blueprints.utils.report import Report

# Create a report
report = Report(title="My report")
report.add_heading("Introduction")
report.add_paragraph("Some content here.")

# Get bytes directly
docx_bytes = report.to_word()
print(f"Document size: {len(docx_bytes)} bytes")

# Now you can stream it, send as email attachment, store in database, etc.
```

## Common Tasks

### Add Text

```python exec="on" source="tabbed-left" result="console"
from blueprints.utils.report import Report

# Create a report
report = Report(title="My report")

report.add_paragraph("This is regular text.")
report.add_paragraph("This is bold text.", bold=True)
report.add_paragraph("This is italic text.", italic=True)
report.add_paragraph("This is bold and italic.", bold=True, italic=True)

print(report.to_latex())
```

### Add Sections

```python exec="on" source="tabbed-left" result="console"
from blueprints.utils.report import Report

# Create a report
report = Report(title="My report")

report.add_heading("Introduction")
report.add_heading("Background", level=2)
report.add_heading("Technical Details", level=3)

print(report.to_latex())
```

### Add Equations

**Standalone equation:**

```python exec="on" source="tabbed-left" result="console"
from blueprints.utils.report import Report

# Create a report
report = Report(title="My report")

report.add_equation("a^2 + b^2 = c^2", tag="Pythagoras")

print(report.to_latex())
```

**Inline equation (within text):**

```python exec="on" source="tabbed-left" result="console"
from blueprints.utils.report import Report

# Create a report
report = Report(title="My report")

report.add_paragraph("The resistance is ").add_equation(r"\frac{F_y \cdot A}{1.0}", inline=True).add_paragraph(" kN")

print(report.to_latex())
```

### Add Blueprints Formulas

```python exec="on" source="tabbed-left" result="console"
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state import formula_6_6n
from blueprints.utils.report import Report

# Create a report
report = Report(title="My report")

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
print(report.to_latex())
```

### Add Tables

```python exec="on" source="tabbed-left" result="console"
from blueprints.utils.report import Report

# Create a report
report = Report(title="My report")

report.add_table(
    headers=["Check", "Utilization", "Status"],
    rows=[
        [r"\text{Shear capacity}", "0.588", r"\text{PASS}"],
        [r"\text{Torsion capacity}", "0.925", r"\text{PASS}"],
    ]
)
print(report.to_latex())
```

### Add Figures

```python exec="on" source="tabbed-left" result="console"
from blueprints.utils.report import Report

# Create a report
report = Report(title="My report")

# Simple figure
report.add_figure("diagram.png", width=0.6)

# Figure with caption
report.add_figure("stress_plot.png", width=0.7, caption="Stress distribution under load")

print(report.to_latex())
```

### Add Lists

```python exec="on" source="tabbed-left" result="console"
from blueprints.utils.report import Report

# Create a report
report = Report(title="My report")

# Bullet list
report.add_list(["Check 1 passed", "Check 2 passed", "Check 3 failed"], style="bulleted")

# Numbered list
report.add_list(["First step: verify inputs", "Second step: run calculations", "Third step: review results"], style='numbered')

# Numbered list, nested
report.add_list(["One", ["A", "B", "C"], "Two", ["A", ["I", "II", "III"]]], style="numbered")

print(report.to_latex())
```

### Add Spacing

```python exec="on" source="tabbed-left" result="console"
from blueprints.utils.report import Report

# Create a report
report = Report(title="My report")

report.add_newline()  # Single new line
report.add_newline(n=3)  # Three new lines

print(report.to_latex())
```
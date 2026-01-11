# Creating Reports and Exporting to LaTeX

This notebook demonstrates how to use the `Report` class to build engineering reports and export them to LaTeX `.tex` files with language localization.

```python
from blueprints.utils.report import Report

# Create report
report = Report(title="Engineering Report")
report.add_heading("Section 1")
report.add_paragraph("This is a sample paragraph with some content.")
report.add_equation("E = mc^2", tag="1")

# Export in English (default)
report.to_latex("report_english.tex")
print("English LaTeX file created")

# Export in German
report.to_latex("report_german.tex", language="de")
print("German LaTeX file created")

# Export in Dutch
report.to_latex("report_dutch.tex", language="nl")
print("Dutch LaTeX file created")

# Export in Spanish
report.to_latex("report_spanish.tex", language="es")
print("Spanish LaTeX file created")

# Get LaTeX as string (without saving to file)
latex_content = report.to_latex()
print("\nLaTeX content preview:")
print(latex_content[:200] + "...")
```
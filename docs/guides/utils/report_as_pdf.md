# Creating Reports and Converting to Word

This notebook demonstrates how to use the `Report` class to build engineering reports and convert them to pdf documents with language localization. For more notes on how to build a report, see the `Report.md` file.

Note: usage of this feature requires installation of a LaTeX distribution (e.g., MiKTeX, TeX Live) that includes pdflatex. Go to https://miktex.org/download or https://www.tug.org/texlive/ for more information.

```python
from blueprints.utils.report import Report

# Create report
report = Report(title="Engineering Report")
report.add_heading("Section 1")
report.add_paragraph("This is a sample paragraph with some content.")
report.add_equation("E = mc^2", tag="1")

# Export in English (default)
report.to_pdf("report_english.pdf")
print("English document created")

# Export in German
report.to_pdf("report_german.pdf", language="de")
print("German document created")

# Export in Dutch
report.to_pdf("report_dutch.pdf", language="nl")
print("Dutch document created")

# Export in Spanish
report.to_pdf("report_spanish.pdf", language="es")
print("Spanish document created")
```
# Creating Reports and Converting to Word

This notebook demonstrates how to use the `Report` class to build engineering reports and convert them to Word documents with language localization.

```python
from blueprints.utils.report import Report

# Create report
report = Report(title="Engineering Report")
report.add_heading("Section 1")
report.add_paragraph("This is a sample paragraph with some content.")
report.add_equation("E = mc^2", tag="1")

# Export in English (default)
report.to_word("report_english.docx")
print("English document created")

# Export in German
report.to_word("report_german.docx", language="de")
print("German document created")

# Export in Dutch
report.to_word("report_dutch.docx", language="nl")
print("Dutch document created")

# Export in Spanish
report.to_word("report_spanish.docx", language="es")
print("Spanish document created")
```
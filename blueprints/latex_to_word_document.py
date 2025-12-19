"""Module to convert LaTeX (with text and equations) to a Word document."""

import re

import latex2mathml.converter
import mathml2omml
from docx import Document
from docx.document import Document as DocumentObject
from docx.oxml import parse_xml
from docx.oxml.xmlchemy import BaseOxmlElement


class LatexToWordConverter:
    r"""
    Limitations and Usage Notes:
    - This converter currently supports LaTeX input containing text and equations only. Figures and tables are not yet supported.
    - Use \newline to indicate new lines. Do not use the double backslash \\ for line breaks.
    - All text must be wrapped in \text{...}. This is also required for compatibility with the translation module.
    - To mix text and equations, close the \text{...} block, write the equation, and then start a new \text{...} block for subsequent text.
    - If you need to include text within an equation (e.g., as a note in brackets), use slashes between words: e.g., (note\ between\ words).
    """

    def __init__(self) -> None:
        """Initialize the converter and optionally convert LaTeX to a Document."""

    @staticmethod
    def _formula(latex_string: str) -> BaseOxmlElement:
        """Convert a LaTeX equation string to an OMML XML element for Word.

        Args:
            latex_string: The LaTeX string representing the equation.
        """
        mathml_output = latex2mathml.converter.convert(latex_string)
        omml_output = mathml2omml.convert(mathml_output)
        xml_output = f'<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">{omml_output}</m:oMathPara>'
        return parse_xml(xml_output)[0]

    def convert_to_word(self, latex: str) -> DocumentObject:
        r"""
        Convert a LaTeX string (with text and equations) to a Word Document object.
        Args:
            latex: The LaTeX string, with lines separated by \newline, text in \text{...}, equations otherwise.

        Returns
        -------
            The python-docx Document object (not saved).
        """
        doc = Document()
        lines = latex.split(r"\newline")
        parsed = []

        # Parse lines into categories: text or equation
        for line in lines:
            # Find all \text{...} and non-\text{...} sections
            pattern = r"\\text\{(.*?)\}|([^\n]+?)(?=(\\text\{|$))"
            for match in re.finditer(pattern, line):
                text_content = match.group(1)
                eq_content = match.group(2)
                if text_content is not None:
                    parsed.append({"type": "text", "content": text_content})
                elif eq_content is not None and eq_content.strip():
                    parsed.append({"type": "equation", "content": eq_content.strip()})
            # Add new line after each line except for the last one
            if lines and line != lines[-1]:
                parsed.append({"type": "text", "content": "\n"})

        # Add parsed content to document and format based on type of content
        p = doc.add_paragraph()
        for item in parsed:
            if item["type"] == "equation":
                # Accessing the private attribute `_p` of the python-docx Paragraph object.
                # This is necessary because the public API does not support inserting OMML (Office Math Markup Language)
                # elements (used for equations) directly into a paragraph.
                p._p.append(self._formula(item["content"]))  # noqa: SLF001
            else:
                p.add_run(item["content"])

        return doc

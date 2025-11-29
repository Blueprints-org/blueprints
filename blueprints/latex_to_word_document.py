"""Module to convert LaTeX (with text and equations) to a Word document."""

import latex2mathml.converter
import mathml2omml
from docx import Document
from docx.oxml import parse_xml


class LatexToWordConverter:
    r"""
    Converts LaTeX strings (with text and equations) to a Word document.
    Parses and adds \text{..} as normal document text and equations in equations mode.
    To create nicely formatted equations in Word, equations and lines of text should be separated by \newline.
    Lines of text should always start with \text{...}.

    Args:
        latex: The LaTeX string, with lines separated by \newline, text in \text{...}, equations otherwise.
    """

    def __new__(cls, latex: str = "") -> Document:
        """Create a new Document from LaTeX string."""
        if latex == "":
            return Document()
        instance = super().__new__(cls)
        return instance.convert(latex)

    @staticmethod
    def _formula(latex_string: str) -> parse_xml:
        """Convert a LaTeX equation string to an OMML XML element for Word.

        Args:
            latex_string: The LaTeX string representing the equation.
        """
        mathml_output = latex2mathml.converter.convert(latex_string)
        omml_output = mathml2omml.convert(mathml_output)
        xml_output = f'<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">{omml_output}</m:oMathPara>'
        return parse_xml(xml_output)[0]

    def convert(self, latex: str) -> Document:
        r"""
        Convert a LaTeX string (with text and equations) to a Word Document object.
        Args:
            latex: The LaTeX string, with lines separated by \\, text in \text{...}, equations otherwise.

        Returns
        -------
            The python-docx Document object (not saved).
        """
        doc = Document()
        lines = latex.split(r"\newline")
        parsed = []

        # Parse lines into categories: text or equation
        for line in lines:
            if line.lstrip().startswith(r"\text{"):
                parsed.append({"type": "text", "content": line.replace(r"\text{", "").replace("}", "") + "\n"})
            else:
                parsed.append({"type": "equation", "content": line})
                parsed.append({"type": "text", "content": "\n"})

        # Add parsed content to document and format based on type of content
        p = doc.add_paragraph()
        for item in parsed:
            if item["type"] == "equation":
                p._p.append(self._formula(item["content"]))  # noqa: SLF001
            else:
                p.add_run(item["content"])

        return doc

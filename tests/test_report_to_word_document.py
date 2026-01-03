"""Tests for the ReportToWordConverter class."""

from blueprints.report_to_word_document import ReportToWordConverter
from blueprints.utils.report import LatexReport


class TestReportToWordConverter:
    """Tests for the ReportToWordConverter class."""

    def test_empty_input_returns_empty_document(self) -> None:
        """Test that an empty LaTeX string returns an empty Document."""
        assert ReportToWordConverter().convert_to_word("")

    def test_complex_document_conversion(self) -> None:
        """Test conversion of a complex LaTeX document."""
        report = LatexReport("Testing Title")
        report.add_section("Testing Section")
        report.add_subsection("Testing Subsection")
        report.add_subsubsection("Testing Subsubsection")
        report.add_text("Bold and", bold=True).add_text(" normal text.").add_newline(n=2)
        report.add_text("And Italic text.", italic=True).add_text(" And also bold and italic.", bold=True, italic=True).add_newline()
        report.add_text("Here is an inline equation: $E=mc^2$ within the text.").add_newline()
        report.add_text("test").add_equation("E=mc^2", tag="1", inline=True).add_text("more text.").add_newline()
        report.add_text("test").add_equation("E=mc^2", inline=True).add_text("more text.").add_newline()
        report.add_equation("E=mc^2", tag="4")
        report.add_equation(r"\int_a^b f(x)dx = F(b) - F(a)")
        report.add_enumerate(["One", ["A", "B", "C"], "Two", ["A", ["I", "II", ["A", "B"], "III"]]])
        report.add_itemize(["First", "Second", ["Subfirst", "Subsecond"], "Third"])
        report.add_text("Here is a table:")
        report.add_table(
            headers=["Header 1", "Header 2", "Header 3 with math $E=mc^2$"],
            rows=[["Row 1 Col 1", "Row 1 Col 2 with inline math $a^2 + b^2 = c^2$", "Row 1 Col 3"], ["Row 2 Col 1", "Row 2 Col 2", "Row 2 Col 3"]],
        )
        report.add_section("Another Section")
        report.add_subsection("Another Subsection")
        report.add_subsection("Yet another Subsection")
        report.add_subsubsection("Yet another Subsubsection")
        report.add_subsubsection("Yet another Subsubsection v2")

        report.add_figure(r"docs\_overrides\assets\images\logo-light-mode.png", width=0.4, caption="Blueprints Logo")

        latex = str(report.to_document())
        converter = ReportToWordConverter()

        assert converter.convert_to_word(latex)

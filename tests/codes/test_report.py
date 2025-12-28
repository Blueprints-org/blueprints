"""Tests for the LatexReport and ReportFormula classes."""

import pytest

from blueprints.codes.report import LatexReport


@pytest.fixture
def fixture_report() -> LatexReport:
    """Fixture for testing LatexReport."""
    return LatexReport(title="Test Report")


class TestLatexReport:
    """Tests for LatexReport class."""

    def test_initialization_without_title(self) -> None:
        """Test that LatexReport initializes with empty content."""
        report = LatexReport()
        assert report.content == ""
        assert report.title is None

    def test_initialization_with_title(self) -> None:
        """Test that LatexReport initializes with title."""
        report = LatexReport(title="Test Title")
        assert report.content == ""
        assert report.title == "Test Title"

    def test_add_text_regular(self, fixture_report: LatexReport) -> None:
        """Test adding regular text."""
        fixture_report.add_text("This is regular text")
        expected = r"\text{This is regular text}" + "\n"
        assert fixture_report.content == expected

    def test_add_text_bold(self, fixture_report: LatexReport) -> None:
        """Test adding bold text."""
        fixture_report.add_text("This is bold text", bold=True)
        expected = r"\textbf{This is bold text}" + "\n"
        assert fixture_report.content == expected

    def test_add_text_italic(self, fixture_report: LatexReport) -> None:
        """Test adding italic text."""
        fixture_report.add_text("This is italic text", italic=True)
        expected = r"\textit{This is italic text}" + "\n"
        assert fixture_report.content == expected

    def test_add_text_bold_and_italic(self, fixture_report: LatexReport) -> None:
        """Test adding bold and italic text."""
        fixture_report.add_text("This is bold and italic", bold=True, italic=True)
        expected = r"\textbf{\textit{This is bold and italic}}" + "\n"
        assert fixture_report.content == expected

    def test_add_text_method_chaining(self, fixture_report: LatexReport) -> None:
        """Test that add_text returns self for method chaining."""
        result = fixture_report.add_text("First").add_text("Second")
        assert result is fixture_report
        assert r"\text{First}" in fixture_report.content
        assert r"\text{Second}" in fixture_report.content

    def test_add_formula_without_tag(self, fixture_report: LatexReport) -> None:
        """Test adding equation without tag."""
        fixture_report.add_formula("a^2+b^2=c^2")
        expected = r"\begin{equation} a^2+b^2=c^2 \end{equation}" + "\n"
        assert fixture_report.content == expected

    def test_add_formula_with_tag(self, fixture_report: LatexReport) -> None:
        """Test adding equation with tag."""
        fixture_report.add_formula("a^2+b^2=c^2", tag="6.83")
        expected = r"\begin{equation} a^2+b^2=c^2 \tag{6.83} \end{equation}" + "\n"
        assert fixture_report.content == expected

    def test_add_formula_method_chaining(self, fixture_report: LatexReport) -> None:
        """Test that add_formula returns self for method chaining."""
        result = fixture_report.add_formula("E=mc^2")
        assert result is fixture_report

    def test_add_formula_inline(self, fixture_report: LatexReport) -> None:
        """Test adding inline equation."""
        fixture_report.add_formula(r"\frac{a}{b}", inline=True)
        expected = r"$\frac{a}{b}$" + "\n"
        assert fixture_report.content == expected

    def test_add_formula_inline_method_chaining(self, fixture_report: LatexReport) -> None:
        """Test that add_formula with inline=True returns self for method chaining."""
        result = fixture_report.add_formula(r"\alpha", inline=True)
        assert result is fixture_report

    def test_add_section(self, fixture_report: LatexReport) -> None:
        """Test adding section."""
        fixture_report.add_section("Introduction")
        expected = r"\section{Introduction}" + "\n"
        assert fixture_report.content == expected

    def test_add_section_method_chaining(self, fixture_report: LatexReport) -> None:
        """Test that add_section returns self for method chaining."""
        result = fixture_report.add_section("Test Section")
        assert result is fixture_report

    def test_add_subsection(self, fixture_report: LatexReport) -> None:
        """Test adding subsection."""
        fixture_report.add_subsection("Background")
        expected = r"\subsection{Background}" + "\n"
        assert fixture_report.content == expected

    def test_add_subsection_method_chaining(self, fixture_report: LatexReport) -> None:
        """Test that add_subsection returns self for method chaining."""
        result = fixture_report.add_subsection("Test Subsection")
        assert result is fixture_report

    def test_add_subsubsection(self, fixture_report: LatexReport) -> None:
        """Test adding subsubsection."""
        fixture_report.add_subsubsection("Details")
        expected = r"\subsubsection{Details}" + "\n"
        assert fixture_report.content == expected

    def test_add_subsubsection_method_chaining(self, fixture_report: LatexReport) -> None:
        """Test that add_subsubsection returns self for method chaining."""
        result = fixture_report.add_subsubsection("Test Subsubsection")
        assert result is fixture_report

    def test_add_table(self, fixture_report: LatexReport) -> None:
        """Test adding table."""
        headers = ["Parameter", "Value", "Unit"]
        rows = [[r"\text{Length}", "10", r"\text{m}"], [r"\text{Density}", "500", r"\text{kg/m$^3$}"]]
        fixture_report.add_table(headers, rows)

        # Check that essential table components are present
        assert r"\begin{table}" in fixture_report.content
        assert r"\end{table}" in fixture_report.content
        assert r"\begin{tabular}{lll}" in fixture_report.content
        assert r"\toprule" in fixture_report.content
        assert r"\midrule" in fixture_report.content
        assert r"\bottomrule" in fixture_report.content
        assert r"Parameter & Value & Unit \\" in fixture_report.content
        assert r"\text{Length} & 10 & \text{m} \\" in fixture_report.content

    def test_add_table_custom_position(self, fixture_report: LatexReport) -> None:
        """Test adding table with custom position."""
        headers = ["A", "B"]
        rows = [["1", "2"]]
        fixture_report.add_table(headers, rows, position="t")
        assert r"\begin{table}[t]" in fixture_report.content

    def test_add_table_no_centering(self, fixture_report: LatexReport) -> None:
        """Test adding table without centering."""
        headers = ["A", "B"]
        rows = [["1", "2"]]
        fixture_report.add_table(headers, rows, centering=False)
        assert r"\centering" not in fixture_report.content

    def test_add_table_method_chaining(self, fixture_report: LatexReport) -> None:
        """Test that add_table returns self for method chaining."""
        result = fixture_report.add_table(["A"], [["1"]])
        assert result is fixture_report

    def test_add_figure(self, fixture_report: LatexReport) -> None:
        """Test adding figure."""
        fixture_report.add_figure("path/to/image.png")

        # Check essential figure components
        assert r"\begin{figure}[h]" in fixture_report.content
        assert r"\centering" in fixture_report.content
        assert r"\includegraphics[width=0.9\textwidth]{path/to/image.png}" in fixture_report.content
        assert r"\end{figure}" in fixture_report.content

    def test_add_figure_custom_width(self, fixture_report: LatexReport) -> None:
        """Test adding figure with custom width."""
        fixture_report.add_figure("image.png", width=0.5)
        assert r"\includegraphics[width=0.5\textwidth]{image.png}" in fixture_report.content

    def test_add_figure_custom_position(self, fixture_report: LatexReport) -> None:
        """Test adding figure with custom position."""
        fixture_report.add_figure("image.png", position="t")
        assert r"\begin{figure}[t]" in fixture_report.content

    def test_add_figure_method_chaining(self, fixture_report: LatexReport) -> None:
        """Test that add_figure returns self for method chaining."""
        result = fixture_report.add_figure("test.png")
        assert result is fixture_report

    def test_add_itemize(self, fixture_report: LatexReport) -> None:
        """Test adding itemized list."""
        items = ["First item", "Second item", "Third item"]
        fixture_report.add_itemize(items)

        assert r"\begin{itemize}" in fixture_report.content
        assert r"\item First item" in fixture_report.content
        assert r"\item Second item" in fixture_report.content
        assert r"\item Third item" in fixture_report.content
        assert r"\end{itemize}" in fixture_report.content

    def test_add_itemize_method_chaining(self, fixture_report: LatexReport) -> None:
        """Test that add_itemize returns self for method chaining."""
        result = fixture_report.add_itemize(["Item"])
        assert result is fixture_report

    def test_add_enumerate(self, fixture_report: LatexReport) -> None:
        """Test adding enumerated list."""
        items = ["First number", "Second number", "Third number"]
        fixture_report.add_enumerate(items)

        assert r"\begin{enumerate}" in fixture_report.content
        assert r"\item First number" in fixture_report.content
        assert r"\item Second number" in fixture_report.content
        assert r"\item Third number" in fixture_report.content
        assert r"\end{enumerate}" in fixture_report.content

    def test_add_enumerate_method_chaining(self, fixture_report: LatexReport) -> None:
        """Test that add_enumerate returns self for method chaining."""
        result = fixture_report.add_enumerate(["Item"])
        assert result is fixture_report

    def test_add_newline_single(self, fixture_report: LatexReport) -> None:
        """Test adding single newline."""
        fixture_report.add_newline()
        expected = r"\newline" + "\n"
        assert fixture_report.content == expected

    def test_add_newline_multiple(self, fixture_report: LatexReport) -> None:
        """Test adding multiple newlines."""
        fixture_report.add_newline(n=4)
        expected = r"\newline\newline\newline\newline" + "\n"
        assert fixture_report.content == expected

    def test_add_newline_method_chaining(self, fixture_report: LatexReport) -> None:
        """Test that add_newline returns self for method chaining."""
        result = fixture_report.add_newline()
        assert result is fixture_report

    def test_to_document_with_instance_title(self, fixture_report: LatexReport) -> None:
        """Test generating document with instance title."""
        fixture_report.add_section("Test Section")
        document = fixture_report.to_document()

        # Check essential document components
        assert r"\documentclass[11pt]{article}" in document
        assert r"\usepackage{amsmath}" in document
        assert r"\usepackage{booktabs}" in document
        assert r"\usepackage{geometry}" in document
        assert r"\usepackage{graphicx}" in document
        assert r"\begin{document}" in document
        assert r"\title{Test Report}" in document
        assert r"\maketitle" in document
        assert r"\section{Test Section}" in document
        assert r"\end{document}" in document

    def test_to_document_with_parameter_title(self, fixture_report: LatexReport) -> None:
        """Test generating document with parameter title overriding instance title."""
        document = fixture_report.to_document(title="Override Title")
        assert r"\title{Override Title}" in document

    def test_to_document_without_title(self) -> None:
        """Test generating document without any title."""
        report = LatexReport()
        document = report.to_document()
        assert r"\title{Untitled}" in document

    def test_to_document_includes_preamble(self, fixture_report: LatexReport) -> None:
        """Test that document includes all necessary preamble packages."""
        document = fixture_report.to_document()

        # Check for blueprint-specific styling
        assert r"\definecolor{blueprintblue}{RGB}{0,40,85}" in document
        assert r"\usepackage{helvet}" in document
        assert r"\usepackage{titlesec}" in document
        assert r"\geometry{a4paper, margin=1in}" in document

    def test_comprehensive_example_from_docstring(self) -> None:
        """Test the comprehensive example from the LatexReport docstring.

        This test reproduces the exact example shown in the class docstring to ensure
        all functionality works together as documented.
        """
        report = LatexReport(title="Sample Report")
        report.add_section("Introduction")
        report.add_subsection("Background")
        report.add_subsubsection("Details")
        report.add_text("This is normal text.")
        report.add_text("This is bold text with newline after.", bold=True).add_newline()
        report.add_text("This is italic text with 4 newlines after.", italic=True).add_newline(n=4)
        report.add_text("This is bold and italic text.", bold=True, italic=True)
        report.add_newline()
        report.add_formula("E=mc^2", tag="3.14")
        report.add_text("Before an inline equation:").add_formula(r"\frac{a}{b}", inline=True).add_text("after the inline equation.").add_newline()
        report.add_text("Equations can also be $a^2 + b^2 = c^2$ inline in the add text method.").add_newline()
        report.add_table(
            headers=["Parameter", "Value", "Unit"], rows=[[r"\text{Length}", "10", r"\text{m}"], [r"\text{Density}", "500", r"\text{kg/m$^3$}"]]
        )
        report.add_figure(r"tomato.png", width=0.2)
        report.add_enumerate(["First item", "Second item"])
        report.add_itemize(["Bullet one", "Bullet two"])
        latex_document = report.to_document()

        # Verify all components are present in the generated document
        assert r"\section{Introduction}" in latex_document
        assert r"\subsection{Background}" in latex_document
        assert r"\subsubsection{Details}" in latex_document
        assert r"\text{This is normal text.}" in latex_document
        assert r"\textbf{This is bold text with newline after.}" in latex_document
        assert r"\textit{This is italic text with 4 newlines after.}" in latex_document
        assert r"\textbf{\textit{This is bold and italic text.}}" in latex_document
        assert r"\begin{equation} E=mc^2 \tag{3.14} \end{equation}" in latex_document
        assert r"$\frac{a}{b}$" in latex_document
        assert r"Parameter & Value & Unit" in latex_document
        assert r"\text{Length} & 10 & \text{m}" in latex_document
        assert r"\includegraphics[width=0.2\textwidth]{tomato.png}" in latex_document
        assert r"\begin{enumerate}" in latex_document
        assert r"\item First item" in latex_document
        assert r"\item Second item" in latex_document
        assert r"\begin{itemize}" in latex_document
        assert r"\item Bullet one" in latex_document
        assert r"\item Bullet two" in latex_document
        assert r"\title{Sample Report}" in latex_document
        assert r"\begin{document}" in latex_document
        assert r"\end{document}" in latex_document

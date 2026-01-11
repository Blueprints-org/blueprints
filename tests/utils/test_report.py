"""Tests for the LatexReport class."""

import tempfile
from pathlib import Path

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import formula_6_5
from blueprints.utils.report import Report


@pytest.fixture
def fixture_report() -> Report:
    """Fixture for testing LatexReport."""
    return Report(title="Test Report")


class TestLatexReport:
    """Tests for LatexReport class."""

    def test_initialization_without_title(self) -> None:
        """Test that LatexReport initializes with empty content."""
        report = Report()
        assert report.content == ""
        assert report.title is None

    def test_initialization_with_title(self) -> None:
        """Test that LatexReport initializes with title."""
        report = Report(title="Test Title")
        assert report.content == ""
        assert report.title == "Test Title"

    def test_add_text_regular(self, fixture_report: Report) -> None:
        """Test adding regular text."""
        fixture_report.add_paragraph("This is regular text")
        expected = r"\txt{This is regular text}" + "\n"
        assert fixture_report.content == expected

    def test_add_text_bold(self, fixture_report: Report) -> None:
        """Test adding bold text."""
        fixture_report.add_paragraph("This is bold text", bold=True)
        expected = r"\textbf{This is bold text}" + "\n"
        assert fixture_report.content == expected

    def test_add_text_italic(self, fixture_report: Report) -> None:
        """Test adding italic text."""
        fixture_report.add_paragraph("This is italic text", italic=True)
        expected = r"\textit{This is italic text}" + "\n"
        assert fixture_report.content == expected

    def test_add_text_bold_and_italic(self, fixture_report: Report) -> None:
        """Test adding bold and italic text."""
        fixture_report.add_paragraph("This is bold and italic", bold=True, italic=True)
        expected = r"\textbf{\textit{This is bold and italic}}" + "\n"
        assert fixture_report.content == expected

    def test_add_text_method_chaining(self, fixture_report: Report) -> None:
        """Test that add_text returns self for method chaining."""
        result = fixture_report.add_paragraph("First").add_paragraph("Second")
        assert result is fixture_report
        assert r"\txt{First}" in fixture_report.content
        assert r"\txt{Second}" in fixture_report.content

    def test_add_equation_without_tag(self, fixture_report: Report) -> None:
        """Test adding equation without tag."""
        fixture_report.add_equation("a^2+b^2=c^2")
        expected = r"\begin{equation} a^2+b^2=c^2 \end{equation}" + "\n"
        assert fixture_report.content == expected

    def test_add_equation_with_tag(self, fixture_report: Report) -> None:
        """Test adding equation with tag."""
        fixture_report.add_equation("a^2+b^2=c^2", tag="6.83")
        expected = r"\begin{equation} a^2+b^2=c^2 \tag{6.83} \end{equation}" + "\n"
        assert fixture_report.content == expected

    def test_add_equation_method_chaining(self, fixture_report: Report) -> None:
        """Test that add_equation returns self for method chaining."""
        result = fixture_report.add_equation("E=mc^2")
        assert result is fixture_report

    def test_add_equation_inline(self, fixture_report: Report) -> None:
        """Test adding inline equation."""
        fixture_report.add_equation(r"\frac{a}{b}", inline=True)
        expected = r"\txt{ $\frac{a}{b}$ }" + "\n"
        assert fixture_report.content == expected

    def test_add_equation_inline_method_chaining(self, fixture_report: Report) -> None:
        """Test that add_equation with inline=True returns self for method chaining."""
        result = fixture_report.add_equation(r"\alpha", inline=True)
        assert result is fixture_report

    def test_add_formula(self, fixture_report: Report) -> None:
        """Test adding formula."""
        fixture_report.add_formula(formula_6_5.Form6Dot5UnityCheckTensileStrength(n_ed=150000, n_t_rd=200000), options="complete")
        expected = r"\begin{equation} CHECK"
        assert expected in fixture_report.content

    def test_add_formula_inline(self, fixture_report: Report) -> None:
        """Test adding inline formula."""
        fixture_report.add_formula(formula_6_5.Form6Dot5UnityCheckTensileStrength(n_ed=150000, n_t_rd=200000), options="short", inline=True)
        expected = r"$CHECK"
        assert expected in fixture_report.content

    def test_add_formula_complete_with_units(self, fixture_report: Report) -> None:
        """Test adding formula with complete_with_units option."""
        fixture_report.add_formula(formula_6_5.Form6Dot5UnityCheckTensileStrength(n_ed=150000, n_t_rd=200000), options="complete_with_units")
        expected = r"\begin{equation} CHECK"
        assert expected in fixture_report.content

    def test_add_section(self, fixture_report: Report) -> None:
        """Test adding section."""
        fixture_report.add_heading("Introduction")
        expected = r"\section{Introduction}" + "\n"
        assert fixture_report.content == expected

    def test_add_section_method_chaining(self, fixture_report: Report) -> None:
        """Test that add_section returns self for method chaining."""
        result = fixture_report.add_heading("Test Section")
        assert result is fixture_report

    def test_add_subsection(self, fixture_report: Report) -> None:
        """Test adding subsection."""
        fixture_report.add_heading("Background", level=2)
        expected = r"\subsection{Background}" + "\n"
        assert fixture_report.content == expected

    def test_add_subsection_method_chaining(self, fixture_report: Report) -> None:
        """Test that add_subsection returns self for method chaining."""
        result = fixture_report.add_heading("Test Subsection", level=2)
        assert result is fixture_report

    def test_add_subsubsection(self, fixture_report: Report) -> None:
        """Test adding subsubsection."""
        fixture_report.add_heading("Details", level=3)
        expected = r"\subsubsection{Details}" + "\n"
        assert fixture_report.content == expected

    def test_add_subsubsection_method_chaining(self, fixture_report: Report) -> None:
        """Test that add_subsubsection returns self for method chaining."""
        result = fixture_report.add_heading("Test Subsubsection", level=3)
        assert result is fixture_report

    def test_add_table(self, fixture_report: Report) -> None:
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

    def test_add_table_no_centering(self, fixture_report: Report) -> None:
        """Test adding table without centering."""
        headers = ["A", "B"]
        rows = [["1", "2"]]
        fixture_report.add_table(headers, rows, centering=False)
        assert r"\centering" not in fixture_report.content

    def test_add_table_method_chaining(self, fixture_report: Report) -> None:
        """Test that add_table returns self for method chaining."""
        result = fixture_report.add_table(["A"], [["1"]])
        assert result is fixture_report

    def test_add_figure(self, fixture_report: Report) -> None:
        """Test adding figure."""
        fixture_report.add_figure("path/to/image.png")

        # Check essential figure components
        assert r"\begin{figure}[h]" in fixture_report.content
        assert r"\centering" in fixture_report.content
        assert r"\includegraphics[width=0.9\textwidth]{path/to/image.png}" in fixture_report.content
        assert r"\end{figure}" in fixture_report.content

    def test_add_figure_custom_width(self, fixture_report: Report) -> None:
        """Test adding figure with custom width."""
        fixture_report.add_figure("image.png", width=0.5)
        assert r"\includegraphics[width=0.5\textwidth]{image.png}" in fixture_report.content

    def test_add_figure_method_chaining(self, fixture_report: Report) -> None:
        """Test that add_figure returns self for method chaining."""
        result = fixture_report.add_figure("test.png")
        assert result is fixture_report

    def test_add_itemize(self, fixture_report: Report) -> None:
        """Test adding itemized list."""
        items = ["First item", "Second item", "Third item"]
        fixture_report.add_list(items, style="bulleted")

        assert r"\begin{itemize}" in fixture_report.content
        assert r"\item First item" in fixture_report.content
        assert r"\item Second item" in fixture_report.content
        assert r"\item Third item" in fixture_report.content
        assert r"\end{itemize}" in fixture_report.content

    def test_add_itemize_nested(self, fixture_report: Report) -> None:
        """Test adding nested itemized list."""
        items = ["Item 1", ["Subitem 1.1", "Subitem 1.2"], "Item 2"]
        fixture_report.add_list(items, style="bulleted")

        assert fixture_report.content.count(r"\begin{itemize}") == 2
        assert r"\item Item 1" in fixture_report.content
        assert r"\item Subitem 1.1" in fixture_report.content
        assert r"\item Subitem 1.2" in fixture_report.content
        assert r"\item Item 2" in fixture_report.content
        assert fixture_report.content.count(r"\end{itemize}") == 2

    def test_add_itemize_method_chaining(self, fixture_report: Report) -> None:
        """Test that add_itemize returns self for method chaining."""
        result = fixture_report.add_list(["Item"], style="bulleted")
        assert result is fixture_report

    def test_add_enumerate(self, fixture_report: Report) -> None:
        """Test adding enumerated list."""
        items = ["First number", "Second number", "Third number"]
        fixture_report.add_list(items, style="numbered")

        assert r"\begin{enumerate}" in fixture_report.content
        assert r"\item First number" in fixture_report.content
        assert r"\item Second number" in fixture_report.content
        assert r"\item Third number" in fixture_report.content
        assert r"\end{enumerate}" in fixture_report.content

    def test_add_enumerate_nested(self, fixture_report: Report) -> None:
        """Test adding nested enumerated list."""
        items = ["Number 1", ["Subnumber 1.1", "Subnumber 1.2"], "Number 2"]
        fixture_report.add_list(items, style="numbered")

        assert fixture_report.content.count(r"\begin{enumerate}") == 2
        assert r"\item Number 1" in fixture_report.content
        assert r"\item Subnumber 1.1" in fixture_report.content
        assert r"\item Subnumber 1.2" in fixture_report.content
        assert r"\item Number 2" in fixture_report.content
        assert fixture_report.content.count(r"\end{enumerate}") == 2

    def test_add_enumerate_method_chaining(self, fixture_report: Report) -> None:
        """Test that add_enumerate returns self for method chaining."""
        result = fixture_report.add_list(["Item"], style="numbered")
        assert result is fixture_report

    def test_add_newline_single(self, fixture_report: Report) -> None:
        """Test adding single newline."""
        fixture_report.add_newline()
        expected = r"\newline" + "\n"
        assert fixture_report.content == expected

    def test_add_newline_multiple(self, fixture_report: Report) -> None:
        """Test adding multiple newlines."""
        fixture_report.add_newline(n=4)
        expected = r"\newline\newline\newline\newline" + "\n"
        assert fixture_report.content == expected

    def test_add_newline_method_chaining(self, fixture_report: Report) -> None:
        """Test that add_newline returns self for method chaining."""
        result = fixture_report.add_newline()
        assert result is fixture_report

    def test_to_document_with_instance_title(self, fixture_report: Report) -> None:
        """Test generating document with instance title."""
        fixture_report.add_heading("Test Section")
        document = fixture_report.to_latex()

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

    def test_to_document_without_title(self) -> None:
        """Test generating document without any title."""
        report = Report()
        document = report.to_latex()
        assert r"\title{}" in document

    def test_to_document_includes_preamble(self, fixture_report: Report) -> None:
        """Test that document includes all necessary preamble packages."""
        document = fixture_report.to_latex()

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
        report = Report(title="Sample Report")
        report.add_heading("Introduction")
        report.add_heading("Background", level=2)
        report.add_heading("Details", level=3)
        report.add_paragraph("This is normal text.")
        report.add_paragraph("This is bold text with newline after.", bold=True).add_newline()
        report.add_paragraph("This is italic text with 4 newlines after.", italic=True).add_newline(n=4)
        report.add_paragraph("This is bold and italic text.", bold=True, italic=True)
        report.add_newline()
        report.add_equation("E=mc^2", tag="3.14")
        report.add_formula(formula_6_5.Form6Dot5UnityCheckTensileStrength(n_ed=150000, n_t_rd=200000), options="complete")
        report.add_paragraph("Before an inline equation:").add_equation(r"\frac{a}{b}", inline=True).add_paragraph(
            "After the inline equation."
        ).add_newline()
        report.add_paragraph("Equations can also be $a^2 + b^2 = c^2$ inline in the add text method.").add_newline()
        report.add_table(
            headers=["Parameter", "Value", "Unit"], rows=[[r"\text{Length}", "10", r"\text{m}"], [r"\text{Density}", "500", r"\text{kg/m$^3$}"]]
        )
        report.add_figure(r"tomato.png", width=0.2)
        report.add_list(["First item", "Second item"], style="numbered")
        report.add_list(["Bullet one", "Bullet two"])
        latex_document = report.to_latex()

        # Verify all components are present in the generated document
        assert r"\section{Introduction}" in latex_document
        assert r"\subsection{Background}" in latex_document
        assert r"\subsubsection{Details}" in latex_document
        assert r"\txt{This is normal text.}" in latex_document
        assert r"\textbf{This is bold text with newline after.}" in latex_document
        assert r"\textit{This is italic text with 4 newlines after.}" in latex_document
        assert r"\textbf{\textit{This is bold and italic text.}}" in latex_document
        assert r"\begin{equation} E=mc^2 \tag{3.14} \end{equation}" in latex_document
        assert r"\begin{equation} CHECK" in latex_document
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

    def test_add_formula_invalid_option(self, fixture_report: Report) -> None:
        """Test that add_formula raises ValueError for invalid option."""
        formula = formula_6_5.Form6Dot5UnityCheckTensileStrength(n_ed=150000, n_t_rd=200000)
        with pytest.raises(ValueError, match="Invalid option"):
            fixture_report.add_formula(formula, options="invalid_option")  # type: ignore[arg-type]

    def test_add_table_empty_headers(self, fixture_report: Report) -> None:
        """Test that add_table raises ValueError for empty headers."""
        with pytest.raises(ValueError, match="At least one header is required"):
            fixture_report.add_table(headers=[], rows=[["1", "2"]])

    def test_add_table_empty_rows(self, fixture_report: Report) -> None:
        """Test that add_table raises ValueError for empty rows."""
        with pytest.raises(ValueError, match="At least one row is required"):
            fixture_report.add_table(headers=["A", "B"], rows=[])

    def test_add_table_column_mismatch(self, fixture_report: Report) -> None:
        """Test that add_table raises ValueError for column mismatch."""
        with pytest.raises(ValueError, match="Row 0 has 2 columns but 3 headers were provided"):
            fixture_report.add_table(
                headers=["A", "B", "C"],
                rows=[["1", "2"]],
            )

    def test_add_figure_with_caption(self, fixture_report: Report) -> None:
        """Test adding figure with caption."""
        fixture_report.add_figure("image.png", caption="Test caption")
        assert r"\caption{Test caption}" in fixture_report.content
        assert r"\begin{figure}" in fixture_report.content

    def test_repr_empty_report(self) -> None:
        """Test repr of empty report."""
        report = Report(title="Test")
        repr_str = repr(report)
        assert "LatexReport" in repr_str
        assert 'title="Test"' in repr_str
        assert "sections=0" in repr_str

    def test_repr_with_content(self) -> None:
        """Test repr of report with content."""
        report = Report(title="Report")
        report.add_heading("Intro")
        report.add_equation("a=b")
        report.add_table(headers=["X"], rows=[["1"]])
        repr_str = repr(report)
        assert "sections=1" in repr_str
        assert "equations=1" in repr_str
        assert "tables=1" in repr_str

    def test_str_representation(self, fixture_report: Report) -> None:
        """Test string representation of report."""
        fixture_report.add_heading("Section 1")
        fixture_report.add_heading("Subsection 1", level=2)
        fixture_report.add_equation("x = y")
        str_repr = str(fixture_report)
        assert "LaTeX Report: Test Report" in str_repr
        assert "Sections:      1" in str_repr
        assert "Subsections:   1" in str_repr
        assert "Equations:     1" in str_repr
        assert "to_latex()" in str_repr
        assert "to_word()" in str_repr

    def test_str_representation_untitled(self) -> None:
        """Test string representation of untitled report."""
        report = Report()
        str_repr = str(report)
        assert "LaTeX Report: (untitled)" in str_repr

    def test_to_latex_returns_string_when_path_is_none(self) -> None:
        """Test that to_latex() returns string when path is None."""
        report = Report(title="Test Report")
        report.add_heading("Introduction")
        report.add_paragraph("Some test content")

        # Call without path argument
        result = report.to_latex()

        # Verify result is string
        assert isinstance(result, str)
        assert len(result) > 0
        # Verify it's a valid LaTeX document
        assert r"\documentclass" in result
        assert r"\begin{document}" in result
        assert r"\end{document}" in result

    def test_to_latex_with_file_path_string(self) -> None:
        """Test that to_latex() saves to file when given a string path."""
        report = Report(title="Test Report")
        report.add_heading("Introduction")
        report.add_paragraph("Some test content")

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = str(Path(tmpdir) / "report.tex")

            # Call with file path
            result = report.to_latex(file_path)

            # Verify return value is None
            assert result is None

            # Verify file was created
            assert Path(file_path).exists()

            # Verify file contains valid LaTeX
            content = Path(file_path).read_text(encoding="utf-8")
            assert r"\documentclass" in content
            assert r"\begin{document}" in content
            assert "Introduction" in content

    def test_to_latex_with_pathlib_path(self) -> None:
        """Test that to_latex() saves to file when given a Path object."""
        report = Report(title="Test Report")
        report.add_heading("Introduction")
        report.add_paragraph("Some test content")

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "report.tex"

            # Call with Path object
            result = report.to_latex(file_path)

            # Verify return value is None
            assert result is None

            # Verify file was created
            assert file_path.exists()

            # Verify file contains valid LaTeX
            content = file_path.read_text(encoding="utf-8")
            assert r"\documentclass" in content
            assert r"\begin{document}" in content
            assert "Introduction" in content

    def test_to_latex_file_with_language_translation(self) -> None:
        """Test that to_latex() saves translated content to file."""
        report = Report(title="Test Report")
        report.add_heading("Introduction")
        report.add_paragraph("Some test content")

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = str(Path(tmpdir) / "report_zh.tex")

            # Call with path and language translation
            result = report.to_latex(file_path, language="zh")

            # Verify return value is None
            assert result is None

            # Verify file was created
            assert Path(file_path).exists()

            # Verify file contains LaTeX (may be translated)
            content = Path(file_path).read_text(encoding="utf-8")
            assert r"\documentclass" in content
            assert r"\begin{document}" in content

"""Tests for the Report class."""

import subprocess
import tempfile
from collections.abc import Callable
from pathlib import Path

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import formula_6_5
from blueprints.utils.report import Report


@pytest.fixture
def mock_run(monkeypatch: pytest.MonkeyPatch) -> Callable[[str], None]:  # noqa: C901
    """Fixture for mocking subprocess.run with different behaviors."""

    def _mock_run(behavior: str = "success") -> None:  # noqa: C901
        """
        Create a mock_run function based on the specified behavior.

        Args:
            behavior: Type of mock behavior. Options are:
                - "not_available": Raise FileNotFoundError
                - "success": Return successful completion and create mock PDF
                - "fail_compilation": Succeed on version check, fail on compilation
        """
        if behavior == "not_available":

            def mock_func(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess:  # type: ignore[type-arg]
                raise FileNotFoundError("pdflatex not found")
        elif behavior == "success":

            def mock_func(*_args: object, **kwargs: object) -> subprocess.CompletedProcess:  # type: ignore[type-arg]
                if kwargs.get("capture_output") and kwargs.get("check"):
                    # This is the version check call
                    return subprocess.CompletedProcess(args=[], returncode=0, stdout=b"pdfTeX 3.14159265-2.6-1.40.21")
                # This is the pdflatex compilation call - create the mock PDF
                if "cwd" in kwargs:
                    pdf_path = Path(kwargs["cwd"]) / "report.pdf"  # type: ignore[arg-type]
                    pdf_path.write_bytes(b"%PDF-1.4 mock content")
                return subprocess.CompletedProcess(args=[], returncode=0)
        elif behavior == "fail_compilation":
            call_count = [0]

            def mock_func(*_args: object, **kwargs: object) -> subprocess.CompletedProcess:  # type: ignore[type-arg]
                call_count[0] += 1
                if call_count[0] == 1 and kwargs.get("capture_output") and kwargs.get("check"):
                    return subprocess.CompletedProcess(args=[], returncode=0, stdout=b"pdfTeX 3.14159265")
                return subprocess.CompletedProcess(args=[], returncode=1, stderr=b"LaTeX error")
        else:

            def mock_func(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess:  # type: ignore[type-arg]
                return subprocess.CompletedProcess(args=[], returncode=0)

        monkeypatch.setattr(subprocess, "run", mock_func)

    return _mock_run


@pytest.fixture
def fixture_report() -> Report:
    """Fixture for testing Report."""
    return Report(title="Test Report")


class TestReport:
    """Tests for Report class."""

    def test_initialization_without_title(self) -> None:
        """Test that Report initializes with empty content."""
        report = Report()
        assert report.content == ""
        assert report.title == ""

    def test_initialization_with_title(self) -> None:
        """Test that Report initializes with title."""
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

    def test_multline_add_text_calls(self, fixture_report: Report) -> None:
        """Test multline add_text calls."""
        fixture_report.add_paragraph("First line.Second line.")
        expected = r"\txt{First line.Second line.}" + "\n"
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
        expected = r"\begin{multline} a^2+b^2=c^2 \notag \end{multline}" + "\n"
        assert fixture_report.content == expected

    def test_add_equation_with_tag(self, fixture_report: Report) -> None:
        """Test adding equation with tag."""
        fixture_report.add_equation("a^2+b^2=c^2", tag="6.83")
        expected = r"\begin{multline} a^2+b^2=c^2 \tag{6.83} \end{multline}" + "\n"
        assert fixture_report.content == expected

    def test_very_long_equation_splitting(self, fixture_report: Report) -> None:
        """Test adding a very long equation that requires splitting."""
        long_equation = "a = b + c + d + e + f + g + h + i + j + k + l + m + n + o + p + q + r + s + t + u + v + w + x + y + z"
        fixture_report.add_equation(long_equation, split_after=[(3, "+"), (6, "+"), (9, "+")])
        expected_parts = [
            r"\begin{multline} a = b + c + d + \\",
            r"e + f + g + \\",
            r"h + i + j + \\",
            r"k + l + m + n + o + p + q + r + s + t + u + v + w + x + y + z \notag \end{multline}",
        ]
        for part in expected_parts:
            assert part in fixture_report.content

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
        expected = r"\begin{multline} CHECK"
        assert expected in fixture_report.content

    def test_add_formula_inline(self, fixture_report: Report) -> None:
        """Test adding inline formula."""
        fixture_report.add_formula(formula_6_5.Form6Dot5UnityCheckTensileStrength(n_ed=150000, n_t_rd=200000), options="short", inline=True)
        expected = r"$CHECK"
        assert expected in fixture_report.content

    def test_add_formula_complete_with_units(self, fixture_report: Report) -> None:
        """Test adding formula with complete_with_units option."""
        fixture_report.add_formula(formula_6_5.Form6Dot5UnityCheckTensileStrength(n_ed=150000, n_t_rd=200000), options="complete_with_units")
        expected = r"\begin{multline} CHECK"
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
        assert r"\begin{figure}" in fixture_report.content
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
        assert r"\begin{multline} E=mc^2 \tag{3.14} \end{multline}" in latex_document
        assert r"\begin{multline} CHECK" in latex_document
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
        assert "LaTeX Report: " in str_repr

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

    def test_add_heading_invalid_level(self) -> None:
        """Test that add_heading raises ValueError for invalid level."""
        report = Report(title="Test Report")
        with pytest.raises(ValueError, match="Invalid heading level"):
            report.add_heading("Invalid", level=4)

    def test_add_list_invalid_style(self) -> None:
        """Test that add_list raises ValueError for invalid style."""
        report = Report(title="Test Report")
        with pytest.raises(ValueError, match="Invalid style"):
            report.add_list(["Item 1", "Item 2"], style="invalid")

    def test_to_pdf_pdflatex_not_available(self, fixture_report: Report, mock_run: Callable[[str], None]) -> None:
        """Test that to_pdf raises RuntimeError when pdflatex is not available."""
        mock_run("not_available")

        with pytest.raises(RuntimeError, match="pdflatex is not installed"):
            fixture_report.to_pdf()

    def test_to_pdf_returns_bytes_when_path_is_none(self, fixture_report: Report, mock_run: Callable[[str], None]) -> None:
        """Test that to_pdf() returns bytes when path is None."""
        mock_run("success")

        fixture_report.add_heading("Test")

        result = fixture_report.to_pdf()

        assert isinstance(result, bytes)
        assert len(result) > 0
        assert result.startswith(b"%PDF")

    def test_to_pdf_saves_to_file_with_string_path(self, fixture_report: Report, mock_run: Callable[[str], None]) -> None:
        """Test that to_pdf() saves to file when given a string path."""
        mock_run("success")

        fixture_report.add_heading("Test")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = str(Path(tmpdir) / "output.pdf")

            result = fixture_report.to_pdf(output_path)

            assert result is None
            assert Path(output_path).exists()

    def test_to_pdf_saves_to_file_with_pathlib_path(self, fixture_report: Report, mock_run: Callable[[str], None]) -> None:
        """Test that to_pdf() saves to file when given a Path object."""
        mock_run("success")

        fixture_report.add_heading("Test")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.pdf"

            result = fixture_report.to_pdf(output_path)

            assert result is None
            assert output_path.exists()

    def test_to_pdf_compilation_fails(self, fixture_report: Report, mock_run: Callable[[str], None]) -> None:
        """Test that to_pdf raises RuntimeError when pdflatex compilation fails."""
        mock_run("fail_compilation")

        fixture_report.add_heading("Test")

        with pytest.raises(RuntimeError, match="pdflatex compilation failed"):
            fixture_report.to_pdf()

    def test_to_pdf_with_language_parameter(self, fixture_report: Report, mock_run: Callable[[str], None]) -> None:
        """Test that to_pdf() accepts language parameter."""
        mock_run("success")

        fixture_report.add_heading("Test")

        result = fixture_report.to_pdf(language="zh")

        assert isinstance(result, bytes)

    def test_to_pdf_cleanup_true_removes_temp_files(self, fixture_report: Report, mock_run: Callable[[str], None]) -> None:
        """Test that to_pdf() with cleanup=True removes temporary files."""
        mock_run("success")

        fixture_report.add_heading("Test")

        # With cleanup=True (default), temp directory is removed automatically by context manager
        result = fixture_report.to_pdf(cleanup=True)
        assert isinstance(result, bytes)

    def test_to_pdf_cleanup_false_preserves_temp_files(self, fixture_report: Report, mock_run: Callable[[str], None]) -> None:
        """Test that to_pdf() with cleanup=False preserves temporary files."""
        mock_run("success")

        fixture_report.add_heading("Test")

        result = fixture_report.to_pdf(cleanup=False)
        assert isinstance(result, bytes)

    def test_adding_two_reports_together(self) -> None:
        """Test that two Report instances can be added together."""
        report1 = Report(title="Report 1")
        report1.add_heading("Introduction")
        report1.add_paragraph("Content for report 1.")

        report2 = Report(title="Report 2")
        report2.add_heading("Overview")
        report2.add_paragraph("Content for report 2.")

        report3 = Report(title="Report 3")
        report3.add_heading("Summary")
        report3.add_paragraph("Content for report 3.")

        final_report = report1 + report2 + report3

        assert isinstance(final_report, Report)
        assert final_report.title == "Report 1"
        assert "Content for report 1." in final_report.content
        assert "Content for report 2." in final_report.content
        assert "Content for report 3." in final_report.content

    def test_adding_report_with_non_report_raises_type_error(self) -> None:
        """Test that adding a Report with a non-Report raises TypeError."""
        report = Report(title="Main Report")
        report.add_heading("Main Section")

        with pytest.raises(TypeError, match=r"unsupported operand type\(s\) for \+: 'Report' and 'str'"):
            _ = report + "Not a Report"

    def test_adding_reports_first_has_no_title(self) -> None:
        """Test adding reports where the first report has no title (None)."""
        report1 = Report()  # No title
        report1.add_heading("Chapter 1")

        report2 = Report(title="Should Be Ignored")
        report2.add_heading("Chapter 2")

        combined = report1 + report2

        assert combined.title == ""
        assert "Chapter 1" in combined.content
        assert "Chapter 2" in combined.content

    def test_adding_empty_reports(self) -> None:
        """Test adding completely empty reports (no content)."""
        report1 = Report(title="Empty Report")
        report2 = Report()

        combined = report1 + report2

        assert combined.title == "Empty Report"
        assert combined.content == ""

    def test_adding_report_with_title_to_report_without_title(self) -> None:
        """Test that title=None is preserved when left operand has no title."""
        report_no_title = Report()
        report_no_title.add_paragraph("No title content")

        report_with_title = Report(title="Has Title")
        report_with_title.add_paragraph("Titled content")

        combined = report_no_title + report_with_title

        assert combined.title == ""
        assert "No title content" in combined.content
        assert "Titled content" in combined.content

    def test_adding_reports_does_not_mutate_originals(self) -> None:
        """Test that original reports are not mutated after addition."""
        report1 = Report(title="Original 1")
        report1.add_heading("Section 1")
        original_content1 = report1.content
        original_title1 = report1.title

        report2 = Report(title="Original 2")
        report2.add_heading("Section 2")
        original_content2 = report2.content
        original_title2 = report2.title

        _ = report1 + report2

        # Verify originals are unchanged
        assert report1.content == original_content1
        assert report1.title == original_title1
        assert report2.content == original_content2
        assert report2.title == original_title2

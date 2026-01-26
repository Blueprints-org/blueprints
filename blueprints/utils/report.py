"""Report builder for LaTeX documents.

This module provides functionality for creating structured LaTeX reports programmatically.
The Report class offers a fluent API for building documents with headings, paragraphs,
equations, tables, figures, and lists. Reports can be exported to LaTeX format for
compilation with pdflatex, compiled directly to PDF, or converted to Word documents.

Key Features:
    - Fluent API with method chaining for easy document construction
    - Support for mathematical equations using LaTeX syntax
    - Integration with Blueprints Formula objects
    - Table and figure insertion with customizable formatting
    - Nested bulleted and numbered lists
    - Export to LaTeX (.tex), PDF (.pdf), and Word (.docx) formats
    - Multi-language support through translation

Developer notes:
    The LaTeX styling is designed to match Word document styling as closely as possible.
    Changes to LaTeX output should be reflected in _report_to_word.py converter.

"""

import subprocess
import tempfile
from collections.abc import Sequence
from dataclasses import dataclass, field
from io import BytesIO
from pathlib import Path
from typing import Any, Literal, Self

from blueprints.codes.formula import Formula


@dataclass
class Report:
    r"""Report builder for creating structured documents with standardized formatting.

    Check our docs for examples of usage.

    Parameters
    ----------
    title : str, optional
        The title of the report.

    Examples
    --------
    >>> report = Report(title="Sample Report")
    >>> report.add_heading("Introduction")
    >>> report.add_heading("Background", level=2)
    >>> report.add_heading("Details", level=3)
    >>> report.add_paragraph("This is normal text.")
    >>> report.add_paragraph("This is bold text with newline after.", bold=True).add_newline()
    >>> report.add_paragraph("This is italic text with 4 newlines after.", italic=True).add_newline(n=4)
    >>> report.add_paragraph("This is bold and italic text.", bold=True, italic=True)
    >>> report.add_newline()
    >>> report.add_equation("E=mc^2", tag="3.14")
    >>> report.add_paragraph("Before inline equation:", italic=True).add_equation(r"\frac{a}{b}", inline=True).add_paragraph(
    ...     " and after inline equation.", bold=True
    ... ).add_newline()
    >>> report.add_equation(r"e^{i \pi} + 1 = 0", inline=True).add_paragraph("inline can be at start of text.").add_newline()
    >>> report.add_paragraph("Or at the end of text", bold=True).add_equation(r"\int_a^b f(x) dx", inline=True).add_newline(n=2)
    >>> report.add_paragraph("Equations can also be $a^2 + b^2 = c^2$ inline in the add text method.").add_newline()
    >>> report.add_table(
    ...     headers=["Parameter", "Value", "Unit"], rows=[[r"\text{Length}", "10", r"\text{m}"], [r"\text{Density}", "500", r"\text{kg/$m^3$}"]]
    ... )
    >>> report.add_figure(r"tomato.png", width=0.2)  # needs the tomato.png file in working directory
    >>> report.add_list(["First item", "Second item"], style="numbered")
    >>> report.add_list(["Layer one", ["Layer two", ["Layer three", ["Layer four"]]]], style="numbered")
    >>> report.add_list(["Bullet one", "Bullet two"], style="bulleted")
    >>> latex_document = report.to_latex()
    >>> print(latex_document)  # prints the complete LaTeX document string, which can be compiled with pdflatex in for example Overleaf.
    """

    title: str = ""
    content: str = field(default="", init=False)

    def add_paragraph(self, text: str, bold: bool = False, italic: bool = False) -> Self:
        r"""Add text with optional bold and italic formatting.

        Parameters
        ----------
        text : str
            The text content of the paragraph.
        bold : bool, optional
            Whether to format the text in bold.
        italic : bool, optional
            Whether to format the text in italics.

        Returns
        -------
        Report
            Returns self for method chaining.

        Examples
        --------
        >>> report = Report()
        >>> report.add_paragraph("This is regular text")
        >>> report.add_paragraph("This is bold text", bold=True)
        >>> report.add_paragraph("This is bold and italic", bold=True, italic=True)
        """
        if bold and italic:
            self.content += rf"\textbf{{\textit{{{text}}}}}"
        elif bold:
            self.content += rf"\textbf{{{text}}}"
        elif italic:
            self.content += rf"\textit{{{text}}}"
        else:
            self.content += rf"\txt{{{text}}}"

        # Add a newline for visual separation
        self.content += "\n"

        return self

    def add_equation(
        self,
        equation: str,
        tag: str | None = None,
        inline: bool = False,
    ) -> Self:
        r"""Add an equation to the report. For adding Blueprints formulas, use add_formula instead.

        Parameters
        ----------
        equation : str
            An equation in LaTeX format.
        tag : str or None, optional
            Tag to label the equation (e.g., "6.83", "EN 1992-1-1:2004 6.6n", etc.).
        inline : bool, optional
            Whether to add the equation inline (meaning within text) or as a separate equation block. Default is False.

        Returns
        -------
        Report
            Returns self for method chaining.

        Examples
        --------
        When creating a report, you can add equations in different ways:
        >>> report = Report()
        >>> report.add_equation("a^2+b^2=c^2")
        >>> report.add_equation("a^2+b^2=c^2", tag="6.83")
        >>> report.add_equation(r"\\frac{a}{b}", inline=True)

        """
        if inline:
            self.content += r"\txt{ " + rf"${equation}$" + f"{f' ({tag})' if tag else ''}" + r" }"
        elif tag:
            self.content += rf"\begin{{equation}} {equation} \tag{{{tag}}} \end{{equation}}"
        else:
            self.content += rf"\begin{{equation}} {equation} \end{{equation}}"

        # Add a newline for visual separation
        self.content += "\n"

        return self

    def add_formula(
        self,
        formula: Formula,
        options: Literal["short", "complete", "complete_with_units"] = "complete",
        include_source: bool = True,
        include_formula_number: bool = True,
        inline: bool = False,
    ) -> Self:
        r"""Add a Blueprints formula to the report, for generic equations, use add_equation.

        Parameters
        ----------
        formula : Formula
            Use any Blueprints Formula object.
        options : Literal["short", "complete", "complete_with_units"]
            The representation of the formula to add.
            short - Minimal representation (symbol = result [unit])
            complete - Complete representation (symbol = equation = numeric_equation = result [unit])
            complete_with_units - Complete representation with units (symbol = equation = numeric_equation_with_units [unit] = result [unit])
        include_source: bool, optional
            If True, includes the source document in the equation tag. Default is True.
            For example: "EN 1993-1-1:2005" or "EN 1992-1-1:2004".
        include_formula_number: bool, optional
            If True, includes the formula number in the equation tag. Default is True.
            For example: "6.5" or "6.6n".
        inline : bool, optional
            Whether to add the formula inline (meaning within text) or as a separate equation block (default).

        Returns
        -------
        Report
            Returns self for method chaining.

        Examples
        --------
        >>> from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import formula_6_5
        >>> formula = formula_6_5.Form6Dot5UnityCheckTensileStrength(n_ed=150000, n_t_rd=200000)
        >>> report = Report()
        >>> report.add_formula(formula, options="short")  # Minimal representation
        >>> print(report)
        # report can be converted to formatted LaTeX document with report.to_document()
        >>> print(report.to_latex())
        """
        # Get the desired LaTeX representation from the formula
        latex = formula.latex()

        # define the equation string based on options
        equation_str: str = ""
        match options.lower():
            case "short":
                equation_str = latex.short
            case "complete":
                equation_str = latex.complete
            case "complete_with_units":
                equation_str = latex.complete_with_units
            case _:
                raise ValueError(f"Invalid option '{options}'. Choose from 'short', 'complete', or 'complete_with_units'.")

        # Build tag from include_source and include_formula_number flags
        tag_parts = []
        if include_source or include_formula_number:
            if include_source:
                tag_parts.append(formula.source_document)
            if include_formula_number:
                tag_parts.append(formula.label)
        tag_str = " ".join(tag_parts).strip()

        return self.add_equation(equation=equation_str, inline=inline, tag=tag_str or None)

    def add_heading(self, text: str, level: int = 1) -> Self:
        """Add a heading to the report.

        Currently, supports levels 1 (section), 2 (subsection), and 3 (subsubsection).

        Parameters
        ----------
        text : str
            The heading text.
        level : int
            The heading level (1 for section, 2 for subsection, 3 for subsubsection). Default is 1.

        Returns
        -------
        Report
            Returns self for method chaining.

        Examples
        --------
        >>> report = Report()
        >>> report.add_heading("This is a section")
        """
        match level:
            case 1:
                self.content += rf"\section{{{text}}}"
            case 2:
                self.content += rf"\subsection{{{text}}}"
            case 3:
                self.content += rf"\subsubsection{{{text}}}"
            case _:
                raise ValueError(f"Invalid heading level '{level}'. Choose from 1 (section), 2 (subsection), or 3 (subsubsection).")

        # Add a newline for visual separation
        self.content += "\n"

        return self

    def add_table(
        self,
        headers: list[str],
        rows: list[list[str]],
        centering: bool = True,
    ) -> Self:
        r"""Add a table to the report.

        Parameters
        ----------
        headers : list[str]
            List of column headers.
        rows : list[list[str]]
            List of rows, where each row is a list of cell values.
        centering : bool, optional
            If True, centers the table. Default is True.

        Returns
        -------
        Report
            Returns self for method chaining.

        Examples
        --------
        >>> report = Report()
        >>> headers = ["Check", "Utilization", "Status"]
        >>> rows = [[r"\\text{Concrete strut capacity}", "0.588", r"\\text{PASS}"], [r"\\text{Torsion moment capacity}", "4.825", r"\\text{FAIL}"]]
        >>> report.add_table(headers, rows)
        """
        # Validate headers and rows match
        num_cols = len(headers)

        if not headers:
            raise ValueError("At least one header is required.")
        if not rows:
            raise ValueError("At least one row is required.")

        for i, row in enumerate(rows):
            if len(row) != num_cols:
                raise ValueError(
                    f"Row {i} has {len(row)} columns but {num_cols} headers were provided. All rows must have the same number of columns as headers."
                )

        col_spec = "l" * num_cols

        # Build header row
        header_row = " & ".join(headers) + r" \\"

        # Build data rows
        data_rows = " ".join([" & ".join(row) + r" \\" for row in rows])

        # Build table
        centering_cmd = r"\centering " if centering else ""
        table = (
            rf"\begin{{table}}[h] {centering_cmd}"
            rf"\begin{{tabular}}{{{col_spec}}} "
            rf"\toprule {header_row} \midrule {data_rows} "
            rf"\bottomrule \end{{tabular}} \end{{table}}"
        )
        self.content += table

        # Add a newline for visual separation
        self.content += "\n"

        return self

    def add_figure(
        self,
        image_path: str,
        width: float = 0.9,
        caption: str | None = None,
    ) -> Self:
        r"""Adds a figure to the report.

        Parameters
        ----------
        image_path : str
            Path to the image file.
        width : float, optional
            Width specification for the image as ratio of the text width. Default is 0.9.
        caption : str, optional
            Caption text for the figure. Will be displayed below the image. Default is None.

        Returns
        -------
        Report
            Returns self for method chaining.

        Examples
        --------
        >>> report = Report()
        >>> report.add_figure("path_to_image")
        >>> report.add_figure("path_to_image", width=0.5)
        >>> report.add_figure("plot.png", caption="Results of the analysis")
        """
        # Convert Windows backslashes to forward slashes for LaTeX compatibility
        latex_image_path = image_path.replace("\\", "/")

        # Build the figure environment
        figure_parts = [r"\begin{figure}[h] \centering ", rf"\includegraphics[width={width}\textwidth]{{{latex_image_path}}} "]

        # Add optional caption
        if caption:
            figure_parts.append(rf"\caption{{{caption}}} ")

        figure_parts.append(r"\end{figure}")

        figure = "".join(figure_parts)
        self.content += figure

        # Add a newline for visual separation
        self.content += "\n"

        return self

    def add_list(self, items: Sequence[Any], style: Literal["bulleted", "numbered"] = "bulleted") -> Self:
        """Add a list to the report, either bulleted or numbered.

        Parameters
        ----------
        items : Sequence[Any]
            List of items to display.
        style : Literal["bulleted", "numbered"], optional
            Style of the list, either 'bulleted' for itemize or 'numbered' for enumerate. Default is 'bulleted'.

        Returns
        -------
        Report
            Returns self for method chaining.

        Examples
        --------
        >>> report = Report()
        >>> report.add_list(["Item 1", "Item 2", "Item 3"], style="bulleted")
        >>> report.add_list(["First", "Second", "Third"], style="numbered")
        """
        if style.lower() not in ["bulleted", "numbered"]:
            raise ValueError(f"Invalid style '{style}'. Choose 'bulleted' or 'numbered'.")

        def _build_list(item_list: list, depth: int = 0) -> str:
            r"""Recursively build LaTeX environment for nested lists.

            Parameters
            ----------
            item_list : list
                List of items to convert to LaTeX. Items can be strings or nested lists.
            depth : int, optional
                Current nesting depth (used for recursion tracking). Default is 0.

            Returns
            -------
            str
                LaTeX string with \\begin{itemize}/\\begin{enumerate} environment.
            """
            result = r"\begin{itemize} " if style.lower() == "bulleted" else r"\begin{enumerate} "
            for item in item_list:
                if isinstance(item, list):
                    result += _build_list(item, depth + 1)
                else:
                    result += rf"\item {item} "
            result += r"\end{itemize} " if style.lower() == "bulleted" else r"\end{enumerate} "
            return result

        self.content += _build_list(list(items))

        # Add a newline for visual separation
        self.content += "\n"

        return self

    def add_newline(self, n: int = 1) -> Self:
        """Add one or more newlines to separate content.

        Useful for adding vertical spacing between paragraphs, equations, or other elements.

        Parameters
        ----------
        n : int, optional
            Number of newlines to add. Default is 1.

        Returns
        -------
        Report
            Returns self for method chaining.

        Examples
        --------
        >>> report = Report()
        >>> report.add_newline()
        """
        self.content += r"\newline" * n

        # Add a newline for visual separation
        self.content += "\n"

        return self

    def __add__(self, other: "Report") -> "Report":
        """Combine two reports into a new report.

        The resulting report will have the title of the first (left) report
        and the combined content of both reports.

        Parameters
        ----------
        other : Report
            The report to add to this one.

        Returns
        -------
        Report
            A new Report with combined content.

        Raises
        ------
        TypeError
            If the other object is not a Report instance.

        Examples
        --------
        >>> report1 = Report(title="Part 1")
        >>> report1.add_heading("Introduction")
        Report(title="Part 1", sections=1, subsections=0, equations=0, tables=0, figures=0, lists=0, chars=26)
        >>> report2 = Report(title="Part 2")
        >>> report2.add_heading("Conclusion")
        Report(title="Part 2", sections=1, subsections=0, equations=0, tables=0, figures=0, lists=0, chars=23)
        >>> combined = report1 + report2
        >>> combined.title
        'Part 1'
        """
        if not isinstance(other, Report):
            raise TypeError(f"unsupported operand type(s) for +: 'Report' and '{type(other).__name__}'")
        result = Report(title=self.title)
        result.content = self.content + other.content
        return result

    def __repr__(self) -> str:
        """Return a concise representation showing report structure and content summary."""
        sections = self.content.count(r"\section{")
        subsections = self.content.count(r"\subsection{")
        equations = self.content.count(r"\begin{equation}")
        tables = self.content.count(r"\begin{table}")
        figures = self.content.count(r"\begin{figure}")
        lists = self.content.count(r"\begin{itemize}") + self.content.count(r"\begin{enumerate}")

        title_str = f'title="{self.title}"'
        stats = (
            f"sections={sections}, subsections={subsections}, "
            f"equations={equations}, tables={tables}, figures={figures}, "
            f"lists={lists}, chars={len(self.content)}"
        )

        return f"LatexReport({title_str}, {stats})"

    def __str__(self) -> str:
        """Return a human-readable representation of the report structure and content."""
        sections = self.content.count(r"\section{")
        subsections = self.content.count(r"\subsection{")
        equations = self.content.count(r"\begin{equation}")
        tables = self.content.count(r"\begin{table}")
        figures = self.content.count(r"\begin{figure}")
        lists = self.content.count(r"\begin{itemize}") + self.content.count(r"\begin{enumerate}")

        lines = [
            "=" * 60,
            f"LaTeX Report: {self.title}",
            "=" * 60,
            f"Sections:      {sections}",
            f"Subsections:   {subsections}",
            f"Equations:     {equations}",
            f"Tables:        {tables}",
            f"Figures:       {figures}",
            f"Lists:         {lists}",
            f"Content size:  {len(self.content)} characters",
            "=" * 60,
            "Use .to_latex() to generate the full LaTeX document,",
            ".to_pdf() to compile to PDF (requires pdflatex),",
            "or .to_word() to convert to a Word document.",
            "=" * 60,
        ]

        return "\n".join(lines)

    def to_latex(self, path: str | Path | None = None, language: str = "en") -> str | None:
        """Generate a complete LaTeX document with proper preamble and structure.

        You could compile the output with pdflatex in for example Overleaf.

        Parameters
        ----------
        path : str | Path | None, optional
            The destination for the LaTeX document:
            - str or Path: File path where the .tex file will be saved
            - None: Return the document as a string (default)
        language : str, optional
            Language code for localization, full list on https://docs.cloud.google.com/translate/docs/languages
            Warning: only English is officially supported in Blueprints (default is "en" for English).

        Returns
        -------
        str | None
            If path is None, returns the LaTeX document as a string.
            If path is provided (str or Path), returns None after saving to file.

        Examples
        --------
        Get LaTeX as a string:

        >>> report = Report(title="My Report")
        >>> report.add_heading("Introduction")
        >>> report.add_paragraph("Some text")
        >>> latex_doc = report.to_latex()

        Save directly to a file:

        >>> report.to_latex("report.tex")

        Save using pathlib.Path:

        >>> from pathlib import Path
        >>> report.to_latex(Path("report.tex"))
        """
        # Build the preamble with styling to match Word document converter (pdflatex compatible)
        preamble = (
            r"\documentclass[11pt]{article}" + "\n"
            # Required packages
            r"\usepackage{amsmath}" + "\n"  # Advanced math environments and symbols
            r"\usepackage{booktabs}" + "\n"  # Professional-looking tables with \toprule, \midrule, \bottomrule
            r"\usepackage{geometry}" + "\n"  # Page layout and margins
            r"\usepackage{graphicx}" + "\n"  # Include images and graphics
            r"\usepackage{setspace}" + "\n"  # Line spacing control
            r"\usepackage{xcolor}" + "\n"  # Color definitions and usage
            r"\usepackage{titlesec}" + "\n"  # Customize section titles
            r"\usepackage{helvet}" + "\n"  # Helvetica font family (sans-serif)
            r"\usepackage[T1]{fontenc}" + "\n"  # Better font encoding for special characters
            r"\usepackage{enumitem}" + "\n"  # Enhanced list customization
            # Page setup
            r"\geometry{a4paper, margin=1in}" + "\n"  # A4 paper with 1-inch margins
            r"\setstretch{1.3}" + "\n"  # Line spacing factor
            "\n"
            # Custom commands
            r"\newcommand{\txt}[1]{#1}" + "\n"  # Simple text wrapper command
            # Spacing configuration
            r"\setlength{\parskip}{0pt}" + "\n"  # No extra space between paragraphs
            r"\setlength{\abovedisplayskip}{12pt}" + "\n"  # Space above equations
            r"\setlength{\belowdisplayskip}{12pt}" + "\n"  # Space below equations
            r"\setlist{nosep}" + "\n"  # Remove extra spacing in lists
            "\n"
            # Color definitions
            r"\definecolor{blueprintblue}{RGB}{0,40,85}" + "\n"  # Custom blue color (0, 40, 85)
            "\n"
            # Title formatting
            r"\makeatletter" + "\n"  # Access internal LaTeX commands
            r"\renewcommand{\maketitle}{%" + "\n"  # Redefine \maketitle command
            r"    \begin{center}%" + "\n"  # Center the title
            r"        {\sffamily\fontsize{18}{19}\selectfont\bfseries\color{blueprintblue}\@title}%" + "\n"  # 18pt, bold, blue, sans-serif title
            r"        \vspace{4pt}%" + "\n"  # 4pt vertical space after title
            r"    \end{center}%" + "\n"
            r"}" + "\n"
            r"\makeatother" + "\n"  # Restore @ character behavior
            "\n"
            # Section formatting
            r"\titleformat{\section}" + "\n"  # Section heading format
            r"    {\sffamily\fontsize{14}{15}\selectfont\bfseries\color{blueprintblue}}" + "\n"  # 14pt, bold, blue, sans-serif
            r"    {\thesection}{1em}{}" + "\n"  # Section number with 1em space
            r"\titlespacing*{\section}{0pt}{8pt}{4pt}" + "\n"  # Spacing: left, before, after
            "\n"
            # Subsection formatting
            r"\titleformat{\subsection}" + "\n"  # Subsection heading format
            r"    {\sffamily\fontsize{12}{13}\selectfont\bfseries\color{blueprintblue}}" + "\n"  # 12pt, bold, blue, sans-serif
            r"    {\thesubsection}{1em}{}" + "\n"  # Subsection number with 1em space
            r"\titlespacing*{\subsection}{0pt}{8pt}{4pt}" + "\n"  # Spacing: left, before, after
            "\n"
            # Subsubsection formatting
            r"\titleformat{\subsubsection}" + "\n"  # Subsubsection heading format
            r"    {\sffamily\fontsize{12}{13}\selectfont\bfseries\color{blueprintblue}}" + "\n"  # 12pt, bold, blue, sans-serif
            r"    {\thesubsubsection}{1em}{}" + "\n"  # Subsubsection number with 1em space
            r"\titlespacing*{\subsubsection}{0pt}{4pt}{0pt}" + "\n"  # Spacing: left, before, after
            "\n"
            # Paragraph formatting
            r"\parindent 0in" + "\n"  # No paragraph indentation
            # Begin document
            r"\begin{document}" + "\n"
            rf"\title{{{self.title}}}" + "\n"  # Set document title
            r"\date{}" + "\n"  # No date displayed
            r"\maketitle" + "\n"  # Generate the title
        )

        latex = preamble + self.content + r"\end{document}"
        if language != "en":
            # Translate content to the specified language
            from blueprints.utils.language.translate import LatexTranslator  # noqa: PLC0415

            latex = LatexTranslator(original_text=latex, destination_language=language).text

        # If path is provided, save to file and return None
        if path is not None:
            # Convert Path to str if needed
            file_path = str(path) if isinstance(path, Path) else path
            Path(file_path).write_text(latex, encoding="utf-8")
            return None

        # Return LaTeX string
        return latex

    def to_word(self, path: str | Path | BytesIO | None = None, language: str = "en") -> bytes | None:  # pragma: no cover
        """Convert the LaTeX report to a Word document.

        This method uses the ReportToWordConverter to convert the LaTeX content
        of the report into a Word document format. The output can be saved to a file,
        written to a BytesIO object, or returned as bytes.

        Parameters
        ----------
        path : str | Path | BytesIO | None, optional
            The destination for the Word document:
            - str or Path: File path where the document will be saved, for example 'report.docx'. Remember to use .docx extension.
            - BytesIO: Buffer to write the document to (in-memory)
                ```python
                from io import BytesIO

                buffer = BytesIO()
                report.to_word(buffer)
                docx_bytes = buffer.getvalue()
                ```
            - None: Return the document as bytes (default)
        language : str, optional
            Language code for localization, full list on https://docs.cloud.google.com/translate/docs/languages
            Warning: only English is officially supported in Blueprints (default is "en" for English).

        Returns
        -------
        bytes | None
            If path is None, returns the Word document as bytes.
            If path is provided (str, Path, or BytesIO), returns None.

        Examples
        --------
        Save to a file path:

        >>> report = Report(title="My Report")
        >>> report.add_heading("Introduction")
        >>> report.add_paragraph("Some text")
        >>> report.to_word("report.docx")  # Save to file

        Save to a pathlib.Path:

        >>> from pathlib import Path
        >>> report.to_word(Path("report.docx"))

        Write to a BytesIO object for in-memory processing:

        >>> from io import BytesIO
        >>> buffer = BytesIO()
        >>> report.to_word(buffer)
        >>> docx_bytes = buffer.getvalue()

        Get bytes directly (useful for streaming, email attachments, etc.):

        >>> docx_bytes = report.to_word()
        >>> # Can now send as email attachment or stream over HTTP
        """
        from blueprints.utils._report_to_word import (  # noqa: PLC0415
            _ReportToWordConverter,
        )  # imported here as core does not have word module installed by default

        latex_content = self.to_latex(language=language)
        converter = _ReportToWordConverter(latex_content)
        if converter.document:
            if path is None:
                # Return bytes directly
                buffer = BytesIO()
                converter.document.save(buffer)
                buffer.seek(0)
                return buffer.getvalue()
            # Save to file path or BytesIO object
            # Convert Path to str for compatibility with python-docx
            if isinstance(path, Path):
                converter.document.save(str(path))
            else:
                converter.document.save(path)
            return None
        return None

    def to_pdf(self, path: str | Path | None = None, language: str = "en", cleanup: bool = True) -> bytes | None:  # noqa: C901
        """Generate a PDF document by compiling LaTeX with pdflatex.

        This method generates LaTeX content using to_latex(), compiles it with pdflatex,
        and returns or saves the resulting PDF. Requires pdflatex to be installed and
        available in the system PATH. Can be downloaded from a LaTeX distribution such as TeX Live or MiKTeX.

        Parameters
        ----------
        path : str | Path | None, optional
            The destination for the PDF document:
            - str or Path: File path where the .pdf file will be saved
            - None: Return the PDF as bytes (default)
        language : str, optional
            Language code for localization, full list on https://docs.cloud.google.com/translate/docs/languages
            Warning: only English is officially supported in Blueprints (default is "en" for English).
        cleanup : bool, optional
            Whether to remove temporary LaTeX files after compilation. Default is True.

        Returns
        -------
        bytes | None
            If path is None, returns the PDF document as bytes.
            If path is provided (str or Path), returns None after saving to file.

        Raises
        ------
        RuntimeError
            If pdflatex is not found or compilation fails.

        Examples
        --------
        Get PDF as bytes:

        >>> report = Report(title="My Report")
        >>> report.add_heading("Introduction")
        >>> report.add_paragraph("Some text")
        >>> pdf_bytes = report.to_pdf()

        Save directly to a file:

        >>> report.to_pdf("report.pdf")

        Save using pathlib.Path:

        >>> from pathlib import Path
        >>> report.to_pdf(Path("report.pdf"))

        Keep temporary LaTeX files for debugging:

        >>> report.to_pdf("report.pdf", cleanup=False)
        """
        # Check if pdflatex is available
        try:
            subprocess.run(
                ["pdflatex", "--version"],
                capture_output=True,
                check=True,
                timeout=10,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            raise RuntimeError(
                "pdflatex is not installed or not found in PATH. Please install a LaTeX distribution (e.g., MiKTeX, TeX Live) that includes pdflatex."
                " Go to https://miktex.org/download or https://www.tug.org/texlive/ for more information."
            ) from e

        # Generate LaTeX content
        latex_content = self.to_latex(language=language)
        assert latex_content is not None  # to_latex returns str when path is None

        # Create temporary directory for compilation
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            tex_file = tmpdir_path / "report.tex"
            pdf_file = tmpdir_path / "report.pdf"

            # Write LaTeX content to temporary file
            tex_file.write_text(latex_content, encoding="utf-8")

            # Run pdflatex twice for proper references and table of contents
            for _ in range(2):
                result = subprocess.run(
                    ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", str(tex_file)],
                    check=False,
                    cwd=tmpdir,
                    capture_output=True,
                    text=True,
                    timeout=60,
                )

                if result.returncode != 0:
                    # Extract error information from log
                    error_msg = "pdflatex compilation failed.\n"
                    if result.stdout:  # pragma: no cover
                        # Find the first error in the output
                        lines = result.stdout.split("\n")
                        for i, line in enumerate(lines):
                            if line.startswith("!"):
                                error_msg += "\n".join(lines[i : i + 5])
                                break
                    raise RuntimeError(error_msg)

            # Check if PDF was created
            if not pdf_file.exists():
                raise RuntimeError("PDF file was not created by pdflatex.")  # pragma: no cover

            # Read the PDF content
            pdf_content = pdf_file.read_bytes()

            # If path is provided, save to file
            if path is not None:
                output_path = Path(path) if isinstance(path, str) else path
                output_path.write_bytes(pdf_content)

                # Optionally copy auxiliary files for debugging
                if not cleanup:  # pragma: no cover
                    aux_files = [".aux", ".log", ".out"]
                    base_name = output_path.stem
                    output_dir = output_path.parent
                    for ext in aux_files:
                        aux_file = tmpdir_path / f"report{ext}"
                        if aux_file.exists():
                            (output_dir / f"{base_name}{ext}").write_bytes(aux_file.read_bytes())

                return None

            # Return PDF as bytes
            return pdf_content

"""Report builder for LaTeX documents.

Developer notes: The features in this class are designed to create LaTeX reports that can be compiled with pdflatex.
The LaTeX styling is made to match with the Word document report styling as closely as possible. Changes here
should ideally be reflected in the Word document converter in report_to_word_document.py.

"""

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Literal, Self

from blueprints.codes.formula import Formula


@dataclass
class LatexReport:
    r"""LaTeX report builder for creating structured documents with standardized formatting.

    Check our docs for examples of usage.

    Parameters
    ----------
    title : str, optional
        The title of the report.

    Examples
    --------
    >>> report = LatexReport(title="Sample Report")
    >>> report.add_section("Introduction")
    >>> report.add_subsection("Background")
    >>> report.add_subsubsection("Details")
    >>> report.add_text("This is normal text.")
    >>> report.add_text("This is bold text with newline after.", bold=True).add_newline()
    >>> report.add_text("This is italic text with 4 newlines after.", italic=True).add_newline(n=4)
    >>> report.add_text("This is bold and italic text.", bold=True, italic=True)
    >>> report.add_newline()
    >>> report.add_equation("E=mc^2", tag="3.14")
    >>> report.add_text("Before inline equation:", italic=True).add_equation(r"\frac{a}{b}", inline=True).add_text(
    ...     " and after inline equation.", bold=True
    ... ).add_newline()
    >>> report.add_equation(r"e^{i \pi} + 1 = 0", inline=True).add_text("inline can be at start of text.").add_newline()
    >>> report.add_text("Or at the end of text", bold=True).add_equation(r"\int_a^b f(x) dx", inline=True).add_newline(n=2)
    >>> report.add_text("Equations can also be $a^2 + b^2 = c^2$ inline in the add text method.").add_newline()
    >>> report.add_table(
    ...     headers=["Parameter", "Value", "Unit"], rows=[[r"\text{Length}", "10", r"\text{m}"], [r"\text{Density}", "500", r"\text{kg/$m^3$}"]]
    ... )
    >>> report.add_figure(r"tomato.png", width=0.2)  # needs the tomato.png file in working directory
    >>> report.add_enumerate(["First item", "Second item"])
    >>> report.add_itemize(["Bullet one", "Bullet two"])
    >>> latex_document = report.to_document()
    >>> print(latex_document)  # prints the complete LaTeX document string, which can be compiled with pdflatex in for example Overleaf.
    """

    title: str | None = None
    content: str = field(default="", init=False)

    def add_text(self, text: str, bold: bool = False, italic: bool = False) -> Self:
        r"""Add text with optional bold and italic formatting.

        Parameters
        ----------
        text : str
            The text content to display.
        bold : bool, optional
            Whether to format the text in bold.
        italic : bool, optional
            Whether to format the text in italics.

        Returns
        -------
        LatexReport
            Returns self for method chaining.

        Examples
        --------
        >>> report = LatexReport()
        >>> report.add_text("This is regular text")
        >>> report.add_text("This is bold text", bold=True)
        >>> report.add_text("This is bold and italic", bold=True, italic=True)
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
            The LaTeX equation.
        tag : str or None, optional
            Tag to label the equation (e.g., "6.83", "EN 1992-1-1:2004 6.6n", etc.).
        inline : bool, optional
            Whether to add the equation inline (meaning within text) or as a separate equation block. Default is False.

        Returns
        -------
        LatexReport
            Returns self for method chaining.

        Examples
        --------
        When creating a report, you can add equations in different ways:
        >>> report = LatexReport()
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
        LatexReport
            Returns self for method chaining.

        Examples
        --------
        >>> from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import formula_6_5
        >>> formula = formula_6_5.Form6Dot5UnityCheckTensileStrength(n_ed=150000, n_t_rd=200000)
        >>> report = LatexReport()
        >>> report.add_formula(formula, options="short")  # Minimal representation
        >>> print(report)
        # report can be converted to formatted LaTeX document with report.to_document()
        >>> print(report.to_document())
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

    def add_section(self, title: str) -> Self:
        """Add a report section.

        For more info on sections, see: https://www.overleaf.com/learn/latex/Sections_and_chapters
        Blueprints uses Section > Subsection > Subsubsection > content (from add_text etc.) hierarchy.

        Parameters
        ----------
        title : str
            The section title.

        Returns
        -------
        LatexReport
            Returns self for method chaining.

        Examples
        --------
        >>> report = LatexReport()
        >>> report.add_section("This is a section")
        """
        self.content += rf"\section{{{title}}}"

        # Add a newline for visual separation
        self.content += "\n"

        return self

    def add_subsection(self, title: str) -> Self:
        """Add a subsection.

        For more info on subsections, see: https://www.overleaf.com/learn/latex/Sections_and_chapters
        Blueprints uses Section > Subsection > Subsubsection > content (from add_text etc.) hierarchy.

        Parameters
        ----------
        title : str
            The subsection title.

        Returns
        -------
        LatexReport
            Returns self for method chaining.

        Examples
        --------
        >>> report = LatexReport()
        >>> report.add_subsection("This is a subsection")
        """
        self.content += rf"\subsection{{{title}}}"

        # Add a newline for visual separation
        self.content += "\n"

        return self

    def add_subsubsection(self, title: str) -> Self:
        """Add a subsubsection.

        For more info on subsubsections, see: https://www.overleaf.com/learn/latex/Sections_and_chapters
        Blueprints uses Section > Subsection > Subsubsection > content (from add_text etc.) hierarchy.

        Parameters
        ----------
        title : str
            The subsubsection title.

        Returns
        -------
        LatexReport
            Returns self for method chaining.

        Examples
        --------
        >>> report = LatexReport()
        >>> report.add_subsubsection("This is a subsubsection")
        """
        self.content += rf"\subsubsection{{{title}}}"

        # Add a newline for visual separation
        self.content += "\n"

        return self

    def add_table(
        self,
        headers: list[str],
        rows: list[list[str]],
        position: str = "h",
        centering: bool = True,
    ) -> Self:
        r"""Add a table using LaTeX table environment.

        For more info on tables, see: https://www.overleaf.com/learn/latex/Tables

        Parameters
        ----------
        headers : list[str]
            List of column headers.
        rows : list[list[str]]
            List of rows, where each row is a list of cell values.
        position : str, optional
            LaTeX positioning parameter (e.g., 'h', 't', 'b'). Default is 'h'.

            h: Will place the table here approximately.
            t: Position the table at the top of the page.
            b: Position the table at the bottom of the page.
            p: Put the table in a special page, for tables only.
            !: Override internal LaTeX parameters.
            H: Place the table at this precise location, pretty much like h!.
        centering : bool, optional
            If True, centers the table. Default is True.

        Returns
        -------
        LatexReport
            Returns self for method chaining.

        Examples
        --------
        >>> report = LatexReport()
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
            rf"\begin{{table}}[{position}] {centering_cmd}"
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
        position: str = "h",
        caption: str | None = None,
    ) -> Self:
        r"""Add a figure with an image.

        For more info on figures, see: https://www.overleaf.com/learn/latex/Inserting_Images

        Parameters
        ----------
        image_path : str
            Path to the image file.
        width : float, optional
            Width specification for the image as ratio of the text width. Default is 0.9.
        position : str, optional
            LaTeX positioning parameter (e.g., 'h', 't', 'b'). Default is 'h'.

            h: Will place the figure here approximately.
            t: Position the figure at the top of the page.
            b: Position the figure at the bottom of the page.
            p: Put the figure in a special page, for floats only.
            !: Override internal LaTeX parameters.
            H: Place the figure at this precise location, pretty much like h!.
        caption : str, optional
            Caption text for the figure. Will be displayed below the image. Default is None.

        Returns
        -------
        LatexReport
            Returns self for method chaining.

        Examples
        --------
        >>> report = LatexReport()
        >>> report.add_figure("path_to_image")
        >>> report.add_figure("path_to_image", width=0.5)
        >>> report.add_figure("plot.png", caption="Results of the analysis")
        """
        # Build the figure environment
        figure_parts = [rf"\begin{{figure}}[{position}] \centering ", rf"\includegraphics[width={width}\textwidth]{{{image_path}}} "]

        # Add optional caption
        if caption:
            figure_parts.append(rf"\caption{{{caption}}} ")

        figure_parts.append(r"\end{figure}")

        figure = "".join(figure_parts)
        self.content += figure

        # Add a newline for visual separation
        self.content += "\n"

        return self

    def add_itemize(self, items: Sequence[Any]) -> Self:
        """Add a bulleted list using LaTeX itemize environment.

        For more info on itemize, see: https://www.overleaf.com/learn/latex/Lists#The_itemize_environment_for_bulleted_(unordered)_lists

        Parameters
        ----------
        items : Sequence[Any]
            List of items to display as bullets. Can include nested lists for sub-items.

        Returns
        -------
        LatexReport
            Returns self for method chaining.

        Examples
        --------
        >>> report = LatexReport()
        >>> report.add_itemize(["Bullet 1", "Bullet 2", "Bullet 3"])
        >>> report.add_itemize(["One", ["A", "B", "C"], "Two", ["A", ["I", "II", "III"]]])

        """

        def _build_itemize(item_list: list, depth: int = 0) -> str:
            """Recursively build itemize environment for nested lists."""
            result = r"\begin{itemize} "
            for item in item_list:
                if isinstance(item, list):
                    result += _build_itemize(item, depth + 1)
                else:
                    result += rf"\item {item} "
            result += r"\end{itemize} "
            return result

        self.content += _build_itemize(list(items))

        # Add a newline for visual separation
        self.content += "\n"

        return self

    def add_enumerate(self, items: Sequence[Any]) -> Self:
        """Add a numbered list using LaTeX enumerate environment.

        For more info on enumerate, see: https://www.overleaf.com/learn/latex/Lists#The_enumerate_environment_for_numbered_(ordered)_lists

        Parameters
        ----------
        items : Sequence[Any]
            List of items to display as numbered entries. Can include nested lists for sub-items.

        Returns
        -------
        LatexReport
            Returns self for method chaining.

        Examples
        --------
        >>> report = LatexReport()
        >>> report.add_enumerate(["Number 1", "Number 2", "Number 3"])
        >>> report.add_enumerate(["One", ["A", "B", "C"], "Two", ["A", ["I", "II", "III"]]])
        """

        def _build_enumerate(item_list: list, depth: int = 0) -> str:
            """Recursively build enumerate environment for nested lists."""
            result = r"\begin{enumerate} "
            for item in item_list:
                if isinstance(item, list):
                    result += _build_enumerate(item, depth + 1)
                else:
                    result += rf"\item {item} "
            result += r"\end{enumerate} "
            return result

        self.content += _build_enumerate(list(items))

        # Add a newline for visual separation
        self.content += "\n"

        return self

    def add_newline(self, n: int = 1) -> Self:
        """Add a newline command.

        For more info on newlines, see: https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes#Basic_formatting:_abstract,_paragraphs_and_newlines

        Parameters
        ----------
        n : int, optional
            Number of newlines to add. Default is 1.

        Returns
        -------
        LatexReport
            Returns self for method chaining.

        Examples
        --------
        >>> report = LatexReport()
        >>> report.add_newline()
        """
        self.content += r"\newline" * n

        # Add a newline for visual separation
        self.content += "\n"

        return self

    def __repr__(self) -> str:
        """Return a concise representation showing report structure and content summary."""
        sections = self.content.count(r"\section{")
        subsections = self.content.count(r"\subsection{")
        equations = self.content.count(r"\begin{equation}")
        tables = self.content.count(r"\begin{table}")
        figures = self.content.count(r"\begin{figure}")
        lists = self.content.count(r"\begin{itemize}") + self.content.count(r"\begin{enumerate}")

        title_str = f'title="{self.title}"' if self.title else "title=None"
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
            f"LaTeX Report: {self.title or '(untitled)'}",
            "=" * 60,
            f"Sections:      {sections}",
            f"Subsections:   {subsections}",
            f"Equations:     {equations}",
            f"Tables:        {tables}",
            f"Figures:       {figures}",
            f"Lists:         {lists}",
            f"Content size:  {len(self.content)} characters",
            "=" * 60,
            "Use .to_document() to generate the full LaTeX document.",
            "=" * 60,
        ]

        return "\n".join(lines)

    def to_document(self, language: str = "en") -> str:
        """Generate a complete LaTeX document with proper preamble and structure.

        You could compile the output with pdflatex in for example Overleaf.

        Parameters
        ----------
        language : str, optional
            Language code for localization, full list on https://docs.cloud.google.com/translate/docs/languages
            Warning: only English is officially supported in Blueprints (default is "en" for English).

        Returns
        -------
        str
            Complete LaTeX document string including preamble, begin/end document,
            and all content, ready for copy-pasting into a .tex file for example.

        Examples
        --------
        >>> report = LatexReport(title="My Report")
        >>> report.add_section("Introduction")
        >>> report.add_text("Some text")
        >>> latex_doc = report.to_document()
        """
        # Use provided title or fall back to instance title
        doc_title = self.title or ""

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
            rf"\title{{{doc_title}}}" + "\n"  # Set document title
            r"\date{}" + "\n"  # No date displayed
            r"\maketitle" + "\n"  # Generate the title
        )

        latex = preamble + self.content + r"\end{document}"
        if language != "en":
            # Translate content to the specified language
            from blueprints.utils.language.translate import LatexTranslator  # noqa: PLC0415

            latex = str(LatexTranslator(original_text=latex, destination_language=language))

        # Combine preamble, content, and closing
        return latex

    def to_word(self, path: str, language: str = "en") -> None:  # pragma: no cover
        """Convert the LaTeX report to a Word document.

        This method uses the ReportToWordConverter to convert the LaTeX content
        of the report into a Word document format, saved at the specified path.

        Parameters
        ----------
        path : str
            The file path where the Word document will be saved.
        language : str, optional
            Language code for localization, full list on https://docs.cloud.google.com/translate/docs/languages
            Warning: only English is officially supported in Blueprints (default is "en" for English).

        Examples
        --------
        >>> report = LatexReport(title="My Report")
        >>> report.add_section("Introduction")
        >>> report.add_text("Some text")
        >>> report.to_word("report.docx")  # Save the Word document
        """
        from blueprints.utils.report_to_word import (  # noqa: PLC0415
            ReportToWordConverter,
        )  # imported here as core does not have word module installed by default

        latex_content = self.to_document(language=language)
        converter = ReportToWordConverter(latex_content)
        if converter.document:
            converter.document.save(path)

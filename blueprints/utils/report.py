"""Report builder for LaTeX documents."""

from dataclasses import dataclass, field
from typing import Literal, Self

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
    >>> report.add_text("Before an inline equation:", italic=True).add_equation(r"\frac{a}{b}", inline=True).add_text(
    ...     " and after the inline equation.", bold=True
    ... ).add_newline()
    >>> report.add_equation(r"e^{i \pi} + 1 = 0", inline=True).add_text("inline can be at start of text.", bold=True, italic=True).add_newline()
    >>> report.add_text("or at the end of text", bold=True).add_equation(r"\int_a^b f(x) dx", inline=True).add_newline(n=2)
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
            self.content += rf"\text{{{text}}}"

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
            self.content += r"\text{" + rf"${equation}$" + f"{f' ({tag})' if tag else ''}" + r"}"
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

        Parameters
        ----------
        image_path : str
            Path to the image file.
        width : float, optional
            Width specification for the image as ratio of the text width. Default is 0.9.
        position : str, optional
            LaTeX positioning parameter. Default is 'h'.

            =========  ==================================================================================
            Parameter  Description
            =========  ==================================================================================
            h          Place the float here, approximately at the same point it occurs in the source text
            t          Position at the top of the page
            b          Position at the bottom of the page
            p          Put on a special page for floats only
            =========  ==================================================================================

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

    def add_itemize(self, items: list[str]) -> Self:
        """Add a bulleted list using LaTeX itemize environment.

        For more info on itemize, see: https://www.overleaf.com/learn/latex/Lists#The_itemize_environment_for_bulleted_(unordered)_lists

        Parameters
        ----------
        items : list[str]
            List of items to display as bullets.

        Returns
        -------
        LatexReport
            Returns self for method chaining.

        Examples
        --------
        >>> report = LatexReport()
        >>> report.add_itemize(["Bullet 1", "Bullet 2", "Bullet 3"])
        """
        itemize = r"\begin{itemize} "
        for item in items:
            itemize += rf"\item {item} "
        itemize += r"\end{itemize}"
        self.content += itemize

        # Add a newline for visual separation
        self.content += "\n"

        return self

    def add_enumerate(self, items: list[str]) -> Self:
        """Add a numbered list using LaTeX enumerate environment.

        For more info on enumerate, see: https://www.overleaf.com/learn/latex/Lists#The_enumerate_environment_for_numbered_(ordered)_lists

        Parameters
        ----------
        items : list[str]
            List of items to display as numbered entries.

        Returns
        -------
        LatexReport
            Returns self for method chaining.

        Examples
        --------
        >>> report = LatexReport()
        >>> report.add_enumerate(["Number 1", "Number 2", "Number 3"])
        """
        enumerate_content = r"\begin{enumerate} "
        for item in items:
            enumerate_content += rf"\item {item} "
        enumerate_content += r"\end{enumerate}"
        self.content += enumerate_content

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

    def to_document(self) -> str:
        """Generate a complete LaTeX document with proper preamble and structure.

        You could compile the output with pdflatex in for example Overleaf.

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
            r"\usepackage{amsmath}" + "\n"
            r"\usepackage{booktabs}" + "\n"
            r"\usepackage{geometry}" + "\n"
            r"\usepackage{graphicx}" + "\n"
            r"\usepackage{setspace}" + "\n"
            r"\usepackage{xcolor}" + "\n"
            r"\usepackage{titlesec}" + "\n"
            r"\usepackage{helvet}" + "\n"
            r"\usepackage[T1]{fontenc}" + "\n"
            r"\usepackage{enumitem}" + "\n"
            r"\geometry{a4paper, margin=1in}" + "\n"
            r"\setstretch{1.3}" + "\n"
            r"\setlength{\parskip}{0pt}" + "\n"
            r"\setlength{\abovedisplayskip}{12pt}" + "\n"
            r"\setlength{\belowdisplayskip}{12pt}" + "\n"
            r"\setlist{nosep}" + "\n"
            "\n"
            r"% Define the dark blue color" + "\n"
            r"\definecolor{blueprintblue}{RGB}{0,40,85}" + "\n"
            "\n"
            r"% Configure title style (18pt, sans-serif, bold, blue)" + "\n"
            r"\makeatletter" + "\n"
            r"\renewcommand{\maketitle}{%" + "\n"
            r"    \begin{center}%" + "\n"
            r"        {\sffamily\fontsize{18}{19}\selectfont\bfseries\color{blueprintblue}\@title}%" + "\n"
            r"        \vspace{4pt}%" + "\n"
            r"    \end{center}%" + "\n"
            r"}" + "\n"
            r"\makeatother" + "\n"
            "\n"
            r"% Configure section styles" + "\n"
            r"\titleformat{\section}" + "\n"
            r"    {\sffamily\fontsize{14}{15}\selectfont\bfseries\color{blueprintblue}}" + "\n"
            r"    {\thesection}{1em}{}" + "\n"
            r"\titlespacing*{\section}{0pt}{8pt}{4pt}" + "\n"
            "\n"
            r"\titleformat{\subsection}" + "\n"
            r"    {\sffamily\fontsize{12}{13}\selectfont\bfseries\color{blueprintblue}}" + "\n"
            r"    {\thesubsection}{1em}{}" + "\n"
            r"\titlespacing*{\subsection}{0pt}{8pt}{4pt}" + "\n"
            "\n"
            r"\titleformat{\subsubsection}" + "\n"
            r"    {\sffamily\fontsize{12}{13}\selectfont\bfseries\color{blueprintblue}}" + "\n"
            r"    {\thesubsubsection}{1em}{}" + "\n"
            r"\titlespacing*{\subsubsection}{0pt}{4pt}{0pt}" + "\n"
            "\n"
            r"\begin{document}" + "\n"
            rf"\title{{{doc_title}}}" + "\n"
            r"\date{}" + "\n"
            r"\maketitle" + "\n"
        )

        # Combine preamble, content, and closing
        return preamble + self.content + r"\end{document}"

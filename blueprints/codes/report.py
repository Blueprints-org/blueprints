"""Report formula representation."""

from dataclasses import dataclass, field
from typing import Literal, Self

from blueprints.codes.formula import Formula


@dataclass
class LatexReport:
    r"""Report check representation.

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
    >>> report.add_equation(r"e^{i \pi} + 1 = 0", inline=True).add_text("inline can be at start at of text.", bold=True, italic=True).add_newline()
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

    Parameters
    ----------
    title : str, optional
        The title of the report. If provided, will be prepended to content.
    content : str
        The content of the report.
    """

    title: str | None = None
    content: str = field(default="", init=False)

    def __post_init__(self) -> None:
        """Initialize content to an empty string."""
        self.content = ""

    def add_text(self, text: str, bold: bool = False, italic: bool = False) -> Self:
        r"""Add descriptive text using LaTeX text commands.

        Parameters
        ----------
        text : str
            The text content to display.
        bold : bool, optional
            If True, wraps text in \\textbf{...}. Default is False.
        italic : bool, optional
            If True, wraps text in \\textit{...}. Default is False.

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

    def add_equation(self, equation: str, tag: str | None = None, inline: bool = False) -> Self:
        r"""Add an equation in a LaTeX equation environment or inline.

        Parameters
        ----------
        equation : str
            The LaTeX equation content.
        tag : str or None, optional
            Optional tag to label the equation (e.g., "6.83"). Only used when inline=False. Default is None.
        inline : bool, optional
            If True, wraps equation in $...$. If False, uses equation environment. Default is False.

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
            self.content += r"\text{" + rf"${equation}$" + r"}"
        elif tag:
            self.content += rf"\begin{{equation}} {equation} \tag{{{tag}}} \end{{equation}}"
        else:
            self.content += rf"\begin{{equation}} {equation} \end{{equation}}"

        # Add a newline for visual separation
        self.content += "\n"

        return self

    def add_formula(self, formula: Formula, options: Literal["short", "complete", "complete_with_units"], inline: bool = False) -> Self:
        r"""Add a Blueprints formula to the report, for generic equations, use add_equation.

        Parameters
        ----------
        formula : Formula
            The Blueprints formula object to add.
        options : Literal["short", "complete", "complete_with_units"]
            The representation of the formula to add.
            short - Minimal representation (symbol = result [unit])
            complete - Complete representation (symbol = equation = numeric_equation = result [unit])
            complete_with_units - Complete representation with units (symbol = equation = numeric_equation_with_units [unit] = result [unit])
        inline : bool, optional
            If True, adds the formula inline. Default is False.

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
        if options == "short":
            equation_str = formula.latex().short
        elif options == "complete":
            equation_str = formula.latex().complete
        else:  # complete_with_units
            equation_str = formula.latex().complete_with_units

        self.add_equation(equation=equation_str, inline=inline)

        # New line for visual separation already added in add_equation
        return self

    def add_section(self, title: str) -> Self:
        """Add a section.

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

        Parameters
        ----------
        headers : list[str]
            List of column headers.
        rows : list[list[str]]
            List of rows, where each row is a list of cell values.
        position : str, optional
            LaTeX positioning parameter (e.g., 'h', 't', 'b'). Default is 'h'.
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
        num_cols = len(headers)
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
    ) -> Self:
        """Add a figure with an image.

        Parameters
        ----------
        image_path : str
            Path to the image file.
        width : float, optional
            Width specification for the image as ratio of the text width. Default is 0.9.
        position : str, optional
            LaTeX positioning parameter (e.g., 'h', 't', 'b'). Default is 'h'.


        Returns
        -------
        LatexReport
            Returns self for method chaining.

        Examples
        --------
        >>> report = LatexReport()
        >>> report.add_figure("path_to_image")
        >>> report.add_figure("path_to_image", width=0.5)
        """
        figure = (
            rf"\begin{{figure}}[{position}] \centering "
            rf"\includegraphics[width={width}\textwidth]{{{image_path}}} "
            rf"\end{{figure}}"
        )
        self.content += figure

        # Add a newline for visual separation
        self.content += "\n"

        return self

    def add_itemize(self, items: list[str]) -> Self:
        """Add a bulleted list using LaTeX itemize environment.

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

    def to_document(self, title: str | None = None) -> str:
        """Generate a complete LaTeX document with proper preamble and structure.

        Parameters
        ----------
        title : str, optional
            The document title. If not provided, uses the instance title.

        Returns
        -------
        str
            Complete LaTeX document string including preamble, begin/end document,
            and all content.

        Examples
        --------
        >>> report = LatexReport(title="My Report")
        >>> report.add_section("Introduction")
        >>> report.add_text("Some text")
        >>> latex_doc = report.to_document()
        """
        # Use provided title or fall back to instance title
        doc_title = title if title is not None else self.title if self.title is not None else ""

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
            r"% Configure title style (36pt, sans-serif, bold, blue)" + "\n"
            r"\makeatletter" + "\n"
            r"\renewcommand{\maketitle}{%" + "\n"
            r"    \begin{center}%" + "\n"
            r"        {\sffamily\fontsize{36}{43}\selectfont\bfseries\color{blueprintblue}\@title}%" + "\n"
            r"        \vspace{4pt}%" + "\n"
            r"    \end{center}%" + "\n"
            r"}" + "\n"
            r"\makeatother" + "\n"
            "\n"
            r"% Configure section styles" + "\n"
            r"\titleformat{\section}" + "\n"
            r"    {\sffamily\fontsize{24}{29}\selectfont\bfseries\color{blueprintblue}}" + "\n"
            r"    {\thesection}{1em}{}" + "\n"
            r"\titlespacing*{\section}{0pt}{8pt}{4pt}" + "\n"
            "\n"
            r"\titleformat{\subsection}" + "\n"
            r"    {\sffamily\fontsize{18}{22}\selectfont\bfseries\color{blueprintblue}}" + "\n"
            r"    {\thesubsection}{1em}{}" + "\n"
            r"\titlespacing*{\subsection}{0pt}{8pt}{4pt}" + "\n"
            "\n"
            r"\titleformat{\subsubsection}" + "\n"
            r"    {\sffamily\fontsize{14}{17}\selectfont\bfseries\color{blueprintblue}}" + "\n"
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

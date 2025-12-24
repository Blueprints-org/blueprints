"""Tests for the ReportToWordConverter class."""

from blueprints.report_to_word_document import ReportToWordConverter


class TestReportToWordConverter:
    """Tests for the ReportToWordConverter class."""

    def test_empty_input_returns_empty_document(self) -> None:
        """Test that an empty LaTeX string returns an empty Document."""
        assert ReportToWordConverter().convert_to_word("")

    def test_complex_document_conversion(self) -> None:
        """Test conversion of a complex LaTeX document."""
        complex_latex = r"""
            \documentclass{article}
            \usepackage{amsmath}
            \usepackage{booktabs}
            \usepackage{geometry}
            \geometry{a4paper, margin=1in}

            % Increase spacing throughout document
            \usepackage{setspace}
            \setstretch{1.3}  % Increase line spacing by 30%

            % Add space between paragraphs
            \setlength{\parskip}{0.5em}

            % Add space around equations
            \setlength{\abovedisplayskip}{12pt}
            \setlength{\belowdisplayskip}{12pt}

            \begin{document}

            \title{Torsion Check Results}
            \date{}
            \maketitle

            \section{Utilization Summary}

            \begin{table}[h]
            \centering
            \begin{tabular}{lcc}
            \toprule
            Check & Utilization & Status \\
            \midrule
            \text{Concrete strut capacity} & 0.588 & \text{PASS} \\
            \text{Torsion moment capacity} & 4.825 & \text{FAIL} \\
            \text{Max longitudinal reinforcement} & 0.107 & \text{PASS} \\
            \text{Also $\frac{a}{b}$ inline equations in tables} & 0.250 & \text{PASS} \\
            \bottomrule
            \end{tabular}
            \end{table}

            \textbf{Overall Result: FAIL}
            \section{Individual Checks}
            \subsection{Concrete Strut Capacity}
            \text{Concrete strut capacity check EN 1992-1-1:2004 art. 6.3.2(4)} \newline \newline
            \textbf{Maximum shear resistance}
            \begin{equation} V_{Rd,max} = \alpha_{cw} \cdot b_{w} \cdot z \cdot \nu_{1} \cdot \frac{f_{cd}}{\cot(\theta) + \tan(\theta)} =
            1.00 \cdot 400.00 \cdot 486.00 \cdot 0.52 \cdot \frac{23.33}{\cot(45.00) + \tan(45.00)} = 1170288.00 \ \text{N} \tag{6.9} \end{equation}
            \textbf{Design torsional resistance moment}
            \begin{equation} T_{Rd,max} = 2 \cdot \nu \cdot \alpha_{cw} \cdot f_{cd} \cdot A_{k} \cdot t_{ef,i} \cdot \sin(\theta) \cdot \cos(\theta)=
            2 \cdot 0.52 \cdot 1.00 \cdot 23.33 \cdot 134400.00 \cdot 120.00 \cdot \sin(45.00) \cdot \cos(45.00) =
            194181120.00 \ \text{Nmm} \tag{6.30} \end{equation}
            \textbf{Combined interaction check}
            \begin{equation} \frac{T_{Ed}}{T_{Rd,max}} + \frac{V_{Ed}}{V_{Rd,max}} = 0.309 + 0.279 = 0.588 \leq 1.0 \tag{6.29} \end{equation}
            \textbf{Result: PASS (Utilization: 58.8\%)}

            \section{Conclusions}

            \textbf{Warning:} One or more checks have failed.

            \textbf{Note:} Torsion moment capacity is insufficient with minimum reinforcement.
            Additional torsion-specific reinforcement is required as specified above.

            \textit{This is text in italics which $a = b ^ c$ can also feature inline equation} \newline

            \end{document}
        """

        assert ReportToWordConverter().convert_to_word(complex_latex)

# Reports: Design and Architecture

## LaTeX vs Report Generation

The Formula object provides two distinct methods for generating documentation output, each serving different purposes:

### `.latex()` Method: Math Mode Output

The `.latex()` method returns a `LatexFormula` object containing mathematical expressions in LaTeX math mode. This is designed for inline equations or equation environments:

- Returns symbolic and numeric equations without text formatting
- Output is pure mathematical notation (e.g., `c_{nom} = c_{min} + \Delta c_{dev}`)
- Intended for use within `\begin{equation}...\end{equation}` or `$...$` blocks
- Provides granular access to equation components (return_symbol, equation, numeric_equation, result)

### `.report()` Method: Text Mode Output

The `.report()` method returns a complete LaTeX document fragment in text mode. It can include the following, with literal LaTeX text-mode examples which can be included into a LaTeX-handler, e.g. Overleaf:

1. Descriptive text using `\text{...}` commands, also handles `\textbf{...}` and `\textit{...}`
    - ``` \text{This is regular text} ```
    - ``` \textbf{This is bold text} ```
    - ``` \textit{This is italic text} ```
2. Equations in proper LaTeX environments `\begin{equation}...\end{equation}`, optionally with a `\tag{...}`
    - ``` \begin{equation} a^2+b^2=c^2 \tag{6.83} \end{equation} ```
3. Small equation segments within a text environment, wrapped in a `$...$`
    - ``` \text{This text shows an equation $\frac{a}{b}$ halfway the text segment} ```
4. Small text segments within an equation environment, wrapped in a `\text{...}`
    - ``` \begin{equation} 10^3 - 317 = 683 \ \text{mm} \end{equation} ```
5. Formatted sections with titles and (sub)(sub)sections
    - ``` \title{This is a title} ```
    - ``` \section{This is a section} ```
    - ``` \subsection{This is a subsection} ```
    - ``` \subsubsection{This is a subsubsection} ```
6. Tables using `\begin{table}...\end{table}` with support for `\toprule`, `\midrule`, and `\bottomrule`
    - ``` \begin{table}[h] \centering \begin{tabular}{lll} \toprule Check & Utilization & Status \\ \midrule \text{Concrete strut capacity} & 0.588 & \text{PASS} \\ \text{Torsion moment capacity} & 4.825 & \text{FAIL} \\ \bottomrule \end{tabular} \end{table} ```
7. Figures with `\begin{figure}...\end{figure}` and `\includegraphics`
    - ``` \begin{figure}[h] \centering \includegraphics[width=0.9\textwidth]{path_to_image} \end{figure} ```
8. Itemized lists with `\begin{itemize}...\end{itemize}`. use `\item` for each bullet.
    - ``` \begin{itemize} \item Bullet 1 \item Bullet 2 \end{itemize} ```
9. Numbered lists with `\begin{enumerate}...\end{enumerate}`. use `\item` for each bullet.
    - ``` \begin{enumerate} \item Number 1 \item Number 2 \end{enumerate} ```
10. New lines (enter / return) with `\newline`
    - ``` \text{line 1} \newline \text{line 2} ```

To ensure exact formatting, it is recommended to use the `LatexReport` adder functions. 

Output can be directly converted to Word documents using `ReportToWordConverter`

## Comprehensive Example when making a report from a Blueprints Formula

The `blueprints` project supports a wide range of report features. Here's a complete demonstration using actual Eurocode formulas,
with two options:
- Get the report as LaTeX string, which can be copy-pasted to a LaTeX-handler, e.g. Overleaf;
- Convert the report to a .docx, which can be saved locally.

```python exec="on" source="material-block" session="report-demo" result="ansi"
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state import formula_6_5
from blueprints.codes.report import LatexReport

# Example: Unity Check for Tensile Strength
formula = formula_6_5.Form6Dot5UnityCheckTensileStrength(
    n_ed=150000,  # 150 kN tensile force
    n_t_rd=200000,  # 200 kN resistance
)

# Generate report output, this LaTeX string can be copy-pasted to a LaTeX-handler, e.g. Overleaf
report = LatexReport().add_formula(formula, "complete")
print(report)
```

## Comprehensive Example when making a report from a Check
To be filled in when steel check is converted to this format


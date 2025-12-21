# LaTeX to Word Converter Examples

This notebook demonstrates how to use the `LatexToWordConverter` to convert LaTeX formulas and text into Word documents.

First, import the `LatexToWordConverter` class from the `blueprints.latex_to_word_document` module.

```python
from blueprints.latex_to_word_document import LatexToWordConverter
```

Example 1 demonstrates how to convert a single line of LaTeX containing both text and a formula. Note that text and formulas should always be on separate lines in the output Word document.

```python
example_latex = r"\text{With formula 6.83:} \newline E = mc^2 = 5.3 \cdot 299792458^{2} J"
doc = LatexToWordConverter().convert_to_word(example_latex)
doc.save("example_1_latex_to_word.docx")
print("Word document created: example_1_latex_to_word.docx")
```

Example 1b demonstrates the same LaTeX-to-Word conversion as Example 1, but also shows how to use the `TranslateLatex` module to translate the LaTeX text before converting it to Word. This is useful if you want to localize the text in your formulas before document generation.

```python
from blueprints.language.translate import TranslateLatex

# Use the same LaTeX as Example 1
example_latex = r"\text{With formula 6.83:} \newline E = mc^2 = 5.3 \cdot 299792458^{2} J"

# Translate the LaTeX text to Dutch (or any supported language)
translated_latex = str(TranslateLatex(example_latex, dest_language="nl"))

print("Translated LaTeX: \n", translated_latex)

# Now convert the translated LaTeX to Word
doc_translated = LatexToWordConverter().convert_to_word(translated_latex)
doc_translated.save("example_1b_latex_to_word_translated.docx")
print("Word document created: example_1b_latex_to_word_translated.docx")
```

Example 2 shows how to convert multiple LaTeX lines, each containing either text or a formula, into a Word document. Each entry in the list will appear on a separate line in the output.

```python
example_formulas = [
    r"\text{Einstein's mass-energy equivalence:} \newline E = mc^2",
    r"\text{Pythagorean theorem:} \newline a^2 + b^2 = c^2",
    r"\text{Quadratic formula:} \newline x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
    r"\text{Improper integral:} \newline \int_0^\infty e^{-x} dx = 1",
    r"\text{Basel problem:} \newline \sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}",
    r"\text{Sine limit:} \newline \lim_{x \to 0} \frac{\sin x}{x} = 1",
    r"\text{Square root of 2:} \newline \sqrt{2}",
    r"\text{Greek letters:} \newline \alpha + \beta = \gamma",
    r"\text{Fraction multiplication:} \newline \frac{a}{b} \cdot \frac{c}{d} = \frac{ac}{bd}",
    r"\text{Binomial squared:} \newline \left( \frac{a+b}{c-d} \right)^2",
]
doc3 = LatexToWordConverter().convert_to_word(r" \newline".join(example_formulas))
doc3.save("example_2_latex_to_word.docx")
print("Word document created: example_2_latex_to_word.docx")
```

Example 3 demonstrates how to use a LaTeX formula from a code implementation, such as a Eurocode check. Here, we use the LaTeX for EN 1993-1-1:2005 formula 6.5 (unity check for tensile strength):

$$
\left( \frac{N_{Ed}}{N_{t,Rd}} \leq 1 \right)
$$

This formula checks if the design tensile force does not exceed the design resistance.

```python
from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_5 import Form6Dot5UnityCheckTensileStrength

latex_formula_6_5 = Form6Dot5UnityCheckTensileStrength(n_ed=123, n_t_rd=683).latex(n=1).__str__()
print(latex_formula_6_5)
doc_formula_6_5 = LatexToWordConverter().convert_to_word(latex_formula_6_5)
doc_formula_6_5.save("example_3_formula_6_5.docx")
print("Word document created: example_3_formula_6_5.docx")
```

Example 4 demonstrates how to use a LaTeX formula from a code implementation for nominal concrete cover calculations. This is useful for structural engineering checks, such as determining the minimum required concrete cover for reinforcement according to standards.

Below, we extract the LaTeX representation from the `NominalConcreteCover` class and convert it to a Word document.

```python
from blueprints.checks.nominal_concrete_cover.nominal_concrete_cover import NominalConcreteCover
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover.constants import (
    AbrasionClass,
    CastingSurface,
    NominalConcreteCoverConstants,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover.table_4_3 import Table4Dot3ConcreteStructuralClass
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass

# Example values for the calculation (adjust as needed)
concrete_material = ConcreteMaterial(concrete_class=ConcreteStrengthClass.C30_37)
structural_class = Table4Dot3ConcreteStructuralClass(
    exposure_classes=["XC1"],
    design_working_life=100,
    concrete_material=concrete_material,
    plate_geometry=False,
    quality_control=False,
)
cover = NominalConcreteCover(
    reinforcement_diameter=32,
    nominal_max_aggregate_size=32,
    constants=NominalConcreteCoverConstants(),
    structural_class=structural_class,
    carbonation="XC1",
    delta_c_dur_gamma=10,
    delta_c_dur_add=0,
    casting_surface=CastingSurface.PREPARED_GROUND,
    uneven_surface=False,
    abrasion_class=AbrasionClass.NA,
)

latex_nominal_cover = cover.latex().__str__()
print(latex_nominal_cover)
doc_nominal_cover = LatexToWordConverter().convert_to_word(latex_nominal_cover)
doc_nominal_cover.save("example_4_nominal_concrete_cover.docx")
print("Word document created: example_4_nominal_concrete_cover.docx")
```

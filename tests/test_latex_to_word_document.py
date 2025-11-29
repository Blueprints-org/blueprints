"""Tests for the LatexToWordConverter class."""

from blueprints.latex_to_word_document import LatexToWordConverter


class TestLatexToWordConverter:
    """Tests for the LatexToWordConverter class."""

    def test_empty_input_returns_empty_document(self) -> None:
        """Test that an empty LaTeX string returns an empty Document."""
        assert LatexToWordConverter("")

    def test_example_formulas_creates_document_with_paragraph(self) -> None:
        """Test that example LaTeX formulas create a Document with content."""
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

        assert LatexToWordConverter(r" \newline".join(example_formulas))

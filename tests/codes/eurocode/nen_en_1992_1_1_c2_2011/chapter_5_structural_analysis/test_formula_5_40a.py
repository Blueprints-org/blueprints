"""Testing formula 5.40a of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_5_structural_analysis.formula_5_40a import Form5Dot40aCheckLateralInstability


class TestForm5Dot40aCheckLateralInstability:
    """Validation for formula 5.40a from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        l_0t = 6.0  # m
        b = 0.3  # m
        h = 0.5  # m

        # Object to test
        formula = Form5Dot40aCheckLateralInstability(l_0t=l_0t, b=b, h=h)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \left( \frac{l_{0t}}{b} \leq \frac{50}{\left( h/b \right)^{1/3}} \text{ and } \frac{h}{b} \leq 2.5 \right) \to "
                r"\left( \frac{6.000}{0.300} \leq \frac{50}{\left( 0.500/0.300 \right)^{1/3}} \text{ and } "
                r"\frac{0.500}{0.300} \leq 2.5 \right) \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        l_0t = 6.0  # m
        b = 0.3  # m
        h = 0.5  # m

        # Object to test
        latex = Form5Dot40aCheckLateralInstability(l_0t=l_0t, b=b, h=h).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

"""Testing formula 5.31 of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_5_structural_analysis.formula_5_31 import Form5Dot31DesignMoment


class TestForm5Dot31DesignMoment:
    """Validation for formula 5.31 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        m_0ed = 50.0
        m_2 = 10.0

        # Object to test
        formula = Form5Dot31DesignMoment(m_0ed=m_0ed, m_2=m_2)

        # Expected result, manually calculated
        manually_calculated_result = 60.0  # kNm

        assert formula == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"M_{Ed} = M_{0Ed} + M_{2} = 50.000 + 10.000 = 60.000 \text{ kNm}",
            ),
            ("short", r"M_{Ed} = 60.000 \text{ kNm}"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        m_0ed = 50.0
        m_2 = 10.0

        # Object to test
        latex = Form5Dot31DesignMoment(m_0ed=m_0ed, m_2=m_2).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

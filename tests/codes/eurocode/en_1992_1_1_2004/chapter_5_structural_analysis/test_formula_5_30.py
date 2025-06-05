"""Testing formula 5.30 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_30 import Form5Dot30TotalDesignMoment
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot30TotalDesignMoment:
    """Validation for formula 5.30 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        m_0ed = 50.0
        n_ed = 100.0
        n_b = 200.0

        # Object to test
        formula = Form5Dot30TotalDesignMoment(m_0ed=m_0ed, n_ed=n_ed, n_b=n_b)

        # Expected result, manually calculated
        manually_calculated_result = 100.0  # kNm

        assert formula == pytest.approx(manually_calculated_result, rel=1e-4)

    def test_evaluation_at_capacity_normalforce(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        m_0ed = 50.0
        n_ed = 200.0
        n_b = 200.0

        # Object to test
        formula = Form5Dot30TotalDesignMoment(m_0ed=m_0ed, n_ed=n_ed, n_b=n_b)

        # Expected result, manually calculated
        manually_calculated_result = 1e9  # kNm

        assert formula == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("m_0ed", "n_ed", "n_b"),
        [
            (-50.0, 100.0, 200.0),  # m_0ed is negative
            (50.0, -100.0, 200.0),  # n_ed is negative
            (50.0, 100.0, -200.0),  # n_b is negative
            (50.0, 100.0, 0.0),  # n_b is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, m_0ed: float, n_ed: float, n_b: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot30TotalDesignMoment(m_0ed=m_0ed, n_ed=n_ed, n_b=n_b)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"M_{Ed} = \frac{M_{0Ed}}{1 - \left(\frac{N_{Ed}}{N_{B}}\right)} = "
                r"\frac{50.000}{1 - \left(\frac{100.000}{200.000}\right)} = 100.000 \ kNm",
            ),
            ("short", r"M_{Ed} = 100.000 \ kNm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        m_0ed = 50.0
        n_ed = 100.0
        n_b = 200.0

        # Object to test
        latex = Form5Dot30TotalDesignMoment(m_0ed=m_0ed, n_ed=n_ed, n_b=n_b).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

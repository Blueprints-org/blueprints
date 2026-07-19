"""Testing formula 5.2 of NEN-EN 1993-1-1+C2+A1:2016."""

import pytest

from blueprints.codes.eurocode.national_annex.nl.nen_en_1993_1_1_c2_a1_2016.chapter_5_structural_analysis.formula_5_2 import (
    Form5Dot2ElasticCriticalBucklingFactor,
)
from blueprints.validations import LessOrEqualToZeroError, MismatchSignError


class TestForm5Dot2ElasticCriticalBucklingFactor:
    """Validation for formula 5.2 from NEN-EN 1993-1-1+C2+A1:2016."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        h_ed = 100000.0
        v_ed = 500000.0
        h = 3500.0
        delta_h_ed = 10.0

        # Object to test
        formula = Form5Dot2ElasticCriticalBucklingFactor(h_ed=h_ed, v_ed=v_ed, h=h, delta_h_ed=delta_h_ed)

        # Expected result, manually calculated
        manually_calculated_result = 70.0  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_negative(self) -> None:
        """Tests the evaluation of the result with matching negative forces."""
        h_ed = -100000.0
        v_ed = -500000.0
        h = 3500.0
        delta_h_ed = 10.0

        formula = Form5Dot2ElasticCriticalBucklingFactor(h_ed=h_ed, v_ed=v_ed, h=h, delta_h_ed=delta_h_ed)
        manually_calculated_result = 70.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("h_ed", "v_ed", "h", "delta_h_ed", "expected_exception"),
        [
            (100.0, -500.0, 3500.0, 10.0, MismatchSignError),  # h_ed and v_ed have mismatch sign
            (-100.0, 500.0, 3500.0, 10.0, MismatchSignError),  # h_ed and v_ed have mismatch sign
            (100.0, 0.0, 3500.0, 10.0, LessOrEqualToZeroError),  # v_ed is zero
            (100.0, 500.0, 0.0, 10.0, LessOrEqualToZeroError),  # h is zero
            (100.0, 500.0, -3500.0, 10.0, LessOrEqualToZeroError),  # h is negative
            (100.0, 500.0, 3500.0, 0.0, LessOrEqualToZeroError),  # delta_h_ed is zero
            (100.0, 500.0, 3500.0, -10.0, LessOrEqualToZeroError),  # delta_h_ed is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self, h_ed: float, v_ed: float, h: float, delta_h_ed: float, expected_exception: type[Exception]
    ) -> None:
        """Test invalid values."""
        with pytest.raises(expected_exception):
            Form5Dot2ElasticCriticalBucklingFactor(h_ed=h_ed, v_ed=v_ed, h=h, delta_h_ed=delta_h_ed)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\alpha_{cr} = \frac{H_{Ed}}{V_{Ed}} \cdot \frac{h}{\delta_{H,Ed}} = "
                r"\frac{100000.000}{500000.000} \cdot \frac{3500.000}{10.000} = 70.000",
            ),
            (
                "complete_with_units",
                r"\alpha_{cr} = \frac{H_{Ed}}{V_{Ed}} \cdot \frac{h}{\delta_{H,Ed}} = "
                r"\frac{100000.000 \ N}{500000.000 \ N} \cdot \frac{3500.000 \ mm}{10.000 \ mm} = 70.000",
            ),
            ("short", r"\alpha_{cr} = 70.000"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        h_ed = 100000.0
        v_ed = 500000.0
        h = 3500.0
        delta_h_ed = 10.0

        # Object to test
        latex = Form5Dot2ElasticCriticalBucklingFactor(h_ed=h_ed, v_ed=v_ed, h=h, delta_h_ed=delta_h_ed).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

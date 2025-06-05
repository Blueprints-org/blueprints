"""Testing formula 5.38b of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_38b import Form5Dot38bCheckRelativeEccentricityRatio
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot38bCheckRelativeEccentricityRatio:
    """Validation for formula 5.38b from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        e_y = 30.0
        e_z = 4.0
        b_eq = 100.0
        h_eq = 101.0

        # Object to test
        formula = Form5Dot38bCheckRelativeEccentricityRatio(e_y=e_y, e_z=e_z, b_eq=b_eq, h_eq=h_eq)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    def test_evaluation_excentricity_zero(self) -> None:
        """Tests the evaluation of the result with e=0."""
        # Example values
        e_y = 30.0
        e_z = 0.0
        b_eq = 100.0
        h_eq = 101.0

        # Object to test
        formula = Form5Dot38bCheckRelativeEccentricityRatio(e_y=e_y, e_z=e_z, b_eq=b_eq, h_eq=h_eq)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("e_y", "e_z", "b_eq", "h_eq"),
        [
            (-30.0, 4.0, 100.0, 101.0),  # e_y is negative
            (30.0, -4.0, 100.0, 101.0),  # e_z is negative
            (30.0, 4.0, -100.0, 101.0),  # b_eq is negative
            (30.0, 4.0, 100.0, -101.0),  # h_eq is negative
            (30.0, 4.0, 0.0, 101.0),  # b_eq is zero
            (30.0, 4.0, 100.0, 0.0),  # h_eq is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, e_y: float, e_z: float, b_eq: float, h_eq: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot38bCheckRelativeEccentricityRatio(e_y=e_y, e_z=e_z, b_eq=b_eq, h_eq=h_eq)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \left(\frac{e_{y}/h_{eq}}{e_{z}/b_{eq}} \leq 0.2 \text{ or } \frac{e_{z}/b_{eq}}{e_{y}/h_{eq}} \leq 0.2 \right) \to"
                r" \left(\frac{30.000/101.000}{4.000/100.000} \leq 0.2 \text{ or } \frac{4.000/100.000}{30.000/101.000} \leq 0.2 \right) \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        e_y = 30.0
        e_z = 4.0
        b_eq = 100.0
        h_eq = 101.0

        # Object to test
        latex = Form5Dot38bCheckRelativeEccentricityRatio(e_y=e_y, e_z=e_z, b_eq=b_eq, h_eq=h_eq).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

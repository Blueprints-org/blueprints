"""Testing formula 8.58 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2025.chapter_8_ultimate_limit_state.formula_8_58 import Form8Dot58LongitudinalStressClass4CrossSections
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot58LongitudinalStressClass4CrossSections:
    """Validation for formula 8.58 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        sigma_x_ed = 200.0  # MPa
        f_y = 355.0  # MPa
        gamma_m0 = 1.0  # -

        # Object to test
        formula = Form8Dot58LongitudinalStressClass4CrossSections(sigma_x_ed=sigma_x_ed, f_y=f_y, gamma_m0=gamma_m0)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result
        assert formula.unity_check == sigma_x_ed / (f_y / gamma_m0)

    @pytest.mark.parametrize(
        ("sigma_x_ed", "f_y", "gamma_m0"),
        [
            (200.0, 355.0, 0.0),  # gamma_m0 is zero
            (200.0, 355.0, -1.0),  # gamma_m0 is negative
            (-10.0, 355.0, 1.0),  # sigma_x_ed is negative
            (200.0, -50.0, 1.0),  # f_y is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, sigma_x_ed: float, f_y: float, gamma_m0: float) -> None:
        """Test invalid values."""
        with pytest.raises((LessOrEqualToZeroError, NegativeValueError)):
            Form8Dot58LongitudinalStressClass4CrossSections(sigma_x_ed=sigma_x_ed, f_y=f_y, gamma_m0=gamma_m0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \sigma_{x,Ed} \leq \frac{f_y}{\gamma_{M0}} \to 200.000 \leq \frac{355.000}{1.000} \to OK",
            ),
            ("short", r"CHECK \to OK"),
            (
                "complete_with_units",
                r"CHECK \to \sigma_{x,Ed} \leq \frac{f_y}{\gamma_{M0}} \to 200.000 \ MPa \leq \frac{355.000 \ MPa}{1.000} \to OK",
            ),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        sigma_x_ed = 200.0  # MPa
        f_y = 355.0  # MPa
        gamma_m0 = 1.0  # -

        # Object to test
        latex = Form8Dot58LongitudinalStressClass4CrossSections(sigma_x_ed=sigma_x_ed, f_y=f_y, gamma_m0=gamma_m0).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
            "complete_with_units": latex.complete_with_units,
        }

        assert expected == actual[representation], f"{representation} representation failed."

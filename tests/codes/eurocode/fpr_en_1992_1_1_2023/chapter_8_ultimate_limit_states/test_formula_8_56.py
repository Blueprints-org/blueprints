"""Testing formula 8.56 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_56 import Form8Dot56StressInShearReinforcement
from blueprints.validations import NegativeValueError


class TestForm8Dot56StressInShearReinforcement:
    """Validation for formula 8.56 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("cot_theta", "epsilon_x", "expected"),
        [
            # 200000 * (0.8^2 * (0.001 + 0.001) - 0.001) = 200000 * 0.00028, well below f_ywd
            (0.8, 0.001, 56.0),
            # 200000 * (2^2 * (0.005 + 0.001) - 0.001) = 4600, so f_ywd governs
            (2.0, 0.005, 435.0),
        ],
    )
    def test_evaluation(self, cot_theta: float, epsilon_x: float, expected: float) -> None:
        """Tests the evaluation of the result, both below and at the upper bound."""
        # Create object to test
        formula = Form8Dot56StressInShearReinforcement(e_s=200000.0, cot_theta=cot_theta, epsilon_x=epsilon_x, f_ywd=435.0)

        # Perform test by assert
        assert formula == pytest.approx(expected=expected, rel=1e-4)

    def test_result_is_not_clamped_at_zero(self) -> None:
        """The standard prints only an upper bound. A small cotangent combined with a small longitudinal strain
        gives a negative stress, and that result is returned unchanged rather than clamped, since a clamp would
        be an addition beyond the printed text.
        """
        # Example values
        formula = Form8Dot56StressInShearReinforcement(e_s=200000.0, cot_theta=0.5, epsilon_x=0.0, f_ywd=435.0)

        # 200000 * (0.5^2 * (0 + 0.001) - 0.001) = 200000 * -0.00075
        assert formula == pytest.approx(expected=-150.0, rel=1e-4)

    @pytest.mark.parametrize(
        ("e_s", "cot_theta", "epsilon_x", "f_ywd"),
        [
            (-200000.0, 0.8, 0.001, 435.0),  # e_s is negative
            (200000.0, -0.8, 0.001, 435.0),  # cot_theta is negative
            (200000.0, 0.8, -0.001, 435.0),  # epsilon_x is negative
            (200000.0, 0.8, 0.001, -435.0),  # f_ywd is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, e_s: float, cot_theta: float, epsilon_x: float, f_ywd: float) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot56StressInShearReinforcement(e_s=e_s, cot_theta=cot_theta, epsilon_x=epsilon_x, f_ywd=f_ywd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\sigma_{swd} = \min\left(E_s \cdot \left[\left(\cot(\theta)\right)^2 \cdot "
                r"\left(\varepsilon_x + 0.001\right) - 0.001\right], f_{ywd}\right) = "
                r"\min\left(200000.000 \cdot \left[\left(0.800\right)^2 \cdot "
                r"\left(0.001 + 0.001\right) - 0.001\right], 435.000\right) = 56.000 \ MPa",
            ),
            (
                "complete_with_units",
                r"\sigma_{swd} = \min\left(E_s \cdot \left[\left(\cot(\theta)\right)^2 \cdot "
                r"\left(\varepsilon_x + 0.001\right) - 0.001\right], f_{ywd}\right) = "
                r"\min\left(200000.000 \ MPa \cdot \left[\left(0.800\right)^2 \cdot "
                r"\left(0.001 + 0.001\right) - 0.001\right], 435.000 \ MPa\right) = 56.000 \ MPa",
            ),
            ("short", r"\sigma_{swd} = 56.000 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        test_latex = Form8Dot56StressInShearReinforcement(e_s=200000.0, cot_theta=0.8, epsilon_x=0.001, f_ywd=435.0).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]

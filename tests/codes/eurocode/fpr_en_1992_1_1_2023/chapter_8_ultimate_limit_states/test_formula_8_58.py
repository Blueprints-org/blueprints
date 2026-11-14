"""Testing formula 8.58 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_58 import (
    Form8Dot58CheckCotangentInclinedShearReinforcement,
    SubForm8Dot58LowerBound,
    SubForm8Dot58UpperBound,
)
from blueprints.validations import GreaterThan90Error, LessOrEqualToZeroError

# Angles chosen so that their cotangents are round numbers, which keeps the hand calculations readable
THETA_COT_0_5 = 63.434948822922  # cot(theta) = 0.5
THETA_COT_0_9 = 48.012787504183  # cot(theta) = 0.9
THETA_COT_1 = 45.0  # cot(theta) = 1
THETA_COT_2 = 26.565051177078  # cot(theta) = 2
THETA_COT_2_5 = 21.801409486352  # cot(theta) = 2.5
THETA_COT_3 = 18.434948822922  # cot(theta) = 3


class TestForm8Dot58CheckCotangentInclinedShearReinforcement:
    """Validation for formula 8.58 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("theta", "theta_min", "alpha_w", "expected"),
        [
            (THETA_COT_2, THETA_COT_2_5, 60.0, True),  # inside the range, lower bound tan(30) = 0.577
            (THETA_COT_2_5, THETA_COT_2_5, 60.0, True),  # at the upper bound, which is inclusive
            (THETA_COT_3, THETA_COT_2_5, 60.0, False),  # above the upper bound
            # The same theta passes or fails depending only on the inclination of the reinforcement:
            # tan(22.5) = 0.414 lets cot(theta) = 0.5 through, tan(30) = 0.577 does not.
            (THETA_COT_0_5, THETA_COT_2_5, 45.0, True),
            (THETA_COT_0_5, THETA_COT_2_5, 60.0, False),
            # alpha_w = 90 degrees lies outside the printed range of 45 <= alpha_w < 90, so these two are a
            # transcription check and not a supported use: the lower bound becomes tan(45) = 1 and the formula
            # reproduces the (8.41) it replaces.
            (THETA_COT_1, THETA_COT_2_5, 90.0, True),
            (THETA_COT_0_9, THETA_COT_2_5, 90.0, False),
        ],
    )
    def test_evaluation(self, theta: float, theta_min: float, alpha_w: float, expected: bool) -> None:
        """Tests the evaluation of the result."""
        # Create object to test
        formula = Form8Dot58CheckCotangentInclinedShearReinforcement(theta=theta, theta_min=theta_min, alpha_w=alpha_w)

        # Perform test by assert
        assert bool(formula) is expected

    def test_lower_bound_is_inclusive(self) -> None:
        """The lower bound is printed with a less than or equal sign, so a theta exactly on it passes.

        At alpha_w = 60 degrees the bound reads tan(30) <= cot(theta), which theta = 60 degrees meets exactly.
        """
        formula = Form8Dot58CheckCotangentInclinedShearReinforcement(theta=60.0, theta_min=THETA_COT_2_5, alpha_w=60.0)

        assert bool(formula) is True

    @pytest.mark.parametrize(
        ("theta", "expected_unity_check"),
        [
            # the upper bound governs: 2.0 / 2.5
            (THETA_COT_2, 0.8),
            # the lower bound governs: tan(30) / 0.5
            (THETA_COT_0_5, 1.1547005383792515),
            # the upper bound governs and is violated: 3.0 / 2.5
            (THETA_COT_3, 1.2),
        ],
    )
    def test_unity_check_is_the_governing_bound(self, theta: float, expected_unity_check: float) -> None:
        """Aggregating with all takes the largest unity check, so the governing bound is the one reported."""
        # Create object to test
        formula = Form8Dot58CheckCotangentInclinedShearReinforcement(theta=theta, theta_min=THETA_COT_2_5, alpha_w=60.0)

        # Perform test by assert
        assert formula.unity_check == pytest.approx(expected=expected_unity_check, rel=1e-4)

    def test_both_bounds_are_exposed_separately(self) -> None:
        """Each half of the printed range keeps its own left-hand side, right-hand side and unity check."""
        # Example values
        formula = Form8Dot58CheckCotangentInclinedShearReinforcement(theta=THETA_COT_2, theta_min=THETA_COT_2_5, alpha_w=60.0)
        lower, upper = formula.comparison_formulas

        # Perform test by assert
        assert lower.lhs == pytest.approx(expected=0.5773502691896257, rel=1e-4)
        assert lower.rhs == pytest.approx(expected=2.0, rel=1e-4)
        assert upper.lhs == pytest.approx(expected=2.0, rel=1e-4)
        assert upper.rhs == pytest.approx(expected=2.5, rel=1e-4)

    @pytest.mark.parametrize(
        ("theta", "theta_min", "alpha_w"),
        [
            (0.0, THETA_COT_2_5, 60.0),  # theta is zero, for which the cotangent diverges
            (-THETA_COT_2, THETA_COT_2_5, 60.0),  # theta is negative
            (THETA_COT_2, 0.0, 60.0),  # theta_min is zero, for which the cotangent diverges
            (THETA_COT_2, -THETA_COT_2_5, 60.0),  # theta_min is negative
            (THETA_COT_2, THETA_COT_2_5, 0.0),  # alpha_w is zero
            (THETA_COT_2, THETA_COT_2_5, -60.0),  # alpha_w is negative
        ],
    )
    def test_raise_error_when_the_angles_are_less_or_equal_to_zero(self, theta: float, theta_min: float, alpha_w: float) -> None:
        """All three inputs are inclinations, so none of them can be zero or less."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot58CheckCotangentInclinedShearReinforcement(theta=theta, theta_min=theta_min, alpha_w=alpha_w)

    @pytest.mark.parametrize(
        ("theta", "theta_min", "alpha_w"),
        [
            (120.0, THETA_COT_2_5, 60.0),  # theta exceeds 90 degrees
            (THETA_COT_2, 120.0, 60.0),  # theta_min exceeds 90 degrees
            (THETA_COT_2, THETA_COT_2_5, 120.0),  # alpha_w exceeds 90 degrees
        ],
    )
    def test_raise_error_when_the_angles_exceed_90_degrees(self, theta: float, theta_min: float, alpha_w: float) -> None:
        """The standard says inclinations of the reinforcement above 90 degrees should be avoided, and the
        Formulae (8.59) and (8.60) of the same clause refuse them, so this check refuses them too.
        """
        with pytest.raises(GreaterThan90Error):
            Form8Dot58CheckCotangentInclinedShearReinforcement(theta=theta, theta_min=theta_min, alpha_w=alpha_w)

    @pytest.mark.parametrize(
        ("theta", "representation", "expected"),
        [
            (
                THETA_COT_2,
                "complete",
                (
                    r"CHECK \to \tan\left(\frac{\alpha_w}{2}\right) \leq \cot(\theta) \leq \cot(\theta_{min}) \to "
                    r"\tan\left(\frac{60.000}{2}\right) \leq \cot(26.565) \leq \cot(21.801) \to OK"
                ),
            ),
            (
                THETA_COT_2,
                "complete_with_units",
                (
                    r"CHECK \to \tan\left(\frac{\alpha_w}{2}\right) \leq \cot(\theta) \leq \cot(\theta_{min}) \to "
                    r"\tan\left(\frac{60.000 ^\circ}{2}\right) \leq \cot(26.565 ^\circ) \leq \cot(21.801 ^\circ) \to OK"
                ),
            ),
            (THETA_COT_2, "short", r"CHECK \to OK"),
            (
                THETA_COT_3,
                "complete",
                (
                    r"CHECK \to \tan\left(\frac{\alpha_w}{2}\right) \leq \cot(\theta) \leq \cot(\theta_{min}) \to "
                    r"\tan\left(\frac{60.000}{2}\right) \leq \cot(18.435) \leq \cot(21.801) \to \text{Not OK}"
                ),
            ),
            (THETA_COT_3, "short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, theta: float, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        test_latex = Form8Dot58CheckCotangentInclinedShearReinforcement(theta=theta, theta_min=THETA_COT_2_5, alpha_w=60.0).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]


class TestSubForm8Dot58Bounds:
    """Validation for the two halves of formula 8.58 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("theta", "expected", "expected_latex"),
        [
            (
                THETA_COT_2,
                True,
                (
                    r"CHECK \to \tan\left(\frac{\alpha_w}{2}\right) \leq \cot(\theta) \to "
                    r"\tan\left(\frac{60.000}{2}\right) \leq \cot(26.565) \to OK"
                ),
            ),
            (
                THETA_COT_0_5,
                False,
                (
                    r"CHECK \to \tan\left(\frac{\alpha_w}{2}\right) \leq \cot(\theta) \to "
                    r"\tan\left(\frac{60.000}{2}\right) \leq \cot(63.435) \to \text{Not OK}"
                ),
            ),
        ],
    )
    def test_lower_bound(self, theta: float, expected: bool, expected_latex: str) -> None:
        """Tests the lower bound on its own."""
        # Create object to test
        formula = SubForm8Dot58LowerBound(theta=theta, alpha_w=60.0)

        # Perform test by assert
        assert bool(formula) is expected
        assert formula.latex().complete == expected_latex

    @pytest.mark.parametrize(
        ("theta", "expected", "expected_latex"),
        [
            (THETA_COT_2, True, r"CHECK \to \cot(\theta) \leq \cot(\theta_{min}) \to \cot(26.565) \leq \cot(21.801) \to OK"),
            (
                THETA_COT_3,
                False,
                r"CHECK \to \cot(\theta) \leq \cot(\theta_{min}) \to \cot(18.435) \leq \cot(21.801) \to \text{Not OK}",
            ),
        ],
    )
    def test_upper_bound(self, theta: float, expected: bool, expected_latex: str) -> None:
        """Tests the upper bound on its own."""
        # Create object to test
        formula = SubForm8Dot58UpperBound(theta=theta, theta_min=THETA_COT_2_5)

        # Perform test by assert
        assert bool(formula) is expected
        assert formula.latex().complete == expected_latex

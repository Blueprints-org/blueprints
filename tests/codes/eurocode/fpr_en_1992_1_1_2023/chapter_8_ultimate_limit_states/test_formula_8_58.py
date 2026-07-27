"""Testing formula 8.58 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_58 import (
    Form8Dot58CheckCotangentInclinedShearReinforcement,
    SubForm8Dot58LowerBound,
    SubForm8Dot58UpperBound,
)


class TestForm8Dot58CheckCotangentInclinedShearReinforcement:
    """Validation for formula 8.58 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("cot_theta", "cot_theta_min", "alpha_w", "expected"),
        [
            (2.0, 2.5, 60.0, True),  # inside the range, lower bound tan(30) = 0.577
            (2.5, 2.5, 60.0, True),  # at the upper bound, which is inclusive
            (3.0, 2.5, 60.0, False),  # above the upper bound
            # The same cot_theta passes or fails depending only on the inclination of the reinforcement:
            # tan(22.5) = 0.414 lets 0.5 through, tan(30) = 0.577 does not.
            (0.5, 2.5, 45.0, True),
            (0.5, 2.5, 60.0, False),
            # alpha_w = 90 degrees lies outside the printed range of 45 <= alpha_w < 90, so these two are a
            # transcription check and not a supported use: the lower bound becomes tan(45) = 1 and the formula
            # reproduces the (8.41) it replaces.
            (1.0, 2.5, 90.0, True),
            (0.9, 2.5, 90.0, False),
        ],
    )
    def test_evaluation(self, cot_theta: float, cot_theta_min: float, alpha_w: float, expected: bool) -> None:
        """Tests the evaluation of the result."""
        # Create object to test
        formula = Form8Dot58CheckCotangentInclinedShearReinforcement(cot_theta=cot_theta, cot_theta_min=cot_theta_min, alpha_w=alpha_w)

        # Perform test by assert
        assert bool(formula) is expected

    def test_lower_bound_is_inclusive(self) -> None:
        """The lower bound is printed with a less than or equal sign, so a cot_theta exactly on it passes."""
        # tan(30 degrees) to the precision the class computes it with
        formula = Form8Dot58CheckCotangentInclinedShearReinforcement(cot_theta=0.5773502691896257, cot_theta_min=2.5, alpha_w=60.0)

        assert bool(formula) is True

    @pytest.mark.parametrize(
        ("cot_theta", "expected_unity_check"),
        [
            # the upper bound governs: 2.0 / 2.5
            (2.0, 0.8),
            # the lower bound governs: tan(30) / 0.5
            (0.5, 1.1547005383792515),
            # the upper bound governs and is violated: 3.0 / 2.5
            (3.0, 1.2),
        ],
    )
    def test_unity_check_is_the_governing_bound(self, cot_theta: float, expected_unity_check: float) -> None:
        """Aggregating with all takes the largest unity check, so the governing bound is the one reported."""
        # Create object to test
        formula = Form8Dot58CheckCotangentInclinedShearReinforcement(cot_theta=cot_theta, cot_theta_min=2.5, alpha_w=60.0)

        # Perform test by assert
        assert formula.unity_check == pytest.approx(expected=expected_unity_check, rel=1e-4)

    def test_both_bounds_are_exposed_separately(self) -> None:
        """Each half of the printed range keeps its own left-hand side, right-hand side and unity check."""
        # Example values
        formula = Form8Dot58CheckCotangentInclinedShearReinforcement(cot_theta=2.0, cot_theta_min=2.5, alpha_w=60.0)
        lower, upper = formula.comparison_formulas

        # Perform test by assert
        assert lower.lhs == pytest.approx(expected=0.5773502691896257, rel=1e-4)
        assert lower.rhs == pytest.approx(expected=2.0, rel=1e-4)
        assert upper.lhs == pytest.approx(expected=2.0, rel=1e-4)
        assert upper.rhs == pytest.approx(expected=2.5, rel=1e-4)

    @pytest.mark.parametrize(
        ("cot_theta", "representation", "expected"),
        [
            (
                2.0,
                "complete",
                r"CHECK \to \tan\left(\frac{\alpha_w}{2}\right) \leq \cot(\theta) \leq \cot(\theta_{min}) \to "
                r"\tan\left(\frac{60.000}{2}\right) \leq 2.000 \leq 2.500 \to OK",
            ),
            (
                2.0,
                "complete_with_units",
                r"CHECK \to \tan\left(\frac{\alpha_w}{2}\right) \leq \cot(\theta) \leq \cot(\theta_{min}) \to "
                r"\tan\left(\frac{60.000 \ degrees}{2}\right) \leq 2.000 \leq 2.500 \to OK",
            ),
            (2.0, "short", r"CHECK \to OK"),
            (
                3.0,
                "complete",
                r"CHECK \to \tan\left(\frac{\alpha_w}{2}\right) \leq \cot(\theta) \leq \cot(\theta_{min}) \to "
                r"\tan\left(\frac{60.000}{2}\right) \leq 3.000 \leq 2.500 \to \text{Not OK}",
            ),
            (3.0, "short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, cot_theta: float, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        test_latex = Form8Dot58CheckCotangentInclinedShearReinforcement(cot_theta=cot_theta, cot_theta_min=2.5, alpha_w=60.0).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]


class TestSubForm8Dot58Bounds:
    """Validation for the two halves of formula 8.58 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("cot_theta", "expected", "expected_latex"),
        [
            (
                2.0,
                True,
                r"CHECK \to \tan\left(\frac{\alpha_w}{2}\right) \leq \cot(\theta) \to "
                r"\tan\left(\frac{60.000}{2}\right) \leq 2.000 \to OK",
            ),
            (
                0.5,
                False,
                r"CHECK \to \tan\left(\frac{\alpha_w}{2}\right) \leq \cot(\theta) \to "
                r"\tan\left(\frac{60.000}{2}\right) \leq 0.500 \to \text{Not OK}",
            ),
        ],
    )
    def test_lower_bound(self, cot_theta: float, expected: bool, expected_latex: str) -> None:
        """Tests the lower bound on its own."""
        # Create object to test
        formula = SubForm8Dot58LowerBound(cot_theta=cot_theta, alpha_w=60.0)

        # Perform test by assert
        assert bool(formula) is expected
        assert formula.latex().complete == expected_latex

    @pytest.mark.parametrize(
        ("cot_theta", "expected", "expected_latex"),
        [
            (2.0, True, r"CHECK \to \cot(\theta) \leq \cot(\theta_{min}) \to 2.000 \leq 2.500 \to OK"),
            (3.0, False, r"CHECK \to \cot(\theta) \leq \cot(\theta_{min}) \to 3.000 \leq 2.500 \to \text{Not OK}"),
        ],
    )
    def test_upper_bound(self, cot_theta: float, expected: bool, expected_latex: str) -> None:
        """Tests the upper bound on its own."""
        # Create object to test
        formula = SubForm8Dot58UpperBound(cot_theta=cot_theta, cot_theta_min=2.5)

        # Perform test by assert
        assert bool(formula) is expected
        assert formula.latex().complete == expected_latex

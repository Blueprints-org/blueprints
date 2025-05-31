"""Testing formula 5.10a from EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_10a import Form5Dot10aRedistributionOfMomentsLowerFck
from blueprints.validations import LessOrEqualToZeroError


class TestForm5Dot10aRedistributionOfMomentsLowerFck:
    """Validation for formula 5.10a from EN 1992-1-1:2004."""

    @pytest.mark.parametrize(
        ("delta", "k1", "k2", "xu", "d", "result_manual"),
        [
            (0.5, 0.44, 1.25, 0.2, 0.5, False),
            (1.0, 0.44, 1.25, 0.2, 0.5, True),
        ],
    )
    def test_comparison(self, delta: float, k1: float, k2: float, xu: float, d: float, result_manual: bool) -> None:
        """Test the evaluation of the comparison."""
        form_5_10a = bool(Form5Dot10aRedistributionOfMomentsLowerFck(delta=delta, k1=k1, k2=k2, xu=xu, d=d))
        assert form_5_10a == pytest.approx(expected=result_manual)

    @pytest.mark.parametrize(
        ("delta", "k1", "k2", "xu", "d"),
        [
            (0.5, 0.44, 1.25, 0.2, 0.5),
            (1.0, 0.44, 1.25, 0.2, 0.5),
        ],
    )
    def test_evaluation(self, delta: float, k1: float, k2: float, xu: float, d: float) -> None:
        """Test the right-hand side evaluation of the result."""
        form_5_10a = Form5Dot10aRedistributionOfMomentsLowerFck(delta=delta, k1=k1, k2=k2, xu=xu, d=d)
        expected_rhs = k1 + k2 * (xu / d)
        assert form_5_10a.right_hand_side == pytest.approx(expected_rhs, abs=1e-3)

    def test_raise_error_if_negative_values(self) -> None:
        """Test that a LessOrEqualToZeroError is raised when a negative or zero value is passed."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot10aRedistributionOfMomentsLowerFck(delta=-0.5, k1=0.44, k2=1.25, xu=0.2, d=0.5)
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot10aRedistributionOfMomentsLowerFck(delta=0.5, k1=0, k2=1.25, xu=0.2, d=0.5)

    @pytest.mark.parametrize(
        ("delta", "k1", "k2", "xu", "d", "expected_lhs_rhs"),
        [
            (0.94, 0.44, 1.25, 0.2, 0.5, 0.94),
            (0.825, 0.2, 1.25, 0.3, 0.6, 0.825),
        ],
    )
    def test_properties(self, delta: float, k1: float, k2: float, xu: float, d: float, expected_lhs_rhs: float) -> None:
        """Test the properties of the comparison."""
        form_5_10a = Form5Dot10aRedistributionOfMomentsLowerFck(delta=delta, k1=k1, k2=k2, xu=xu, d=d)
        assert form_5_10a.left_hand_side == pytest.approx(expected_lhs_rhs, abs=1e-3)
        assert form_5_10a.right_hand_side == pytest.approx(expected_lhs_rhs, abs=1e-3)
        assert form_5_10a.ratio == pytest.approx(1, abs=1e-3)

    def test_str_representation(self) -> None:
        """Test the string representation of the comparison."""
        form_5_10a = Form5Dot10aRedistributionOfMomentsLowerFck(delta=0.5, k1=0.44, k2=1.25, xu=0.2, d=0.5)
        expected_str = (
            r"CHECK \rightarrow \delta \geq k_1 + k_2 \frac{x_u}{d} \rightarrow 0.500 \geq 0.44 + 1.25 \frac{0.2}{" r"0.5} \rightarrow \text{Not OK}"
        )
        assert str(form_5_10a) == expected_str

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \rightarrow \delta \geq k_1 + k_2 \frac{x_u}{d} \rightarrow 0.500 \geq 0.44 + 1.25 \frac{"
                r"0.2}{0.5} \rightarrow \text{Not OK}",
            ),
            ("short", r"CHECK \rightarrow \text{Not OK}"),
        ],
    )
    def test_latex_ok(self, representation: str, expected: str) -> None:
        """Test the latex representation of the comparison."""
        # Example values
        delta = 0.5
        k1 = 0.44
        k2 = 1.25
        xu = 0.2
        d = 0.5

        # Object to test
        form_5_10a_latex = Form5Dot10aRedistributionOfMomentsLowerFck(delta=delta, k1=k1, k2=k2, xu=xu, d=d).latex()

        actual = {
            "complete": form_5_10a_latex.complete,
            "short": form_5_10a_latex.short,
        }

        assert actual[representation] == expected

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \rightarrow \delta \geq k_1 + k_2 \frac{x_u}{d} \rightarrow 2000.000 \geq 0.44 + 1.25 \frac{" r"200}{50} \rightarrow OK",
            ),
            ("short", r"CHECK \rightarrow OK"),
        ],
    )
    def test_latex_not_ok(self, representation: str, expected: str) -> None:
        """Test the latex representation of the comparison."""
        # Example values
        delta = 2000
        k1 = 0.44
        k2 = 1.25
        xu = 200
        d = 50

        # Object to test
        form_5_10a_latex = Form5Dot10aRedistributionOfMomentsLowerFck(delta=delta, k1=k1, k2=k2, xu=xu, d=d).latex()

        actual = {
            "complete": form_5_10a_latex.complete,
            "short": form_5_10a_latex.short,
        }

        assert actual[representation] == expected

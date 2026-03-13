"""Testing Formula E.3 from EN 1995-1-1:2023."""

from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from blueprints.codes.eurocode.en_1995_1_1_2023.appendix_e.formula_e_3 import FormEDot3DistanceCentroidAlpha1
from blueprints.validations import LessOrEqualToZeroError


class TestFormEDot3DistanceCentroidAlpha1:
    """Validation for formula E.3 from EN 1995-1-1:2023."""

    @pytest.mark.parametrize(
        ("h_1", "h_2", "alpha_2", "expected_result"),
        [(10, 10, 0, 10), (10, 20, -10.06, 25.06), (20, 80, 14.686, 35.314), (30, 20, -10, 35.00)],
        ids=["a2=0", "a2<0", "a2>0", "a2<0b"],
    )
    def test_evaluation(self, h_1: float, h_2: float, alpha_2: float, expected_result: float) -> None:
        """Test the evaluation of the result."""
        form_e_3 = FormEDot3DistanceCentroidAlpha1(h_1=h_1, h_2=h_2, alpha_2=alpha_2)
        assert form_e_3 == pytest.approx(expected=expected_result, abs=1e-3)

    @pytest.mark.parametrize(
        ("h_1", "h_2", "alpha_2", "expectation"),
        [
            (10, 10, 0, does_not_raise()),
            (10, 20, -10.06, does_not_raise()),
            (0, 80, 14.686, pytest.raises(LessOrEqualToZeroError)),
            (-30, 20, -10, pytest.raises(LessOrEqualToZeroError)),
            (30, -20, -10, pytest.raises(LessOrEqualToZeroError)),
        ],
        ids=["passes1", "passes2", "h1=0", "h1<0", "h2<0"],
    )
    def test_raise_error_incorrect_args(self, h_1: float, h_2: float, alpha_2: float, expectation: AbstractContextManager) -> None:
        """Test the evaluation of incorrect arguments."""
        with expectation:
            assert FormEDot3DistanceCentroidAlpha1(h_1=h_1, h_2=h_2, alpha_2=alpha_2) is not None

    @pytest.mark.parametrize(
        ("h_1", "h_2", "alpha_2", "rep_short", "rep_long"),
        [
            (10, 10, 0, r"\alpha_1 = 10.00", r"\alpha_1 = \frac{h_1 + h_2}{2} - \alpha_2 = \frac{10.00 + 10.00}{2} - \left(0.00\right) = 10.00"),
            (
                10,
                20,
                -10.06,
                r"\alpha_1 = 25.06",
                r"\alpha_1 = \frac{h_1 + h_2}{2} - \alpha_2 = \frac{10.00 + 20.00}{2} - \left(-10.06\right) = 25.06",
            ),
        ],
        ids=["latex_a2_pos", "latex_a2_neg"],
    )
    def test_latex(self, h_1: float, h_2: float, alpha_2: float, rep_short: str, rep_long: str) -> None:
        """Test the latex representation of the formula."""
        form_e_3_latex = FormEDot3DistanceCentroidAlpha1(h_1=h_1, h_2=h_2, alpha_2=alpha_2).latex()
        assert form_e_3_latex.complete == rep_long
        assert form_e_3_latex.short == rep_short

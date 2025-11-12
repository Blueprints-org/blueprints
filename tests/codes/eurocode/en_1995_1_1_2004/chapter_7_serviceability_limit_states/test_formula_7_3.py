"""Testing formula 7.3 from EN 1995-1-1:2004."""

from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from blueprints.codes.eurocode.en_1995_1_1_2004.chapter_7_serviceability_limit_states.formula_7_3 import Form7Dot3RatioDeflectionPointLoadUC
from blueprints.validations import LessOrEqualToZeroError


class TestForm7Dot3RatioDeflectionPointLoadUCt:
    """Validation for formula 7.3 from EN 1995-1-1:2004."""

    @pytest.mark.parametrize(
        ("w", "f", "alpha", "expected_result"),
        [
            (1, 1, 1, 1),
            (0.002, 1, 0.2, 0.01),
            (0.8, 1, 0.4, 2),
        ],
        ids=["UC=1", "UC<1", "UC>1"],
    )
    def test_evaluation(self, w: float, f: float, alpha: float, expected_result: float) -> None:
        """Test the evaluation of the result."""
        form_7_3 = Form7Dot3RatioDeflectionPointLoadUC(w=w, f=f, alpha=alpha)
        assert form_7_3 == pytest.approx(expected=expected_result, abs=1e-4)

    @pytest.mark.parametrize(
        ("w", "f", "alpha", "expectation"),
        [
            (1, 1, 1, does_not_raise()),
            (-1, 1, 2, pytest.raises(LessOrEqualToZeroError)),
            (1, 0, 1, pytest.raises(LessOrEqualToZeroError)),
            (1, 0, -2, pytest.raises(LessOrEqualToZeroError)),
        ],
        ids=[
            "passes",
            "w<0",
            "F=0",
            "alpha<0",
        ],
    )
    def test_raise_error_incorrect_args(self, w: float, f: float, alpha: float, expectation: AbstractContextManager) -> None:
        """Test if errors are raised."""
        with expectation:
            assert Form7Dot3RatioDeflectionPointLoadUC(w=w, f=f, alpha=alpha) is not None

    @pytest.mark.parametrize(
        ("w", "f", "alpha", "rep_short", "rep_long"),
        [
            (
                0.0020,  # DIMENSIONLESS
                1,  # HZ
                0.0200,  # DIMENSIONLESS
                r"UC = 0.100",
                r"UC = \frac{w/F}{\alpha} = \frac{0.002/1.000}{0.020} = 0.100",
            ),
            (
                1,  # DIMENSIONLESS
                1,  # HZ
                1,  # DIMENSIONLESS
                r"UC = 1.000",
                r"UC = \frac{w/F}{\alpha} = \frac{1.000/1.000}{1.000} = 1.000",
            ),
        ],
        ids=["decimal result", "integer result"],
    )
    def test_latex(self, w: float, f: float, alpha: float, rep_short: str, rep_long: str) -> None:
        """Test the latex representation of the formula."""
        form_7_3_latex = Form7Dot3RatioDeflectionPointLoadUC(w=w, f=f, alpha=alpha).latex()
        assert form_7_3_latex.complete == rep_long
        assert form_7_3_latex.short == rep_short

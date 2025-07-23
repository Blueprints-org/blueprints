"""Testing formula 7.4 from EN 1995-1-1:2004."""

from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from blueprints.codes.eurocode.en_1995_1_1_2004.chapter_7_serviceability_limit_states.formula_7_4 import Form7Dot4VelocityResponseLimit
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm7Dot4VelocityResponseLimit:
    """Validation for formula 7.4 from EN 1995-1-1:2004."""

    @pytest.mark.parametrize(
        ("b", "f_1", "ksi", "expected_result"),
        [
            (120, 5, 0.02, 0.0134),
            (50, 2, 1, 50.000),
            (150, 3, 1.2, 454817.612),
            (120, 1, 0, 0.0083),
        ],
        ids=["b=120", "ksi = 1", "ksi > 1", "ksi = 0"],
    )
    def test_evaluation(self, b: float, f_1: float, ksi: float, expected_result: float) -> None:
        """Test the evaluation of the result."""
        form_7_4 = Form7Dot4VelocityResponseLimit(b=b, f_1=f_1, ksi=ksi)
        assert form_7_4 == pytest.approx(expected=expected_result, abs=1e-4)

    @pytest.mark.parametrize(
        ("b", "f_1", "ksi", "expectation"),
        [
            (120, 5, 0.02, does_not_raise()),
            (50, 2, -1, pytest.raises(NegativeValueError)),
            (50, 0, 1, pytest.raises(LessOrEqualToZeroError)),
            (
                40,
                8,
                1.2,
                pytest.raises(ValueError),
            ),
        ],
        ids=[
            "passes",
            "ksi < 0",
            "f_1 = 0",
            "b_outside_range",
        ],
    )
    def test_raise_error_incorrect_args(self, b: float, f_1: float, ksi: float, expectation: AbstractContextManager) -> None:
        """Test if errors are raised."""
        with expectation:
            assert Form7Dot4VelocityResponseLimit(b=b, f_1=f_1, ksi=ksi) is not None

    @pytest.mark.parametrize(
        ("b", "f_1", "ksi", "rep_short", "rep_long"),
        [
            (
                50,  # DIMENSIONLESS
                2,  # HZ
                1,  # DIMENSIONLESS
                r"v_{lim} = 50.000",
                r"v_{lim} = b^{(f_1 \cdot \xi - 1)} = 50.000^{(2.000 \cdot 1.000 - 1)} = 50.000",
            ),
            (
                120,  # DIMENSIONLESS
                5,  # HZ
                0.02,  # DIMENSIONLESS
                r"v_{lim} = 0.013",
                r"v_{lim} = b^{(f_1 \cdot \xi - 1)} = 120.000^{(5.000 \cdot 0.020 - 1)} = 0.013",
            ),
        ],
        ids=["decimal result", "integer result"],
    )
    def test_latex(self, b: float, f_1: float, ksi: float, rep_short: str, rep_long: str) -> None:
        """Test the latex representation of the formula."""
        form_7_4_latex = Form7Dot4VelocityResponseLimit(f_1=f_1, b=b, ksi=ksi).latex()
        assert form_7_4_latex.complete == rep_long
        assert form_7_4_latex.short == rep_short

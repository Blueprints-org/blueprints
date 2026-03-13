"""Testing formula 7.7 from EN 1995-1-1:2004."""

from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from blueprints.codes.eurocode.en_1995_1_1_2004.chapter_7_serviceability_limit_states.formula_7_7 import Form7Dot7NumberOfFOVibrations
from blueprints.validations import LessOrEqualToZeroError


class TestForm7Dot7NumberOfFOVibrations:
    """Validation for formula 7.7 from EN 1995-1-1:2004."""

    @pytest.mark.parametrize(
        ("f_1", "b", "length", "ei_l", "ei_b", "expected_result"),
        [
            (8.96, 1.0, 5.3, 5.81e12, 3.89e11, 0.774),
            (28.2843, 1.0, 1.0, 1.0001, 1, 1.00),
        ],
        ids=["decimal result", "result to 1"],
    )
    def test_evaluation(self, f_1: float, b: float, length: float, ei_l: float, ei_b: float, expected_result: float) -> None:
        """Test the evaluation of the result."""
        form_7_7 = Form7Dot7NumberOfFOVibrations(f_1=f_1, b=b, length=length, ei_l=ei_l, ei_b=ei_b)
        assert form_7_7 == pytest.approx(expected=expected_result, rel=1e-3)

    @pytest.mark.parametrize(
        ("f_1", "b", "length", "ei_l", "ei_b", "expectation"),
        [
            (8.96, 1.0, 5.3, 5.81e12, 3.89e11, does_not_raise()),
            (20, 1.0, 1.0, 5.82e12, 5.81e12, does_not_raise()),
            (41, 1, 1, 2, 1, pytest.raises(ValueError, match=r"exceeds the allowed limit of 40.")),
            (20, 1, 1, 1, 1, pytest.raises(ValueError, match="must be bigger than")),
            (20, 1, 1, 1, 2, pytest.raises(ValueError, match="must be bigger than")),
            (20, 1, 1, 2, 0, pytest.raises(LessOrEqualToZeroError)),
            (20, 0, 1, 2, 2, pytest.raises(LessOrEqualToZeroError)),
            (20, 1, -20, 2, 3, pytest.raises(LessOrEqualToZeroError)),
            (20, 1, 1, -2, 3, pytest.raises(LessOrEqualToZeroError)),
        ],
        ids=["passes decimal result", "passes integer", "f_1 > 40", "ei_b = ei_l", "ei_b > ei_l", "ei_b = 0", "b = 0", "length < 0", "ei_l < 0"],
    )
    def test_raise_error_incorrect_args(
        self, f_1: float, b: float, length: float, ei_l: float, ei_b: float, expectation: AbstractContextManager
    ) -> None:
        """Test if errors are raised."""
        with expectation:
            assert Form7Dot7NumberOfFOVibrations(f_1=f_1, b=b, length=length, ei_l=ei_l, ei_b=ei_b) is not None

    @pytest.mark.parametrize(
        ("f_1", "b", "length", "ei_l", "ei_b", "rep_short", "rep_long"),
        [
            (
                8.96,  # HZ
                1.0,  # M
                5.3,  # M
                5.81e7,  # NM2_M
                3.89e6,  # NM2_M
                r"n_{40} = 0.77",
                r"n_{40} = \left\{\left ( \left (\frac{40}{f_1} \right )^2 -1 \right)\left ( \frac{b}{l } \right )^4 \frac{(EI)_l}{(EI)_b}\right\}^{0.25} = \left\{\left ( \left (\frac{40}{8.96} \right )^2 -1 \right)\left ( \frac{1.00}{5.30} \right )^4 \frac{58100000.00}{3890000.00}\right\}^{0.25} = 0.77",  # noqa: E501
            ),
            (
                28.2843,  # HZ
                1,  # M
                1,  # M
                1.001,  # NM2_M
                1,  # NM2_M
                r"n_{40} = 1.00",
                r"n_{40} = \left\{\left ( \left (\frac{40}{f_1} \right )^2 -1 \right)\left ( \frac{b}{l } \right )^4 \frac{(EI)_l}{(EI)_b}\right\}^{0.25} = \left\{\left ( \left (\frac{40}{28.28} \right )^2 -1 \right)\left ( \frac{1.00}{1.00} \right )^4 \frac{1.00}{1.00}\right\}^{0.25} = 1.00",  # noqa: E501
            ),
        ],
        ids=["test with decimal output", "test with integer output"],
    )
    def test_latex(self, f_1: float, b: float, length: float, ei_l: float, ei_b: float, rep_short: str, rep_long: str) -> None:
        """Test the latex representation of the formula."""
        form_7_7_latex = Form7Dot7NumberOfFOVibrations(f_1=f_1, b=b, length=length, ei_l=ei_l, ei_b=ei_b).latex()
        assert form_7_7_latex.complete == rep_long
        assert form_7_7_latex.short == rep_short

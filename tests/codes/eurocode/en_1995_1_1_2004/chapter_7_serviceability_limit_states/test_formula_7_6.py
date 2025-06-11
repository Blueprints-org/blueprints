"""Testing formula 7.6 from EN 1995-1-1:2004."""

from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from blueprints.codes.eurocode.en_1995_1_1_2004.chapter_7_serviceability_limit_states.formula_7_6 import Form7Dot6VelocityResponse
from blueprints.validations import LessOrEqualToZeroError


class TestForm7Dot6VelocityResponse:
    """Validation for formula 7.6 from EN 1995-1-1:2004."""

    @pytest.mark.parametrize(
        ("n_40", "m", "length", "b", "expected_result"),
        [(0.77, 226, 5.30, 1.00, 0.002466), (1, 1, 1, 1, 0.0199)],
        ids=["test 1", "test 2"],
    )
    def test_evaluation(self, n_40: float, m: float, length: float, b: float, expected_result: float) -> None:
        """Test the evaluation of the result."""
        form_7_6 = Form7Dot6VelocityResponse(n_40=n_40, m=m, length=length, b=b)
        assert form_7_6 == pytest.approx(expected=expected_result, rel=1e-3)

    @pytest.mark.parametrize(
        ("n_40", "m", "length", "b", "expectation"),
        [
            (1, 1, 1, 1, does_not_raise()),
            (0.01, 0.2, 10, 2, does_not_raise()),
            (0, 1, 1, 1, pytest.raises(LessOrEqualToZeroError)),
            (1, 0, 1, 1, pytest.raises(LessOrEqualToZeroError)),
            (1, 1, 0, 1, pytest.raises(LessOrEqualToZeroError)),
            (1, 1, 1, 0, pytest.raises(LessOrEqualToZeroError)),
            (-1, 1, 1, 1, pytest.raises(LessOrEqualToZeroError)),
            (1, -1, 1, 1, pytest.raises(LessOrEqualToZeroError)),
            (1, 1, -1, 1, pytest.raises(LessOrEqualToZeroError)),
            (1, 1, 1, -1, pytest.raises(LessOrEqualToZeroError)),
        ],
        ids=[
            "passes test 1",
            "passes test 2",
            "zero_n_40",
            "zero_m",
            "zero_length",
            "zero_b",
            "negative_n_40",
            "negative_m",
            "negative_length",
            "negative_b",
        ],
    )
    def test_raise_error_incorrect_args(self, n_40: float, m: float, length: float, b: float, expectation: AbstractContextManager) -> None:
        """Test the evaluation of the result."""
        with expectation:
            assert Form7Dot6VelocityResponse(n_40=n_40, length=length, m=m, b=b) is not None

    @pytest.mark.parametrize(
        ("n_40", "m", "length", "b", "rep_short", "rep_long"),
        [
            (
                1,  # HZ
                1,  # KG_M2
                1,  # M
                1,  # M
                r"v = 0.020",
                r"v = \frac{4 \cdot (0.4 + 0.6 \cdot n_{40})}{m \cdot b \cdot l + 200} = \frac{4 \cdot (0.4 + 0.6 \cdot 1.00)}{1.00 \cdot 1.00 \cdot 1.00 + 200} = 0.020",  # noqa: E501
            ),
            (
                0.77,  # HZ
                226,  # KG_M2
                5.3,  # M
                1,  # M
                r"v = 0.002",
                r"v = \frac{4 \cdot (0.4 + 0.6 \cdot n_{40})}{m \cdot b \cdot l + 200} = \frac{4 \cdot (0.4 + 0.6 \cdot 0.77)}{226.00 \cdot 1.00 \cdot 5.30 + 200} = 0.002",  # noqa: E501
            ),
        ],
        ids=["test with integer input", "test with decimal inputs"],
    )
    def test_latex(self, n_40: float, m: float, length: float, b: float, rep_short: str, rep_long: str) -> None:
        """Test the latex representation of the formula."""
        # act
        form_7_6_latex = Form7Dot6VelocityResponse(n_40=n_40, b=b, m=m, length=length).latex()

        # assert
        assert form_7_6_latex.complete == rep_long
        assert form_7_6_latex.short == rep_short

"""Testing formula 7.5 from EN 1995-1-1:2004."""

from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from blueprints.codes.eurocode.en_1995_1_1_2004.chapter_7_serviceability_limit_states.formula_7_5 import Form7Dot5NaturalFrequency
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm7Dot5NaturalFrequency:
    """Validation for formula 7.5 from EN 1995-1-1:2004."""

    @pytest.mark.parametrize(
        ("length", "ei_l", "m", "expected_result"),
        [(5.3, 5.81e6, 226, 8.9661), (1.25, 0, 1, 0.00)],
        ids=[
            "result 1",
            "result 2",
        ],
    )
    def test_evaluation(self, length: float, ei_l: float, m: float, expected_result: float) -> None:
        """Test the evaluation of the result."""
        form_7_5 = Form7Dot5NaturalFrequency(length=length, ei_l=ei_l, m=m)
        assert form_7_5 == pytest.approx(expected=expected_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("length", "ei_l", "m", "expectation"),
        [
            (5.3, 5.81e6, 226, does_not_raise()),
            (1.25, 0, 1, does_not_raise()),
            (5.3, 5.8e06, 0, pytest.raises(LessOrEqualToZeroError)),
            (0, 5.8e06, 20, pytest.raises(LessOrEqualToZeroError)),
            (1, -5.8e06, 20, pytest.raises(NegativeValueError)),
        ],
        ids=["decimal f1", "integer f1", "zero_m", "zero_l", "negative_ei"],
    )
    def test_raise_error_incorrect_args(self, length: float, ei_l: float, m: float, expectation: AbstractContextManager) -> None:
        """Test the evaluation of the result."""
        with expectation:
            assert Form7Dot5NaturalFrequency(length=length, ei_l=ei_l, m=m) is not None

    @pytest.mark.parametrize(
        ("length", "ei_l", "m", "rep_short", "rep_long"),
        [
            (
                5.30,  # M
                5.81e6,  # NM2_M
                226,  # KG_M2
                r"f_{1} = 8.97",
                r"f_{1} = \frac{\pi}{2 \cdot l^{2}} \cdot \sqrt{\frac{(EI)_{l}}{m}} = \frac{\pi}{2 \cdot 5.30^{2}} \cdot \sqrt{\frac{5810000.00}{226.00}} = 8.97",  # noqa: E501
            ),
            (
                1.25,  # M
                0,  # NM2_M
                1,  # KG_M2
                r"f_{1} = 0.00",
                r"f_{1} = \frac{\pi}{2 \cdot l^{2}} \cdot \sqrt{\frac{(EI)_{l}}{m}} = \frac{\pi}{2 \cdot 1.25^{2}} \cdot \sqrt{\frac{0.00}{1.00}} = 0.00",  # noqa: E501
            ),
        ],
        ids=["test with decimal outcome", "test with outcome=0"],
    )
    def test_latex(self, length: float, ei_l: float, m: float, rep_short: str, rep_long: str) -> None:
        """Text the latex representation of the formula."""
        # Objects to test

        # arrange
        # act
        form_7_5_latex = Form7Dot5NaturalFrequency(length=length, ei_l=ei_l, m=m).latex()

        # assert
        assert form_7_5_latex.complete == rep_long
        assert form_7_5_latex.short == rep_short

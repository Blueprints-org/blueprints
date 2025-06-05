"""Testing formula 6.4 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_4 import Form6Dot4ShearResistance
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot4ShearResistance:
    """Validation for formula 6.4 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        i = 1000.0
        b_w = 300.0
        s = 500.0
        f_ctd = 2.5
        alpha_l = 1.0
        sigma_cp = 1.5

        # Object to test
        formula = Form6Dot4ShearResistance(i=i, b_w=b_w, s=s, f_ctd=f_ctd, alpha_l=alpha_l, sigma_cp=sigma_cp)

        # Expected result, manually calculated
        manually_calculated_result = 1897.3665961010277

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("i", "b_w", "s", "f_ctd", "alpha_l", "sigma_cp"),
        [
            (-1000.0, 300.0, 500.0, 2.5, 1.0, 1.5),  # i is negative
            (1000.0, -300.0, 500.0, 2.5, 1.0, 1.5),  # b_w is negative
            (1000.0, 300.0, -500.0, 2.5, 1.0, 1.5),  # s is negative
            (1000.0, 300.0, 500.0, -2.5, 1.0, 1.5),  # f_ctd is negative
            (1000.0, 300.0, 500.0, 2.5, -1.0, 1.5),  # alpha_l is negative
            (1000.0, 300.0, 500.0, 2.5, 1.0, -1.5),  # sigma_cp is negative
            (1000.0, 300.0, 0.0, 2.5, 1.0, 1.5),  # s is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, i: float, b_w: float, s: float, f_ctd: float, alpha_l: float, sigma_cp: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot4ShearResistance(i=i, b_w=b_w, s=s, f_ctd=f_ctd, alpha_l=alpha_l, sigma_cp=sigma_cp)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"V_{Rd,c} = \frac{I \cdot b_w}{S} \cdot \sqrt{(f_{ctd})^2 + \alpha_l \cdot \sigma_{cp} \cdot f_{ctd}} = "
                r"\frac{1000.000 \cdot 300.000}{500.000} \cdot \sqrt{(2.500)^2 + 1.000 \cdot 1.500 \cdot 2.500} = 1897.367 \ N",
            ),
            ("short", r"V_{Rd,c} = 1897.367 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        i = 1000.0
        b_w = 300.0
        s = 500.0
        f_ctd = 2.5
        alpha_l = 1.0
        sigma_cp = 1.5

        # Object to test
        latex = Form6Dot4ShearResistance(i=i, b_w=b_w, s=s, f_ctd=f_ctd, alpha_l=alpha_l, sigma_cp=sigma_cp).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

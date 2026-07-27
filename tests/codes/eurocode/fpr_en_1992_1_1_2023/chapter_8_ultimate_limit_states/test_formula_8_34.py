"""Testing formula 8.34 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_34 import Form8Dot34FactorK1
from blueprints.validations import LessOrEqualToZeroError


class TestForm8Dot34FactorK1:
    """Validation for formula 8.34 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result when the expression governs."""
        # Example values
        a_cs_0 = 1333.333333
        e_p = 100.0
        d = 500.0
        a_c = 180000.0
        b_w = 300.0
        z = 450.0

        # Object to test
        formula = Form8Dot34FactorK1(a_cs_0=a_cs_0, e_p=e_p, d=d, a_c=a_c, b_w=b_w, z=z)

        # Expected result, manually calculated
        manually_calculated_result = 0.133333  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_when_the_upper_bound_governs(self) -> None:
        """Tests the evaluation of the result when the printed upper bound governs."""
        # Example values, with a short shear span so the expression exceeds the bound
        formula = Form8Dot34FactorK1(a_cs_0=500.0, e_p=100.0, d=500.0, a_c=180000.0, b_w=300.0, z=450.0)

        # Expected result, manually calculated: 0.18 * 180000 / (300 * 450)
        manually_calculated_result = 0.24  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_with_negative_eccentricity(self) -> None:
        """Tests that an eccentricity on the compressive side, which the standard defines as negative, is accepted."""
        formula = Form8Dot34FactorK1(a_cs_0=1333.333333, e_p=-100.0, d=500.0, a_c=180000.0, b_w=300.0, z=450.0)

        # Expected result, manually calculated
        manually_calculated_result = 0.033333  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_can_return_a_negative_factor(self) -> None:
        """Tests that no lower bound is imposed, since the standard prints none.

        For an eccentricity more negative than minus one third of the effective depth, the bracket turns
        negative and so does the factor.
        """
        formula = Form8Dot34FactorK1(a_cs_0=1333.333333, e_p=-300.0, d=500.0, a_c=180000.0, b_w=300.0, z=450.0)

        # Expected result, manually calculated: (0.5 / 1333.333333) * (-300 + 500 / 3) * (180000 / 135000)
        manually_calculated_result = -0.066667  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_cs_0", "e_p", "d", "a_c", "b_w", "z"),
        [
            (1333.333333, 100.0, -500.0, 180000.0, 300.0, 450.0),  # d is negative
            (1333.333333, 100.0, 0.0, 180000.0, 300.0, 450.0),  # d is zero, which is not a cross-section
            (1333.333333, 100.0, 500.0, -180000.0, 300.0, 450.0),  # a_c is negative
            (1333.333333, 100.0, 500.0, 0.0, 300.0, 450.0),  # a_c is zero
            (-1333.333333, 100.0, 500.0, 180000.0, 300.0, 450.0),  # a_cs_0 is negative
            (0.0, 100.0, 500.0, 180000.0, 300.0, 450.0),  # a_cs_0 is zero
            (1333.333333, 100.0, 500.0, 180000.0, -300.0, 450.0),  # b_w is negative
            (1333.333333, 100.0, 500.0, 180000.0, 0.0, 450.0),  # b_w is zero
            (1333.333333, 100.0, 500.0, 180000.0, 300.0, -450.0),  # z is negative
            (1333.333333, 100.0, 500.0, 180000.0, 300.0, 0.0),  # z is zero
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero(self, a_cs_0: float, e_p: float, d: float, a_c: float, b_w: float, z: float) -> None:
        """Test if error is raised for parameters that are not allowed to be zero or less."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot34FactorK1(a_cs_0=a_cs_0, e_p=e_p, d=d, a_c=a_c, b_w=b_w, z=z)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"k_1 = \min\left(\frac{0.5}{a_{cs,0}} \cdot \left(e_p + \frac{d}{3}\right) \cdot "
                r"\frac{A_c}{b_w \cdot z}, 0.18 \cdot \frac{A_c}{b_w \cdot z}\right) = "
                r"\min\left(\frac{0.5}{1333.333} \cdot \left(100.000 + \frac{500.000}{3}\right) \cdot "
                r"\frac{180000.000}{300.000 \cdot 450.000}, 0.18 \cdot \frac{180000.000}{300.000 \cdot 450.000}\right) = 0.133 \ -",
            ),
            (
                "complete_with_units",
                r"k_1 = \min\left(\frac{0.5}{a_{cs,0}} \cdot \left(e_p + \frac{d}{3}\right) \cdot "
                r"\frac{A_c}{b_w \cdot z}, 0.18 \cdot \frac{A_c}{b_w \cdot z}\right) = "
                r"\min\left(\frac{0.5}{1333.333 \ mm} \cdot \left(100.000 \ mm + \frac{500.000 \ mm}{3}\right) \cdot "
                r"\frac{180000.000 \ mm^2}{300.000 \ mm \cdot 450.000 \ mm}, 0.18 \cdot "
                r"\frac{180000.000 \ mm^2}{300.000 \ mm \cdot 450.000 \ mm}\right) = 0.133 \ -",
            ),
            ("short", r"k_1 = 0.133 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_cs_0 = 1333.333333
        e_p = 100.0
        d = 500.0
        a_c = 180000.0
        b_w = 300.0
        z = 450.0

        # Object to test
        latex = Form8Dot34FactorK1(a_cs_0=a_cs_0, e_p=e_p, d=d, a_c=a_c, b_w=b_w, z=z).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

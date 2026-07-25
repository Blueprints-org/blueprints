"""Testing formula 8.31 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_31 import Form8Dot31AxialForceCoefficient
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot31AxialForceCoefficient:
    """Validation for formula 8.31 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("n_ed", "expected"),
        [
            (-200000.0, 0.833333),  # axial force lowering the coefficient
            (0.0, 1.0),  # no axial force
            (200000.0, 1.166667),  # axial force raising the coefficient
        ],
    )
    def test_evaluation(self, n_ed: float, expected: float) -> None:
        """Tests the evaluation of the result for both signs of the axial force."""
        # Example values
        v_ed = 150000.0
        d = 500.0
        a_cs = 1333.333333

        # Object to test
        formula = Form8Dot31AxialForceCoefficient(n_ed=n_ed, v_ed=v_ed, d=d, a_cs=a_cs)

        assert formula == pytest.approx(expected=expected, rel=1e-4)

    def test_evaluation_when_the_lower_bound_governs(self) -> None:
        """Tests the evaluation of the result when the printed lower bound of 0.1 governs."""
        # Example values, with an axial force large enough to drive the expression below 0.1
        formula = Form8Dot31AxialForceCoefficient(n_ed=-2000000.0, v_ed=150000.0, d=500.0, a_cs=1333.333333)

        # Expected result, manually calculated: the expression yields -0.666667, so the lower bound governs
        manually_calculated_result = 0.1  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_is_insensitive_to_the_sign_of_the_shear_force(self) -> None:
        """Tests that the absolute value bars printed around the shear force make its sign irrelevant."""
        positive = Form8Dot31AxialForceCoefficient(n_ed=-200000.0, v_ed=150000.0, d=500.0, a_cs=1333.333333)
        negative = Form8Dot31AxialForceCoefficient(n_ed=-200000.0, v_ed=-150000.0, d=500.0, a_cs=1333.333333)

        assert float(positive) == pytest.approx(expected=float(negative), rel=1e-9)

    @pytest.mark.parametrize(
        ("n_ed", "v_ed", "d", "a_cs"),
        [
            (-200000.0, 0.0, 500.0, 1333.333333),  # v_ed is zero
            (-200000.0, 150000.0, -500.0, 1333.333333),  # d is negative
            (-200000.0, 150000.0, 500.0, -1333.333333),  # a_cs is negative
            (-200000.0, 150000.0, 500.0, 0.0),  # a_cs is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, n_ed: float, v_ed: float, d: float, a_cs: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot31AxialForceCoefficient(n_ed=n_ed, v_ed=v_ed, d=d, a_cs=a_cs)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"k_{vp} = \max\left(1 + \frac{N_{Ed}}{\left|V_{Ed}\right|} \cdot \frac{d}{3 \cdot a_{cs}}, 0.1\right) = "
                r"\max\left(1 + \frac{-200000.000}{\left|150000.000\right|} \cdot \frac{500.000}{3 \cdot 1333.333}, 0.1\right) = 0.833 \ -",
            ),
            (
                "complete_with_units",
                r"k_{vp} = \max\left(1 + \frac{N_{Ed}}{\left|V_{Ed}\right|} \cdot \frac{d}{3 \cdot a_{cs}}, 0.1\right) = "
                r"\max\left(1 + \frac{-200000.000 \ N}{\left|150000.000 \ N\right|} \cdot "
                r"\frac{500.000 \ mm}{3 \cdot 1333.333 \ mm}, 0.1\right) = 0.833 \ -",
            ),
            ("short", r"k_{vp} = 0.833 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n_ed = -200000.0
        v_ed = 150000.0
        d = 500.0
        a_cs = 1333.333333

        # Object to test
        latex = Form8Dot31AxialForceCoefficient(n_ed=n_ed, v_ed=v_ed, d=d, a_cs=a_cs).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

"""Testing formula 8.21 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_21 import Form8Dot21DesignShearForcePerUnitWidth


class TestForm8Dot21DesignShearForcePerUnitWidth:
    """Validation for formula 8.21 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed_x = 100.0
        v_ed_y = 40.0

        # Object to test
        formula = Form8Dot21DesignShearForcePerUnitWidth(v_ed_x=v_ed_x, v_ed_y=v_ed_y)

        # Expected result, manually calculated
        manually_calculated_result = 107.703296  # N/mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_with_shear_in_one_direction_only(self) -> None:
        """Tests the evaluation when the shear force acts in one direction only."""
        # Object to test
        formula = Form8Dot21DesignShearForcePerUnitWidth(v_ed_x=0.0, v_ed_y=250.0)

        # Expected result, manually calculated
        manually_calculated_result = 250.0  # N/mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("v_ed_x", "v_ed_y"),
        [
            (100.0, 40.0),  # both positive
            (-100.0, 40.0),  # v_ed_x is negative
            (100.0, -40.0),  # v_ed_y is negative
            (-100.0, -40.0),  # both negative
        ],
    )
    def test_sign_of_the_components_does_not_reach_the_result(self, v_ed_x: float, v_ed_y: float) -> None:
        """The components are squared, so all four sign combinations give the same magnitude.

        They are components of a shear force vector and the standard places no restriction on their sign,
        so a negative one is ordinary input rather than an error.
        """
        formula = Form8Dot21DesignShearForcePerUnitWidth(v_ed_x=v_ed_x, v_ed_y=v_ed_y)

        assert formula == pytest.approx(expected=107.703296, rel=1e-4)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"v_{Ed} = \sqrt{\left(v_{Ed,x}\right)^2 + \left(v_{Ed,y}\right)^2} = "
                r"\sqrt{\left(100.000\right)^2 + \left(40.000\right)^2} = 107.703 \ N/mm",
            ),
            (
                "complete_with_units",
                r"v_{Ed} = \sqrt{\left(v_{Ed,x}\right)^2 + \left(v_{Ed,y}\right)^2} = "
                r"\sqrt{\left(100.000 \ N/mm\right)^2 + \left(40.000 \ N/mm\right)^2} = 107.703 \ N/mm",
            ),
            ("short", r"v_{Ed} = 107.703 \ N/mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_ed_x = 100.0
        v_ed_y = 40.0

        # Object to test
        latex = Form8Dot21DesignShearForcePerUnitWidth(v_ed_x=v_ed_x, v_ed_y=v_ed_y).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

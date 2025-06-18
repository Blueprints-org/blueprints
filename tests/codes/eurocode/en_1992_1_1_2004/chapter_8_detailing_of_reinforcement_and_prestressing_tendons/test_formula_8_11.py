"""Testing formula 8.11 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_3 import (
    Form8Dot3RequiredAnchorageLength,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_11 import (
    Form8Dot11MinimumDesignLapLength,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot11MinimumDesignLapLength:
    """Validation for formula 8.11 from EN 1992-1-1:2004."""

    def test_evaluation_first_term_decisive(self) -> None:
        """Test the evaluation of the result."""
        # example values
        alpha_6 = 1  # [-]
        l_b_rqd = 1200  # mm
        diameter = 16  # mm
        form_8_11 = Form8Dot11MinimumDesignLapLength(
            alpha_6=alpha_6,
            l_b_rqd=l_b_rqd,
            diameter=diameter,
        )

        # manually calculated result
        manually_calculated_result = 360  # mm

        assert form_8_11 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_second_term_decisive(self) -> None:
        """Test the evaluation of the result."""
        # example values
        alpha_6 = 1  # [-]
        l_b_rqd = 450  # mm
        diameter = 32  # mm
        form_8_11 = Form8Dot11MinimumDesignLapLength(
            alpha_6=alpha_6,
            l_b_rqd=l_b_rqd,
            diameter=diameter,
        )

        # manually calculated result
        manually_calculated_result = 480  # mm

        assert form_8_11 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_third_term_decisive(self) -> None:
        """Test the evaluation of the result."""
        # example values
        alpha_6 = 1  # [-]
        l_b_rqd = 450  # mm
        diameter = 8  # mm
        form_8_11 = Form8Dot11MinimumDesignLapLength(
            alpha_6=alpha_6,
            l_b_rqd=l_b_rqd,
            diameter=diameter,
        )

        # manually calculated result
        manually_calculated_result = 200  # mm

        assert form_8_11 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_if_alpha_6_is_negative(self) -> None:
        """Test that a NegativeValueError is raised if alpha_6 is negative."""
        # example values
        alpha_6 = -1  # [-]
        l_b_rqd = 450  # mm
        diameter = 8  # mm

        with pytest.raises(NegativeValueError):
            Form8Dot11MinimumDesignLapLength(
                alpha_6=alpha_6,
                l_b_rqd=l_b_rqd,
                diameter=diameter,
            )

    def test_raise_error_if_l_b_rqd_is_negative(self) -> None:
        """Test that a NegativeValueError is raised if l_b_rqd is negative."""
        # example values
        alpha_6 = 1  # [-]
        l_b_rqd = -450  # mm
        diameter = 8  # mm

        with pytest.raises(NegativeValueError):
            Form8Dot11MinimumDesignLapLength(
                alpha_6=alpha_6,
                l_b_rqd=l_b_rqd,
                diameter=diameter,
            )

    def test_raise_error_if_diameter_is_negative(self) -> None:
        """Test that a NegativeValueError is raised if diameter is negative."""
        # example values
        alpha_6 = 1  # [-]
        l_b_rqd = 450  # mm
        diameter = -8  # mm

        with pytest.raises(NegativeValueError):
            Form8Dot11MinimumDesignLapLength(
                alpha_6=alpha_6,
                l_b_rqd=l_b_rqd,
                diameter=diameter,
            )

    def test_integration_with_form_8_3(self) -> None:
        """Test the integration with formula 8.3."""
        # example values
        diameter = 8  # mm
        alpha_6 = 1  # [-]
        sigma_sd = 500  # MPa
        f_bd = 2.5  # MPa
        l_b_rqd = Form8Dot3RequiredAnchorageLength(
            diameter=diameter,
            sigma_sd=sigma_sd,
            f_bd=f_bd,
        )

        form_8_11 = Form8Dot11MinimumDesignLapLength(
            alpha_6=alpha_6,
            l_b_rqd=l_b_rqd,
            diameter=diameter,
        )

        # manually calculated result
        manually_calculated_result = 200  # mm

        assert form_8_11 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            (
                "complete",
                r"l_{Ø,min} = \max \left\{0.3 \cdot \alpha_6 \cdot l_{b,rqd}; 15 \cdot Ø; 200 \ \text{mm}\right\} = \max \left\{0.3 \cdot 1.000 "
                r"\cdot 450.000; 15 \cdot 8; 200\right\} = 200.000",
            ),
            ("short", r"l_{Ø,min} = 200.000"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the LaTeX representation."""
        # example values
        alpha_6 = 1
        l_b_rqd = 450
        diameter = 8

        latex = Form8Dot11MinimumDesignLapLength(
            alpha_6=alpha_6,
            l_b_rqd=l_b_rqd,
            diameter=diameter,
        ).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."

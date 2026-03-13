"""Testing formula 8.10 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_3 import (
    Form8Dot3RequiredAnchorageLength,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_10 import (
    Form8Dot10DesignLapLength,
    SubForm8Dot10Alpha6,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_11 import (
    Form8Dot11MinimumDesignLapLength,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot10DesignLapLength:
    """Validation for formula 8.10 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        alpha_1 = 1  # [-]
        alpha_2 = 1  # [-]
        alpha_3 = 1  # [-]
        alpha_5 = 1  # [-]
        alpha_6 = 1  # [-]
        l_b_rqd = 450  # mm
        l_0_min = 200  # mm
        form_8_10 = Form8Dot10DesignLapLength(
            alpha_1=alpha_1,
            alpha_2=alpha_2,
            alpha_3=alpha_3,
            alpha_5=alpha_5,
            alpha_6=alpha_6,
            l_b_rqd=l_b_rqd,
            l_0_min=l_0_min,
        )

        # manually calculated result
        manually_calculated_result = 450  # mm

        assert form_8_10 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_minimum(self) -> None:
        """Test the evaluation of the result if the minimum is reached."""
        # example values
        alpha_1 = 1  # [-]
        alpha_2 = 1  # [-]
        alpha_3 = 1  # [-]
        alpha_5 = 1  # [-]
        alpha_6 = 1  # [-]
        l_b_rqd = 450  # mm
        l_0_min = 500  # mm
        form_8_10 = Form8Dot10DesignLapLength(
            alpha_1=alpha_1,
            alpha_2=alpha_2,
            alpha_3=alpha_3,
            alpha_5=alpha_5,
            alpha_6=alpha_6,
            l_b_rqd=l_b_rqd,
            l_0_min=l_0_min,
        )

        # manually calculated result
        manually_calculated_result = 500  # mm

        assert form_8_10 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_if_alpha_1_is_negative(self) -> None:
        """Test that a NegativeValueError is raised if alpha_1 is negative."""
        # example values
        alpha_1 = -1  # [-]
        alpha_2 = 1  # [-]
        alpha_3 = 1  # [-]
        alpha_5 = 1  # [-]
        alpha_6 = 1  # [-]
        l_b_rqd = 450  # mm
        l_0_min = 200  # mm

        with pytest.raises(NegativeValueError):
            Form8Dot10DesignLapLength(
                alpha_1=alpha_1,
                alpha_2=alpha_2,
                alpha_3=alpha_3,
                alpha_5=alpha_5,
                alpha_6=alpha_6,
                l_b_rqd=l_b_rqd,
                l_0_min=l_0_min,
            )

    def test_raise_error_if_alpha_2_is_negative(self) -> None:
        """Test that a NegativeValueError is raised if alpha_2 is negative."""
        # example values
        alpha_1 = 1  # [-]
        alpha_2 = -1  # [-]
        alpha_3 = 1  # [-]
        alpha_5 = 1  # [-]
        alpha_6 = 1  # [-]
        l_b_rqd = 450  # mm
        l_0_min = 200  # mm

        with pytest.raises(NegativeValueError):
            Form8Dot10DesignLapLength(
                alpha_1=alpha_1,
                alpha_2=alpha_2,
                alpha_3=alpha_3,
                alpha_5=alpha_5,
                alpha_6=alpha_6,
                l_b_rqd=l_b_rqd,
                l_0_min=l_0_min,
            )

    def test_raise_error_if_alpha_3_is_negative(self) -> None:
        """Test that a NegativeValueError is raised if alpha_3 is negative."""
        # example values
        alpha_1 = 1  # [-]
        alpha_2 = 1  # [-]
        alpha_3 = -1  # [-]
        alpha_5 = 1  # [-]
        alpha_6 = 1  # [-]
        l_b_rqd = 450  # mm
        l_0_min = 200  # mm

        with pytest.raises(NegativeValueError):
            Form8Dot10DesignLapLength(
                alpha_1=alpha_1,
                alpha_2=alpha_2,
                alpha_3=alpha_3,
                alpha_5=alpha_5,
                alpha_6=alpha_6,
                l_b_rqd=l_b_rqd,
                l_0_min=l_0_min,
            )

    def test_raise_error_if_alpha_5_is_negative(self) -> None:
        """Test that a NegativeValueError is raised if alpha_5 is negative."""
        alpha_1 = 1  # [-]
        alpha_2 = 1  # [-]
        alpha_3 = 1  # [-]
        alpha_5 = -1  # [-]
        alpha_6 = 1  # [-]
        l_b_rqd = 450  # mm
        l_0_min = 200  # mm

        with pytest.raises(NegativeValueError):
            Form8Dot10DesignLapLength(
                alpha_1=alpha_1,
                alpha_2=alpha_2,
                alpha_3=alpha_3,
                alpha_5=alpha_5,
                alpha_6=alpha_6,
                l_b_rqd=l_b_rqd,
                l_0_min=l_0_min,
            )

    def test_raise_error_if_alpha_6_is_negative(self) -> None:
        """Test that a NegativeValueError is raised if alpha_6 is negative."""
        # example values
        alpha_1 = 1  # [-]
        alpha_2 = 1  # [-]
        alpha_3 = 1  # [-]
        alpha_5 = 1  # [-]
        alpha_6 = -1  # [-]
        l_b_rqd = 450  # mm
        l_0_min = 200  # mm

        with pytest.raises(NegativeValueError):
            Form8Dot10DesignLapLength(
                alpha_1=alpha_1,
                alpha_2=alpha_2,
                alpha_3=alpha_3,
                alpha_5=alpha_5,
                alpha_6=alpha_6,
                l_b_rqd=l_b_rqd,
                l_0_min=l_0_min,
            )

    def test_raise_error_if_l_b_rqd_is_negative(self) -> None:
        """Test that a NegativeValueError is raised if l_b_rqd is negative."""
        # example values
        alpha_1 = 1  # [-]
        alpha_2 = 1  # [-]
        alpha_3 = 1  # [-]
        alpha_5 = 1  # [-]
        alpha_6 = 1  # [-]
        l_b_rqd = -450  # mm
        l_0_min = 200  # mm

        with pytest.raises(NegativeValueError):
            Form8Dot10DesignLapLength(
                alpha_1=alpha_1,
                alpha_2=alpha_2,
                alpha_3=alpha_3,
                alpha_5=alpha_5,
                alpha_6=alpha_6,
                l_b_rqd=l_b_rqd,
                l_0_min=l_0_min,
            )

    def test_raise_error_if_l_0_min_is_negative(self) -> None:
        """Test that a NegativeValueError is raised if l_0_min is negative."""
        # example values
        alpha_1 = 1  # [-]
        alpha_2 = 1  # [-]
        alpha_3 = 1  # [-]
        alpha_5 = 1  # [-]
        alpha_6 = 1  # [-]
        l_b_rqd = 450  # mm
        l_0_min = -200  # mm

        with pytest.raises(NegativeValueError):
            Form8Dot10DesignLapLength(
                alpha_1=alpha_1,
                alpha_2=alpha_2,
                alpha_3=alpha_3,
                alpha_5=alpha_5,
                alpha_6=alpha_6,
                l_b_rqd=l_b_rqd,
                l_0_min=l_0_min,
            )

    def test_integration_with_form_8_3(self) -> None:
        """Test the integration with formula 8.3."""
        # example values
        alpha_1 = 1  # [-]
        alpha_2 = 1  # [-]
        alpha_3 = 1  # [-]
        alpha_5 = 1  # [-]
        alpha_6 = 1  # [-]
        l_0_min = 200  # mm
        diameter = 16  # mm
        sigma_sd = 500  # MPa
        f_bd = 2.5  # MPa
        l_b_rqd = Form8Dot3RequiredAnchorageLength(
            diameter=diameter,
            sigma_sd=sigma_sd,
            f_bd=f_bd,
        )

        # manually calculated result
        manually_calculated_result = 800  # mm

        assert Form8Dot10DesignLapLength(
            alpha_1=alpha_1,
            alpha_2=alpha_2,
            alpha_3=alpha_3,
            alpha_5=alpha_5,
            alpha_6=alpha_6,
            l_b_rqd=l_b_rqd,
            l_0_min=l_0_min,
        ) == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_integration_with_sub_form_8_10(self) -> None:
        """Test the integration with sub formula 8.10."""
        # example values
        alpha_1 = 1  # [-]
        alpha_2 = 1  # [-]
        alpha_3 = 1  # [-]
        alpha_5 = 1  # [-]
        l_b_rqd = 450  # mm
        l_0_min = 200  # mm
        rho_1 = 0.5  # [-]
        alpha_6 = SubForm8Dot10Alpha6(
            rho_1=rho_1,
        )
        form_8_10 = Form8Dot10DesignLapLength(
            alpha_1=alpha_1,
            alpha_2=alpha_2,
            alpha_3=alpha_3,
            alpha_5=alpha_5,
            alpha_6=alpha_6,
            l_b_rqd=l_b_rqd,
            l_0_min=l_0_min,
        )

        # manually calculated result
        manually_calculated_result = 450  # mm

        assert form_8_10 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_integration_with_form_8_11(self) -> None:
        """Test the evaluation of the result."""
        # example values
        alpha_1 = 1  # [-]
        alpha_2 = 1  # [-]
        alpha_3 = 1  # [-]
        alpha_5 = 1  # [-]
        alpha_6 = 1  # [-]
        l_b_rqd = 200  # mm
        diameter = 16  # mm
        l_0_min = Form8Dot11MinimumDesignLapLength(
            alpha_6=alpha_6,
            l_b_rqd=l_b_rqd,
            diameter=diameter,
        )
        form_8_10 = Form8Dot10DesignLapLength(
            alpha_1=alpha_1,
            alpha_2=alpha_2,
            alpha_3=alpha_3,
            alpha_5=alpha_5,
            alpha_6=alpha_6,
            l_b_rqd=l_b_rqd,
            l_0_min=l_0_min,
        )

        # manually calculated result
        manually_calculated_result = 240  # mm

        assert form_8_10 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            (
                "complete",
                r"l_{0} = \max \left\{\alpha_1 \cdot \alpha_2 \cdot \alpha_3 \cdot \alpha_5 \cdot \alpha_6 \cdot l_{b,rqd};"
                r" l_{0,min}\right\} = \max \left\{1.00 \cdot 1.00 \cdot 1.00 \cdot 1.00 \cdot 1.00 \cdot 200.00; 400.00\right\} = 400.00",
            ),
            ("short", "l_{0} = 400.00"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test latex representation of the formula."""
        alpha_1 = 1  # [-]
        alpha_2 = 1  # [-]
        alpha_3 = 1  # [-]
        alpha_5 = 1  # [-]
        alpha_6 = 1  # [-]
        l_b_rqd = 200  # mm
        l_0_min = 400  # mm

        latex = Form8Dot10DesignLapLength(
            alpha_1=alpha_1,
            alpha_2=alpha_2,
            alpha_3=alpha_3,
            alpha_5=alpha_5,
            alpha_6=alpha_6,
            l_b_rqd=l_b_rqd,
            l_0_min=l_0_min,
        ).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."

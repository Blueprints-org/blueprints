"""Testing formula 8.10 of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ, duplicate-code, fixme


import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_3 import (
    Form8Dot3RequiredAnchorageLength,
)
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_10 import (
    Form8Dot10DesignLapLength,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot10DesignLapLength:
    """Validation for formula 8.10 from NEN-EN 1992-1-1+C2:2011."""

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
        phi = 16  # mm
        sigma_sd = 500  # MPa
        f_bd = 2.5  # MPa
        l_b_rqd = Form8Dot3RequiredAnchorageLength(
            phi=phi,
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

        # TODO INTEGRATION TEST WITH FORMULA 8.11 WHEN MERGED

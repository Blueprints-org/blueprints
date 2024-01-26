"""Testing formula 8.4 of NEN-EN 1992-1-1+C2:2011."""
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_3 import (
    Form8Dot3RequiredAnchorageLength,
)
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_4 import (
    Form8Dot4DesignAnchorageLength,
)
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_6 import (
    Form8Dot6MinimumTensionAnchorage,
)
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_7 import (
    Form8Dot7MinimumCompressionAnchorage,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot4DesignAnchorageLength:
    """Validation for formula 8.4 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        alpha_1 = 1  # [-]
        alpha_2 = 1  # [-]
        alpha_3 = 1  # [-]
        alpha_4 = 1  # [-]
        alpha_5 = 1  # [-]
        l_b_rqd = 450  # mm
        l_b_min = 200  # mm
        form_8_4 = Form8Dot4DesignAnchorageLength(
            alpha_1=alpha_1,
            alpha_2=alpha_2,
            alpha_3=alpha_3,
            alpha_4=alpha_4,
            alpha_5=alpha_5,
            l_b_rqd=l_b_rqd,
            l_b_min=l_b_min,
        )

        # manually calculated result
        manually_calculated_result = 450  # mm

        assert form_8_4 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_minimum(self) -> None:
        """Test the evaluation of the result if the minimum is reached."""
        # example values
        alpha_1 = 1  # [-]
        alpha_2 = 1  # [-]
        alpha_3 = 1  # [-]
        alpha_4 = 1  # [-]
        alpha_5 = 1  # [-]
        l_b_rqd = 200  # mm
        l_b_min = 300  # mm
        form_8_4 = Form8Dot4DesignAnchorageLength(
            alpha_1=alpha_1,
            alpha_2=alpha_2,
            alpha_3=alpha_3,
            alpha_4=alpha_4,
            alpha_5=alpha_5,
            l_b_rqd=l_b_rqd,
            l_b_min=l_b_min,
        )

        # manually calculated result
        manually_calculated_result = 300  # mm

        assert form_8_4 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("alpha_1", "alpha_2", "alpha_3", "alpha_4", "alpha_5"),
        [
            (-1, 1, 1, 1, 1),  # alpha_1 is negative
            (1, -1, 1, 1, 1),  # alpha_2 is negative
            (1, 1, -1, 1, 1),  # alpha_3 is negative
            (1, 1, 1, -1, 1),  # alpha_4 is negative
            (1, 1, 1, 1, -1),  # alpha_5 is negative
        ],
    )
    def test_negative_alpha(self, alpha_1: float, alpha_2: float, alpha_3: float, alpha_4: float, alpha_5: float) -> None:
        """Test the evaluation of the result if one of the alpha values is negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot4DesignAnchorageLength(
                alpha_1=alpha_1,
                alpha_2=alpha_2,
                alpha_3=alpha_3,
                alpha_4=alpha_4,
                alpha_5=alpha_5,
                l_b_rqd=450,  # mm
                l_b_min=200,  # mm
            )

    def test_integration_with_form_8_3(self) -> None:
        """Test the integration with formula 8.3."""
        # example values
        alpha_1 = 1  # [-]
        alpha_2 = 1  # [-]
        alpha_3 = 1  # [-]
        alpha_4 = 1  # [-]
        alpha_5 = 1  # [-]
        l_b_min = 200  # mm
        diameter = 16  # mm
        sigma_sd = 500  # MPa
        f_bd = 2.5  # MPa
        l_b_rqd = Form8Dot3RequiredAnchorageLength(
            diameter=diameter,
            sigma_sd=sigma_sd,
            f_bd=f_bd,
        )

        # manually calculated result
        manually_calculated_result = 800

        assert Form8Dot4DesignAnchorageLength(
            alpha_1=alpha_1,
            alpha_2=alpha_2,
            alpha_3=alpha_3,
            alpha_4=alpha_4,
            alpha_5=alpha_5,
            l_b_rqd=l_b_rqd,
            l_b_min=l_b_min,
        ) == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_integration_with_form_8_6(self) -> None:
        """Test the integration with formula 8.6."""
        # example values
        alpha_1 = 1  # [-]
        alpha_2 = 1  # [-]
        alpha_3 = 1  # [-]
        alpha_4 = 1  # [-]
        alpha_5 = 1  # [-]
        l_b_rqd = 450  # mm
        diameter = 16  # mm
        l_b_min = Form8Dot6MinimumTensionAnchorage(l_b_rqd=l_b_rqd, diameter=diameter)

        # manually calculated result
        manually_calculated_result = 450

        assert Form8Dot4DesignAnchorageLength(
            alpha_1=alpha_1,
            alpha_2=alpha_2,
            alpha_3=alpha_3,
            alpha_4=alpha_4,
            alpha_5=alpha_5,
            l_b_rqd=l_b_rqd,
            l_b_min=l_b_min,
        ) == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_integration_with_form_8_7(self) -> None:
        """Test the integration with formula 8.7."""
        # example values
        alpha_1 = 1  # [-]
        alpha_2 = 1  # [-]
        alpha_3 = 1  # [-]
        alpha_4 = 1  # [-]
        alpha_5 = 1  # [-]
        l_b_rqd = 200  # mm
        diameter = 32  # mm
        l_b_min = Form8Dot7MinimumCompressionAnchorage(l_b_rqd=l_b_rqd, diameter=diameter)

        # manually calculated result
        manually_calculated_result = 320

        assert Form8Dot4DesignAnchorageLength(
            alpha_1=alpha_1,
            alpha_2=alpha_2,
            alpha_3=alpha_3,
            alpha_4=alpha_4,
            alpha_5=alpha_5,
            l_b_rqd=l_b_rqd,
            l_b_min=l_b_min,
        ) == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_latex(self) -> None:
        """Test latex representation of the formula."""
        alpha_1 = 1  # [-]
        alpha_2 = 1  # [-]
        alpha_3 = 1  # [-]
        alpha_4 = 1  # [-]
        alpha_5 = 1  # [-]
        l_b_rqd = 200  # mm
        l_b_min = 400  # mm
        latex = Form8Dot4DesignAnchorageLength(
            alpha_1=alpha_1,
            alpha_2=alpha_2,
            alpha_3=alpha_3,
            alpha_4=alpha_4,
            alpha_5=alpha_5,
            l_b_rqd=l_b_rqd,
            l_b_min=l_b_min,
        ).latex()
        assert latex.complete == (
            r"l_{bd} = \max \left\{\alpha_1 \cdot \alpha_2 \cdot \alpha_3 \cdot \alpha_4 \cdot \alpha_5 \cdot l_{b,rqd}; "
            r"l_{b,min}\right\} = \max \left\{1 \cdot 1 \cdot 1 \cdot 1 \cdot 1 \cdot 200; \text{400}\right\} = 400.0"
        )
        assert latex.short == r"l_{bd} = 400.0"

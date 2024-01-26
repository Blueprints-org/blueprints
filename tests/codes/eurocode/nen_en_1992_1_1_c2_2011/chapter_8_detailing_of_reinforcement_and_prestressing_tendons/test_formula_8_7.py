"""Testing formula 8.7 of NEN-EN 1992-1-1+C2:2011."""
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_3 import (
    Form8Dot3RequiredAnchorageLength,
)
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_7 import (
    Form8Dot7MinimumCompressionAnchorage,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot7MinimumCompressionAnchorage:
    """Validation for formula 8.7 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation_first_term_decisive(self) -> None:
        """Test the evaluation of the result if the first term is decisive."""
        # example values
        l_b_rqd = 500  # mm
        diameter = 8  # mm
        form_8_7 = Form8Dot7MinimumCompressionAnchorage(l_b_rqd=l_b_rqd, diameter=diameter)

        manually_calculated_result = 300  # mm

        assert form_8_7 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_second_term_decisive(self) -> None:
        """Test the evaluation of the result if the second term is decisive."""
        # example values
        l_b_rqd = 200  # mm
        diameter = 16  # mm
        form_8_7 = Form8Dot7MinimumCompressionAnchorage(l_b_rqd=l_b_rqd, diameter=diameter)

        manually_calculated_result = 160  # mm

        assert form_8_7 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_third_term_decisive(self) -> None:
        """Test the evaluation of the result if the third term is decisive."""
        # example values
        l_b_rqd = 150  # mm
        diameter = 8  # mm

        form_8_7 = Form8Dot7MinimumCompressionAnchorage(l_b_rqd=l_b_rqd, diameter=diameter)

        manually_calculated_result = 100  # mm

        assert form_8_7 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_negative_l_b_rqd(self) -> None:
        """Test if NegativeValueError is raised for negative l_b_rqd."""
        # example values
        l_b_rqd = -500  # mm
        diameter = 8  # mm

        with pytest.raises(NegativeValueError):
            Form8Dot7MinimumCompressionAnchorage(l_b_rqd=l_b_rqd, diameter=diameter)

    def test_evaluation_negative_diameter(self) -> None:
        """Test if NegativeValueError is raised for negative diameter."""
        # example values
        l_b_rqd = 500  # mm
        diameter = -8  # mm

        with pytest.raises(NegativeValueError):
            Form8Dot7MinimumCompressionAnchorage(l_b_rqd=l_b_rqd, diameter=diameter)

    def test_integration_with_form_8_3(self) -> None:
        """Test the integration with Form8Dot3RequiredAnchorageLength."""
        # example values
        diameter = 12  # mm
        sigma_sd = 435  # MPA
        f_bd = 2.9  # MPA
        l_b_rqd = Form8Dot3RequiredAnchorageLength(diameter=diameter, sigma_sd=sigma_sd, f_bd=f_bd)

        form_8_7 = Form8Dot7MinimumCompressionAnchorage(l_b_rqd=l_b_rqd, diameter=diameter)

        manually_calculated_result = 270  # mm

        assert form_8_7 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_latex(self) -> None:
        """Test the latex representation."""
        # example values
        l_b_rqd = 500
        diameter = 8
        latex = Form8Dot7MinimumCompressionAnchorage(l_b_rqd=l_b_rqd, diameter=diameter).latex()

        assert latex.complete == (
            r"l_{b,min} = \max \left\{0.6 \cdot l_{b,rqd}; 10 \cdot Ø; 100 \ \text{mm}\right\} = \max \left\{0.6 \cdot 500.00;"
            r" 10 \cdot 8; 100\right\} = 300.00"
        )
        assert latex.short == r"l_{b,min} = 300.00"
        assert str(latex) == (
            r"l_{b,min} = \max \left\{0.6 \cdot l_{b,rqd}; 10 \cdot Ø; 100 \ \text{mm}\right\} = \max \left\{0.6 \cdot 500.00;"
            r" 10 \cdot 8; 100\right\} = 300.00"
        )

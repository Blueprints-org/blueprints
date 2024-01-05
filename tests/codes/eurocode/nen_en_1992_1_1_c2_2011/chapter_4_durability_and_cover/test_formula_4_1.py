"""Testing formula 4.1 of NEN-EN 1992-1-1+C2:2011."""
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.formula_4_1 import Form4Dot1NominalConcreteCover
from blueprints.validations import NegativeValueError


class TestForm4Dot1NominalConcreteCover:
    """Validation for formula 4.1 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        c_min = 60  # mm
        delta_c_dev = 5  # mm
        form_4_1 = Form4Dot1NominalConcreteCover(c_min=c_min, delta_c_dev=delta_c_dev)

        # Expected result, manually calculated
        manually_calculated_result = 65

        assert form_4_1 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_c_min_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        c_min = -60  # mm
        delta_c_dev = 5  # mm

        with pytest.raises(NegativeValueError):
            Form4Dot1NominalConcreteCover(c_min=c_min, delta_c_dev=delta_c_dev)

    def test_raise_error_when_negative_delta_c_dev_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        c_min = 60  # mm
        delta_c_dev = -5  # mm

        with pytest.raises(NegativeValueError):
            Form4Dot1NominalConcreteCover(c_min=c_min, delta_c_dev=delta_c_dev)


def test_latex() -> None:
    """Test the latex implementation."""
    c_min = 60  # mm
    delta_c_dev = 5  # mm
    form = Form4Dot1NominalConcreteCover(c_min=c_min, delta_c_dev=delta_c_dev)

    assert form.latex().complete == r"c_{\text{nom}} = c_{\text{min}}+\Delta c_{\text{dev}} = \text{60}+\text{5} = \text{65.0}"
    assert form.latex().short == r"c_{\text{nom}} = \text{65.0}"
    assert str(form.latex()) == r"c_{\text{nom}} = c_{\text{min}}+\Delta c_{\text{dev}} = \text{60}+\text{5} = \text{65.0}"

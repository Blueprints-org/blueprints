"""Testing formula 4.1 of NEN-EN 1992-1-1+C2:2011."""
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.formula_4_1 import Form4Dot1NominalConcreteCover


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

        with pytest.raises(ValueError):
            Form4Dot1NominalConcreteCover(c_min=c_min, delta_c_dev=delta_c_dev)

    def test_raise_error_when_negative_delta_c_dev_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        c_min = 60  # mm
        delta_c_dev = -5  # mm

        with pytest.raises(ValueError):
            Form4Dot1NominalConcreteCover(c_min=c_min, delta_c_dev=delta_c_dev)

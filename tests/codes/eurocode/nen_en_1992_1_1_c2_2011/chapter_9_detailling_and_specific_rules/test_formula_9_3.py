"""Testing formula 9.3 of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_9_detailling_and_specific_rules.formula_9_3 import Form9Dot3ShiftInMomentDiagram


class TestForm9Dot3ShiftInMomentDiagram:
    """Validation for formula 9.3 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        v_ed = -200  # kN
        a_l = 200  # mm
        z = 250  # mm
        n_ed = 500  # deg
        form_9_3 = Form9Dot3ShiftInMomentDiagram(
            v_ed=v_ed,
            a_l=a_l,
            z=z,
            n_ed=n_ed,
        )

        # Expected result, manually calculated
        manually_calculated_result = 660

        assert form_9_3 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_z_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        v_ed = -200  # kN
        a_l = 200  # mm
        z = -250  # mm
        n_ed = 500  # deg

        with pytest.raises(ValueError):
            Form9Dot3ShiftInMomentDiagram(
                v_ed=v_ed,
                a_l=a_l,
                z=z,
                n_ed=n_ed,
            )

    def test_raise_error_when_negative_a_l_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        v_ed = -200  # kN
        a_l = -200  # mm
        z = 250  # mm
        n_ed = 500  # deg

        with pytest.raises(ValueError):
            Form9Dot3ShiftInMomentDiagram(
                v_ed=v_ed,
                a_l=a_l,
                z=z,
                n_ed=n_ed,
            )

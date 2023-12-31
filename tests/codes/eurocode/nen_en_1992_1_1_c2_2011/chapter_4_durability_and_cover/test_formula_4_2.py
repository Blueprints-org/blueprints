"""Testing formula 4.2 of NEN-EN 1992-1-1+C2:2011."""
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.formula_4_2 import Form4Dot2MinimumConcreteCover


class TestForm4Dot1NominalConcreteCover:
    """Validation for formula 4.2 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        c_min_b = 15  # mm
        c_min_dur = 10  # mm
        delta_c_dur_gamma = 5  # mm
        delta_c_dur_st = 5  # mm
        delta_c_dur_add = 0  # mm
        form_4_2 = Form4Dot2MinimumConcreteCover(
            c_min_b=c_min_b,
            c_min_dur=c_min_dur,
            delta_c_dur_gamma=delta_c_dur_gamma,
            delta_c_dur_st=delta_c_dur_st,
            delta_c_dur_add=delta_c_dur_add,
        )

        # Expected result, manually calculated
        manually_calculated_result = 15

        assert form_4_2 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_c_min_b_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        c_min_b = -15  # mm
        c_min_dur = 10  # mm
        delta_c_dur_gamma = 5  # mm
        delta_c_dur_st = 5  # mm
        delta_c_dur_add = 0  # mm

        with pytest.raises(ValueError):
            Form4Dot2MinimumConcreteCover(
                c_min_b=c_min_b,
                c_min_dur=c_min_dur,
                delta_c_dur_gamma=delta_c_dur_gamma,
                delta_c_dur_st=delta_c_dur_st,
                delta_c_dur_add=delta_c_dur_add,
            )

    def test_raise_error_when_negative_c_min_dur_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        c_min_b = 15  # mm
        c_min_dur = -10  # mm
        delta_c_dur_gamma = 5  # mm
        delta_c_dur_st = 5  # mm
        delta_c_dur_add = 0  # mm

        with pytest.raises(ValueError):
            Form4Dot2MinimumConcreteCover(
                c_min_b=c_min_b,
                c_min_dur=c_min_dur,
                delta_c_dur_gamma=delta_c_dur_gamma,
                delta_c_dur_st=delta_c_dur_st,
                delta_c_dur_add=delta_c_dur_add,
            )

    def test_raise_error_when_negative_delta_c_dur_gamma_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        c_min_b = 15  # mm
        c_min_dur = 10  # mm
        delta_c_dur_gamma = -5  # mm
        delta_c_dur_st = 5  # mm
        delta_c_dur_add = 0  # mm

        with pytest.raises(ValueError):
            Form4Dot2MinimumConcreteCover(
                c_min_b=c_min_b,
                c_min_dur=c_min_dur,
                delta_c_dur_gamma=delta_c_dur_gamma,
                delta_c_dur_st=delta_c_dur_st,
                delta_c_dur_add=delta_c_dur_add,
            )

    def test_raise_error_when_negative_delta_c_dur_st_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        c_min_b = 15  # mm
        c_min_dur = 10  # mm
        delta_c_dur_gamma = 5  # mm
        delta_c_dur_st = -5  # mm
        delta_c_dur_add = 0  # mm

        with pytest.raises(ValueError):
            Form4Dot2MinimumConcreteCover(
                c_min_b=c_min_b,
                c_min_dur=c_min_dur,
                delta_c_dur_gamma=delta_c_dur_gamma,
                delta_c_dur_st=delta_c_dur_st,
                delta_c_dur_add=delta_c_dur_add,
            )

    def test_raise_error_when_negative_delta_c_dur_add_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        c_min_b = 15  # mm
        c_min_dur = 10  # mm
        delta_c_dur_gamma = 5  # mm
        delta_c_dur_st = 5  # mm
        delta_c_dur_add = -5  # mm

        with pytest.raises(ValueError):
            Form4Dot2MinimumConcreteCover(
                c_min_b=c_min_b,
                c_min_dur=c_min_dur,
                delta_c_dur_gamma=delta_c_dur_gamma,
                delta_c_dur_st=delta_c_dur_st,
                delta_c_dur_add=delta_c_dur_add,
            )
